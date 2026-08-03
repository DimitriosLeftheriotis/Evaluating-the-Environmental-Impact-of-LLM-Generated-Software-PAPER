import os
import json
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path

# Set style for publication-quality figures
plt.style.use('seaborn-v0_8-whitegrid' if 'seaborn-v0_8-whitegrid' in plt.style.available else 'default')
plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['font.sans-serif'] = ['DejaVu Sans', 'Arial', 'Helvetica']
plt.rcParams['axes.edgecolor'] = '#cccccc'
plt.rcParams['axes.linewidth'] = 1.0

# Define custom color palette for the 3 LLMs
LLM_COLORS = {
    'chatgpt': '#10a37f',  # OpenAI Emerald Teal
    'claude': '#d97706',   # Anthropic Amber / Terracotta
    'gemini': '#1a73e8'    # Google Blue
}

LLM_LABELS = {
    'chatgpt': 'ChatGPT',
    'claude': 'Claude',
    'gemini': 'Gemini'
}

LLM_MARKERS = {
    'chatgpt': 'o',
    'claude': 's',
    'gemini': '^'
}

def load_data(csv_path="median_emissions.csv"):
    df = pd.read_csv(csv_path)
    df['llm'] = df['llm'].str.lower()
    return df

def cleanup_log_files(output_dir="plots"):
    output_path = Path(output_dir)
    if output_path.exists():
        for p in output_path.rglob("*log*"):
            if p.is_file():
                try:
                    p.unlink()
                    print(f"[-] Removed log view file: {p}")
                except Exception as e:
                    print(f"[-] Error removing {p}: {e}")

def generate_static_plots(df, output_dir="plots"):
    line_dir = Path(output_dir) / "line_plots"
    bar_dir = Path(output_dir) / "bar_plots"
    cat_dir = Path(output_dir) / "categories"
    
    line_dir.mkdir(parents=True, exist_ok=True)
    bar_dir.mkdir(parents=True, exist_ok=True)
    cat_dir.mkdir(parents=True, exist_ok=True)

    algorithms = sorted(df['algorithm'].unique())
    llms = ['chatgpt', 'claude', 'gemini']

    # -----------------------------------------------------------------
    # INDIVIDUAL ALGORITHM PLOTS (LINE AND BAR - LINEAR SCALE ONLY)
    # -----------------------------------------------------------------
    for algo in algorithms:
        sub_df = df[df['algorithm'] == algo].copy()
        category = sub_df['category'].iloc[0]
        
        sub_df['scale_num'] = pd.to_numeric(sub_df['scale'])
        sub_df = sub_df.sort_values(by=['scale_num', 'llm'])
        scales = sorted(sub_df['scale_num'].unique())
        scale_strs = [str(s) for s in scales]
        x_indices = np.arange(len(scales))

        formatted_algo_title = algo.replace('_', ' ').title()
        formatted_cat_title = category.replace('_', ' ').title()

        # 1. LINE PLOT
        fig, ax = plt.subplots(figsize=(7, 5), dpi=300)
        
        for llm in llms:
            llm_df = sub_df[sub_df['llm'] == llm].sort_values(by='scale_num')
            if not llm_df.empty:
                y_vals = []
                for s in scales:
                    val = llm_df[llm_df['scale_num'] == s]['median_emissions'].values
                    y_vals.append(val[0] if len(val) > 0 else np.nan)
                
                ax.plot(x_indices, y_vals, 
                        marker=LLM_MARKERS.get(llm, 'o'), 
                        markersize=8, 
                        linewidth=2.2, 
                        label=LLM_LABELS.get(llm, llm.capitalize()),
                        color=LLM_COLORS.get(llm, '#333333'))

        ax.set_xticks(x_indices)
        ax.set_xticklabels(scale_strs, fontsize=11, fontweight='bold')
        ax.set_xlabel('Scale (Input Size N)', fontsize=12, fontweight='bold', labelpad=8)
        ax.set_ylabel('Median Emissions (kg CO2eq)', fontsize=12, fontweight='bold', labelpad=8)
        ax.set_title(f'Median Emissions vs Scale: {formatted_algo_title}\n({formatted_cat_title})', 
                     fontsize=13, fontweight='bold', pad=12)

        ax.yaxis.set_major_formatter(plt.ScalarFormatter(useMathText=True))
        ax.ticklabel_format(style='sci', scilimits=(0,0), axis='y')

        ax.tick_params(axis='both', which='major', labelsize=11)
        ax.grid(True, linestyle='--', alpha=0.5)
        ax.legend(title='LLM Implementation', title_fontsize='10', fontsize=10, loc='best', frameon=True)
        
        plt.tight_layout()
        plt.savefig(line_dir / f"{algo}_line.png", dpi=300, bbox_inches='tight')
        plt.close(fig)

        # 2. GROUPED BAR PLOT
        fig, ax = plt.subplots(figsize=(7.5, 5), dpi=300)
        
        bar_width = 0.25
        offsets = [-bar_width, 0, bar_width]

        for idx, llm in enumerate(llms):
            llm_df = sub_df[sub_df['llm'] == llm].sort_values(by='scale_num')
            y_vals = []
            for s in scales:
                val = llm_df[llm_df['scale_num'] == s]['median_emissions'].values
                y_vals.append(val[0] if len(val) > 0 else 0)
            
            x_pos = x_indices + offsets[idx]
            ax.bar(x_pos, y_vals, width=bar_width, 
                   label=LLM_LABELS.get(llm, llm.capitalize()),
                   color=LLM_COLORS.get(llm, '#333333'),
                   edgecolor='white', linewidth=1)

        ax.set_xticks(x_indices)
        ax.set_xticklabels(scale_strs, fontsize=11, fontweight='bold')
        ax.set_xlabel('Scale (Input Size N)', fontsize=12, fontweight='bold', labelpad=8)
        ax.set_ylabel('Median Emissions (kg CO2eq)', fontsize=12, fontweight='bold', labelpad=8)
        ax.set_title(f'Median Emissions Comparison: {formatted_algo_title}\n({formatted_cat_title})', 
                     fontsize=13, fontweight='bold', pad=12)

        ax.yaxis.set_major_formatter(plt.ScalarFormatter(useMathText=True))
        ax.ticklabel_format(style='sci', scilimits=(0,0), axis='y')

        ax.tick_params(axis='both', which='major', labelsize=11)
        ax.grid(True, linestyle='--', alpha=0.5, axis='y')
        ax.legend(title='LLM Implementation', title_fontsize='10', fontsize=10, loc='best', frameon=True)
        
        plt.tight_layout()
        plt.savefig(bar_dir / f"{algo}_bar.png", dpi=300, bbox_inches='tight')
        plt.close(fig)

    # -----------------------------------------------------------------
    # CATEGORY GRID PLOTS (LINEAR SCALE ONLY)
    # -----------------------------------------------------------------
    categories = sorted(df['category'].unique())
    for category in categories:
        cat_df = df[df['category'] == category]
        algos = sorted(cat_df['algorithm'].unique())
        n_algos = len(algos)

        cols = 3 if n_algos >= 3 else n_algos
        rows = int(np.ceil(n_algos / cols))

        # Line grid
        fig, axes = plt.subplots(rows, cols, figsize=(5.5 * cols, 4.5 * rows), dpi=300)
        if n_algos == 1:
            axes = np.array([axes])
        axes = axes.flatten()

        for i, algo in enumerate(algos):
            ax = axes[i]
            sub_df = cat_df[cat_df['algorithm'] == algo].copy()
            sub_df['scale_num'] = pd.to_numeric(sub_df['scale'])
            sub_df = sub_df.sort_values(by=['scale_num', 'llm'])
            scales = sorted(sub_df['scale_num'].unique())
            scale_strs = [str(s) for s in scales]
            x_indices = np.arange(len(scales))

            for llm in llms:
                llm_df = sub_df[sub_df['llm'] == llm].sort_values(by='scale_num')
                y_vals = []
                for s in scales:
                    val = llm_df[llm_df['scale_num'] == s]['median_emissions'].values
                    y_vals.append(val[0] if len(val) > 0 else np.nan)
                
                ax.plot(x_indices, y_vals, 
                        marker=LLM_MARKERS.get(llm, 'o'), 
                        markersize=7, 
                        linewidth=2, 
                        label=LLM_LABELS.get(llm, llm.capitalize()),
                        color=LLM_COLORS.get(llm, '#333333'))

            ax.set_xticks(x_indices)
            ax.set_xticklabels(scale_strs, fontsize=10, fontweight='bold')
            ax.set_xlabel('Scale', fontsize=10, fontweight='bold')
            ax.set_ylabel('Median Emissions (kg CO2eq)', fontsize=9, fontweight='bold')
            ax.set_title(algo.replace('_', ' ').title(), fontsize=12, fontweight='bold')
            ax.yaxis.set_major_formatter(plt.ScalarFormatter(useMathText=True))
            ax.ticklabel_format(style='sci', scilimits=(0,0), axis='y')
            ax.grid(True, linestyle='--', alpha=0.5)
            if i == 0:
                ax.legend(fontsize=9, loc='best')

        for j in range(i + 1, len(axes)):
            fig.delaxes(axes[j])

        formatted_cat = category.replace('_', ' ').title()
        fig.suptitle(f'Median Emissions vs Scale: {formatted_cat} Algorithms', 
                     fontsize=16, fontweight='bold', y=1.02)
        plt.tight_layout()
        plt.savefig(cat_dir / f"{category}_line_grid.png", dpi=300, bbox_inches='tight')
        plt.close(fig)

        # Bar grid
        fig, axes = plt.subplots(rows, cols, figsize=(5.5 * cols, 4.5 * rows), dpi=300)
        if n_algos == 1:
            axes = np.array([axes])
        axes = axes.flatten()

        bar_width = 0.25
        offsets = [-bar_width, 0, bar_width]

        for i, algo in enumerate(algos):
            ax = axes[i]
            sub_df = cat_df[cat_df['algorithm'] == algo].copy()
            sub_df['scale_num'] = pd.to_numeric(sub_df['scale'])
            sub_df = sub_df.sort_values(by=['scale_num', 'llm'])
            scales = sorted(sub_df['scale_num'].unique())
            scale_strs = [str(s) for s in scales]
            x_indices = np.arange(len(scales))

            for idx, llm in enumerate(llms):
                llm_df = sub_df[sub_df['llm'] == llm].sort_values(by='scale_num')
                y_vals = []
                for s in scales:
                    val = llm_df[llm_df['scale_num'] == s]['median_emissions'].values
                    y_vals.append(val[0] if len(val) > 0 else 0)
                
                x_pos = x_indices + offsets[idx]
                ax.bar(x_pos, y_vals, width=bar_width, 
                       label=LLM_LABELS.get(llm, llm.capitalize()),
                       color=LLM_COLORS.get(llm, '#333333'),
                       edgecolor='white', linewidth=0.8)

            ax.set_xticks(x_indices)
            ax.set_xticklabels(scale_strs, fontsize=10, fontweight='bold')
            ax.set_xlabel('Scale', fontsize=10, fontweight='bold')
            ax.set_ylabel('Median Emissions (kg CO2eq)', fontsize=9, fontweight='bold')
            ax.set_title(algo.replace('_', ' ').title(), fontsize=12, fontweight='bold')
            ax.yaxis.set_major_formatter(plt.ScalarFormatter(useMathText=True))
            ax.ticklabel_format(style='sci', scilimits=(0,0), axis='y')
            ax.grid(True, linestyle='--', alpha=0.5, axis='y')
            if i == 0:
                ax.legend(fontsize=9, loc='best')

        for j in range(i + 1, len(axes)):
            fig.delaxes(axes[j])

        fig.suptitle(f'Median Emissions Bar Comparison: {formatted_cat}', 
                     fontsize=16, fontweight='bold', y=1.02)
        plt.tight_layout()
        plt.savefig(cat_dir / f"{category}_bar_grid.png", dpi=300, bbox_inches='tight')
        plt.close(fig)

    # -----------------------------------------------------------------
    # MASTER OVERVIEW GRID PLOT (ALL 21 ALGORITHMS - LINEAR SCALE ONLY)
    # -----------------------------------------------------------------
    cols = 3
    rows = int(np.ceil(len(algorithms) / cols))

    fig, axes = plt.subplots(rows, cols, figsize=(16, 22), dpi=300)
    axes = axes.flatten()

    for i, algo in enumerate(algorithms):
        ax = axes[i]
        sub_df = df[df['algorithm'] == algo].copy()
        category = sub_df['category'].iloc[0]
        sub_df['scale_num'] = pd.to_numeric(sub_df['scale'])
        sub_df = sub_df.sort_values(by=['scale_num', 'llm'])
        scales = sorted(sub_df['scale_num'].unique())
        scale_strs = [str(s) for s in scales]
        x_indices = np.arange(len(scales))

        for llm in llms:
            llm_df = sub_df[sub_df['llm'] == llm].sort_values(by='scale_num')
            y_vals = []
            for s in scales:
                val = llm_df[llm_df['scale_num'] == s]['median_emissions'].values
                y_vals.append(val[0] if len(val) > 0 else np.nan)
            
            ax.plot(x_indices, y_vals, 
                    marker=LLM_MARKERS.get(llm, 'o'), 
                    markersize=6, 
                    linewidth=1.8, 
                    label=LLM_LABELS.get(llm, llm.capitalize()),
                    color=LLM_COLORS.get(llm, '#333333'))

        ax.set_xticks(x_indices)
        ax.set_xticklabels(scale_strs, fontsize=9, fontweight='bold')
        ax.set_xlabel('Scale', fontsize=9, fontweight='bold')
        ax.set_ylabel('Median Emissions (kg CO2eq)', fontsize=8, fontweight='bold')
        ax.set_title(f"{algo.replace('_', ' ').title()}\n({category.replace('_', ' ')})", fontsize=10, fontweight='bold')
        ax.yaxis.set_major_formatter(plt.ScalarFormatter(useMathText=True))
        ax.ticklabel_format(style='sci', scilimits=(0,0), axis='y')
        ax.grid(True, linestyle='--', alpha=0.5)
        if i == 0:
            ax.legend(fontsize=8, loc='best')

    for j in range(i + 1, len(axes)):
        fig.delaxes(axes[j])

    fig.suptitle('Comprehensive Overview: Median Emissions vs Scale across All 21 Algorithms', 
                 fontsize=18, fontweight='bold', y=1.002)
    plt.tight_layout()
    plt.savefig(Path(output_dir) / "all_algorithms_grid.png", dpi=300, bbox_inches='tight')
    plt.close(fig)

    print(f"[+] Static plots generated successfully in '{output_dir}/'")

def create_interactive_dashboard(df, output_dir="plots"):
    dashboard_path = Path(output_dir) / "index.html"
    
    grouped_data = {}
    for (cat, algo), algo_df in df.groupby(['category', 'algorithm']):
        algo_df = algo_df.copy()
        algo_df['scale_num'] = pd.to_numeric(algo_df['scale'])
        algo_df = algo_df.sort_values('scale_num')
        scales = [str(s) for s in sorted(algo_df['scale_num'].unique())]
        
        llm_series = {}
        for llm in ['chatgpt', 'claude', 'gemini']:
            sub = algo_df[algo_df['llm'] == llm]
            y_vals = []
            for s in sorted(algo_df['scale_num'].unique()):
                row = sub[sub['scale_num'] == s]
                y_vals.append(float(row['median_emissions'].iloc[0]) if not row.empty else 0)
            llm_series[llm] = y_vals
            
        grouped_data[algo] = {
            'category': cat,
            'title': algo.replace('_', ' ').title(),
            'scales': scales,
            'series': llm_series
        }

    json_data = json.dumps(grouped_data, indent=2)

    html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>LLM Median Emissions Benchmark Dashboard</title>
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700&display=swap" rel="stylesheet">
    <style>
        :root {{
            --bg-color: #0f172a;
            --card-bg: #1e293b;
            --text-main: #f8fafc;
            --text-muted: #94a3b8;
            --border-color: #334155;
            --chatgpt: #10a37f;
            --claude: #d97706;
            --gemini: #3b82f6;
        }}
        body {{
            font-family: 'Inter', sans-serif;
            background-color: var(--bg-color);
            color: var(--text-main);
            margin: 0;
            padding: 24px;
        }}
        .header {{
            text-align: center;
            margin-bottom: 30px;
        }}
        .header h1 {{
            font-size: 28px;
            font-weight: 700;
            margin-bottom: 8px;
            background: linear-gradient(135deg, #38bdf8, #818cf8);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }}
        .header p {{
            color: var(--text-muted);
            font-size: 15px;
        }}
        .controls {{
            display: flex;
            flex-wrap: wrap;
            gap: 16px;
            justify-content: center;
            align-items: center;
            background-color: var(--card-bg);
            padding: 18px 24px;
            border-radius: 12px;
            border: 1px solid var(--border-color);
            margin-bottom: 30px;
            max-width: 900px;
            margin-left: auto;
            margin-right: auto;
        }}
        .control-group {{
            display: flex;
            flex-direction: column;
            gap: 6px;
        }}
        label {{
            font-size: 12px;
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 0.5px;
            color: var(--text-muted);
        }}
        select, button {{
            background-color: #0f172a;
            color: #fff;
            border: 1px solid var(--border-color);
            padding: 10px 14px;
            border-radius: 8px;
            font-size: 14px;
            font-weight: 500;
            outline: none;
            cursor: pointer;
            transition: all 0.2s ease;
        }}
        select:hover, button:hover {{
            border-color: #38bdf8;
        }}
        .btn-toggle.active {{
            background-color: #0284c7;
            border-color: #38bdf8;
        }}
        .btn-group {{
            display: flex;
            gap: 8px;
        }}
        .chart-card {{
            background-color: var(--card-bg);
            border: 1px solid var(--border-color);
            border-radius: 16px;
            padding: 24px;
            max-width: 1000px;
            margin: 0 auto 30px auto;
            box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.3);
        }}
        .chart-header {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 20px;
        }}
        .chart-title {{
            font-size: 20px;
            font-weight: 600;
        }}
        .chart-subtitle {{
            font-size: 13px;
            color: var(--text-muted);
        }}
        .chart-container {{
            position: relative;
            height: 450px;
            width: 100%;
        }}
    </style>
</head>
<body>

    <div class="header">
        <h1>Evaluating LLM Code Efficiency: Median Emissions</h1>
        <p>Interactive comparison of ChatGPT, Claude, and Gemini across 21 algorithms and 3 scales</p>
    </div>

    <div class="controls">
        <div class="control-group">
            <label>Select Category</label>
            <select id="catSelect" onchange="onCategoryChange()">
                <option value="all">All Categories</option>
                <option value="dynamic_programming">Dynamic Programming</option>
                <option value="graph">Graph</option>
                <option value="matrix">Matrix</option>
                <option value="sorting">Sorting</option>
            </select>
        </div>

        <div class="control-group">
            <label>Select Algorithm</label>
            <select id="algoSelect" onchange="renderMainChart()"></select>
        </div>

        <div class="control-group">
            <label>Chart Type</label>
            <div class="btn-group">
                <button id="btnLine" class="btn-toggle active" onclick="setChartType('line')">Line Plot</button>
                <button id="btnBar" class="btn-toggle" onclick="setChartType('bar')">Bar Chart</button>
            </div>
        </div>
    </div>

    <div class="chart-card">
        <div class="chart-header">
            <div>
                <div class="chart-title" id="mainChartTitle">Edit Distance</div>
                <div class="chart-subtitle" id="mainChartSub">Category: Dynamic Programming</div>
            </div>
        </div>
        <div class="chart-container">
            <canvas id="mainChart"></canvas>
        </div>
    </div>

    <script>
        const data = {json_data};
        let currentChartType = 'line';
        let mainChartInstance = null;

        function populateAlgorithms() {{
            const cat = document.getElementById('catSelect').value;
            const algoSelect = document.getElementById('algoSelect');
            algoSelect.innerHTML = '';
            
            for (const [key, val] of Object.entries(data)) {{
                if (cat === 'all' || val.category === cat) {{
                    const opt = document.createElement('option');
                    opt.value = key;
                    opt.textContent = val.title;
                    algoSelect.appendChild(opt);
                }}
            }}
            renderMainChart();
        }}

        function onCategoryChange() {{
            populateAlgorithms();
        }}

        function setChartType(type) {{
            currentChartType = type;
            document.getElementById('btnLine').classList.toggle('active', type === 'line');
            document.getElementById('btnBar').classList.toggle('active', type === 'bar');
            renderMainChart();
        }}

        function renderMainChart() {{
            const algoKey = document.getElementById('algoSelect').value;
            if (!algoKey || !data[algoKey]) return;

            const item = data[algoKey];
            document.getElementById('mainChartTitle').textContent = item.title;
            document.getElementById('mainChartSub').textContent = `Category: ${{item.category.replace('_', ' ').toUpperCase()}} | X: Scale, Y: Median Emissions (kg CO2eq)`;

            const ctx = document.getElementById('mainChart').getContext('2d');
            if (mainChartInstance) {{
                mainChartInstance.destroy();
            }}

            const datasets = [
                {{
                    label: 'ChatGPT',
                    data: item.series.chatgpt,
                    borderColor: '#10a37f',
                    backgroundColor: 'rgba(16, 163, 127, 0.7)',
                    borderWidth: 3,
                    pointRadius: 6,
                    tension: 0.2
                }},
                {{
                    label: 'Claude',
                    data: item.series.claude,
                    borderColor: '#d97706',
                    backgroundColor: 'rgba(217, 119, 6, 0.7)',
                    borderWidth: 3,
                    pointRadius: 6,
                    tension: 0.2
                }},
                {{
                    label: 'Gemini',
                    data: item.series.gemini,
                    borderColor: '#3b82f6',
                    backgroundColor: 'rgba(59, 130, 246, 0.7)',
                    borderWidth: 3,
                    pointRadius: 6,
                    tension: 0.2
                }}
            ];

            mainChartInstance = new Chart(ctx, {{
                type: currentChartType,
                data: {{
                    labels: item.scales.map(s => 'Scale ' + s),
                    datasets: datasets
                }},
                options: {{
                    responsive: true,
                    maintainAspectRatio: false,
                    plugins: {{
                        legend: {{
                            labels: {{ color: '#f8fafc', font: {{ size: 14, weight: 'bold' }} }}
                        }},
                        tooltip: {{
                            callbacks: {{
                                label: function(context) {{
                                    let val = context.raw;
                                    return context.dataset.label + ': ' + val.toExponential(4) + ' kg CO2eq';
                                }}
                            }}
                        }}
                    }},
                    scales: {{
                        x: {{
                            grid: {{ color: '#334155' }},
                            ticks: {{ color: '#94a3b8', font: {{ size: 13, weight: 'bold' }} }},
                            title: {{ display: true, text: 'Scale (Input Size N)', color: '#94a3b8', font: {{ size: 14, weight: 'bold' }} }}
                        }},
                        y: {{
                            type: 'linear',
                            grid: {{ color: '#334155' }},
                            ticks: {{ 
                                color: '#94a3b8',
                                font: {{ size: 12 }},
                                callback: function(value) {{
                                    return Number(value).toExponential(1);
                                }}
                            }},
                            title: {{ display: true, text: 'Median Emissions (kg CO2eq)', color: '#94a3b8', font: {{ size: 14, weight: 'bold' }} }}
                        }}
                    }}
                }}
            }});
        }}

        // Initialize on load
        populateAlgorithms();
    </script>
</body>
</html>
"""
    with open(dashboard_path, "w", encoding="utf-8") as f:
        f.write(html_content)
    print(f"[+] Saved interactive HTML dashboard to {dashboard_path}")

if __name__ == "__main__":
    df = load_data("median_emissions.csv")
    cleanup_log_files("plots")
    generate_static_plots(df, "plots")
    create_interactive_dashboard(df, "plots")
