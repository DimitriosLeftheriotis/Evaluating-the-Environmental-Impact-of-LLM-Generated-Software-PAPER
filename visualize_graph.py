#!/usr/bin/env python3
"""
Graph Visualization Script for graph_100.csv (and other graph scale CSVs)
--------------------------------------------------------------------------
This script parses a weighted edge list CSV, constructs a NetworkX graph,
and generates a high-quality visual representation showing node degrees
and edge weights using modern, aesthetic color palettes.

Features:
- Configurable themes (dark/light mode)
- Edge colors and widths mapped to weights
- Node sizes and colors mapped to degrees
- Automatic statistics calculation
- High resolution output (300 DPI)

Usage:
  python visualize_graph.py [--csv data/graph/graph_100.csv] [--output graph_100_visualization.png] [--theme dark] [--layout spring] [--show]
"""

import os
import sys
import csv
import argparse

# -------------------------------------------------------------------------
# Dependency Check & Import
# -------------------------------------------------------------------------
missing_packages = []
try:
    import networkx as nx
except ImportError:
    missing_packages.append("networkx")

try:
    import matplotlib
    import matplotlib.pyplot as plt
    import matplotlib.colors as mcolors
    import matplotlib.cm as cm
except ImportError:
    missing_packages.append("matplotlib")

try:
    import numpy as np
except ImportError:
    missing_packages.append("numpy")

if missing_packages:
    print("[-] Missing required packages. Please install them using pip:")
    print(f"    pip install {' '.join(missing_packages)}")
    sys.exit(1)


# -------------------------------------------------------------------------
# Argument Parser Setup
# -------------------------------------------------------------------------
def parse_arguments():
    parser = argparse.ArgumentParser(
        description="Visualize a weighted graph from a CSV file."
    )
    
    # Calculate default CSV path relative to this script
    script_dir = os.path.dirname(os.path.abspath(__file__))
    default_csv = os.path.join(script_dir, "data", "graph", "graph_100.csv")
    if not os.path.exists(default_csv):
        # Fallback to current directory or standard layout
        default_csv = "data/graph/graph_100.csv"
        
    parser.add_argument(
        "--csv",
        type=str,
        default=default_csv,
        help="Path to the input CSV file containing graph edges (default: data/graph/graph_100.csv)"
    )
    parser.add_argument(
        "--output",
        type=str,
        default="graph_100_visualization.png",
        help="Path to save the output visualization image (default: graph_100_visualization.png)"
    )
    parser.add_argument(
        "--theme",
        type=str,
        choices=["dark", "light"],
        default="dark",
        help="Color theme for visualization (default: dark)"
    )
    parser.add_argument(
        "--layout",
        type=str,
        choices=["spring", "kamada_kawai", "circular", "shell", "spectral"],
        default="spring",
        help="Graph layout algorithm (default: spring)"
    )
    parser.add_argument(
        "--show",
        action="store_true",
        help="Interactively display the graph using matplotlib window"
    )
    return parser.parse_args()


# -------------------------------------------------------------------------
# Graph Reading and Visualization Logic
# -------------------------------------------------------------------------
def visualize_graph(csv_path, output_path, theme, layout_type, show_plot):
    # Verify CSV file existence
    if not os.path.exists(csv_path):
        print(f"[-] CSV file not found at: {csv_path}")
        print("Please check the path or run 'benchmarks/generate_data.py' to generate datasets.")
        sys.exit(1)

    print(f"[+] Loading graph from: {csv_path}")
    
    # Read edges from CSV
    edges = []
    nodes = set()
    try:
        with open(csv_path, mode="r", encoding="utf-8") as f:
            reader = csv.reader(f)
            header = next(reader)
            
            # Simple validation
            if len(header) < 3 or header[0].strip().lower() != "source":
                # In case header is missing, reset file pointer
                f.seek(0)
                print("[!] Warning: CSV file may be missing a header. Parsing columns as: source, target, weight.")
            
            for row_idx, row in enumerate(reader, start=2):
                if not row or len(row) < 3:
                    continue
                try:
                    u = int(row[0])
                    v = int(row[1])
                    w = float(row[2])
                    edges.append((u, v, w))
                    nodes.add(u)
                    nodes.add(v)
                except ValueError as ve:
                    print(f"[!] Warning: Row {row_idx} is malformed or headers mismatch: {row}. Error: {ve}")
    except Exception as e:
        print(f"[-] Failed to read CSV file: {e}")
        sys.exit(1)

    num_nodes = len(nodes)
    num_edges = len(edges)
    
    if num_nodes == 0 or num_edges == 0:
        print("[-] The graph contains no nodes or edges. Visualization aborted.")
        sys.exit(1)

    print(f"[+] Successfully loaded graph with {num_nodes} nodes and {num_edges} edges.")

    # Create networkx Graph
    # The benchmark suite treats this as an undirected graph, so we visualize it as undirected
    G = nx.Graph()
    G.add_nodes_from(nodes)
    for u, v, w in edges:
        G.add_edge(u, v, weight=w)

    # -------------------------------------------------------------------------
    # Visual Theme Styles Configuration
    # -------------------------------------------------------------------------
    if theme == "dark":
        bg_color = "#121214"
        card_color = "#1e1e24"
        text_color = "#e4e4e7"
        text_muted = "#a1a1aa"
        node_cmap = cm.plasma  # Node colors map (plasma: blue -> purple -> yellow)
        edge_cmap = cm.viridis  # Edge colors map (viridis: purple -> green -> yellow)
        accent_color = "#06b6d4"  # Cyan accent
        grid_color = "#27272a"
    else:  # light theme
        bg_color = "#f8fafc"
        card_color = "#ffffff"
        text_color = "#0f172a"
        text_muted = "#64748b"
        node_cmap = cm.viridis
        edge_cmap = cm.plasma
        accent_color = "#2563eb"  # Royal blue accent
        grid_color = "#e2e8f0"

    # Set up matplotlib figure
    plt.rcParams["text.color"] = text_color
    plt.rcParams["axes.labelcolor"] = text_color
    plt.rcParams["xtick.color"] = text_color
    plt.rcParams["ytick.color"] = text_color
    
    fig = plt.figure(figsize=(14, 11), facecolor=bg_color)
    ax = fig.add_subplot(111, facecolor=bg_color)
    
    # Hide axis borders
    for spine in ax.spines.values():
        spine.set_visible(False)
    ax.get_xaxis().set_visible(False)
    ax.get_yaxis().set_visible(False)

    # -------------------------------------------------------------------------
    # Layout Calculation
    # -------------------------------------------------------------------------
    print(f"[+] Computing graph layout using '{layout_type}' algorithm...")
    if layout_type == "spring":
        # Optimal spacing 'k' changes based on number of nodes to avoid overlapping/cramming
        k_val = 1.65 / np.sqrt(num_nodes)
        pos = nx.spring_layout(G, k=k_val, iterations=60, seed=100)
    elif layout_type == "kamada_kawai":
        pos = nx.kamada_kawai_layout(G)
    elif layout_type == "circular":
        pos = nx.circular_layout(G)
    elif layout_type == "shell":
        pos = nx.shell_layout(G)
    elif layout_type == "spectral":
        pos = nx.spectral_layout(G)
    else:
        pos = nx.spring_layout(G, seed=100)

    # -------------------------------------------------------------------------
    # Node Scaling and Coloring (Mapped to Degree)
    # -------------------------------------------------------------------------
    degrees = dict(G.degree())
    max_degree = max(degrees.values()) if degrees else 1
    min_degree = min(degrees.values()) if degrees else 0
    
    # Calculate sizes: scale node size proportional to its degree
    node_sizes = [50 + (degrees[node] / max_degree) * 450 for node in G.nodes()]
    node_colors = [degrees[node] for node in G.nodes()]

    # -------------------------------------------------------------------------
    # Edge Scaling and Coloring (Mapped to Weight)
    # -------------------------------------------------------------------------
    weights = [G[u][v]["weight"] for u, v in G.edges()]
    min_weight = min(weights) if weights else 1.0
    max_weight = max(weights) if weights else 50.0
    weight_range = (max_weight - min_weight) if (max_weight - min_weight) > 0 else 1.0

    # Scale edge width: thicker line for higher weight
    edge_widths = [0.8 + ((w - min_weight) / weight_range) * 3.2 for w in weights]
    # Edge alpha (transparency): faint for low weights, strong for high weights
    edge_alphas = [0.2 + ((w - min_weight) / weight_range) * 0.65 for w in weights]

    # Draw Edges one-by-one or in groups to support custom alpha per edge
    print("[+] Drawing graph edges...")
    # Sort edges by weight so stronger edges are drawn on top
    sorted_edges = sorted(G.edges(data=True), key=lambda x: x[2]["weight"])
    
    # Normalize weights for colormap matching
    norm = mcolors.Normalize(vmin=min_weight, vmax=max_weight)
    
    for u, v, data in sorted_edges:
        w = data["weight"]
        w_norm = norm(w)
        ec = edge_cmap(w_norm)
        # Apply alpha proportional to weight
        alpha = 0.15 + (w_norm * 0.65)
        # Combine color and alpha
        rgba_color = mcolors.to_rgba(ec, alpha=alpha)
        
        # Calculate width
        width = 0.6 + (w_norm * 2.8)
        
        nx.draw_networkx_edges(
            G, pos,
            edgelist=[(u, v)],
            width=width,
            edge_color=[rgba_color],
            ax=ax,
            arrows=False
        )

    # Draw Nodes
    print("[+] Drawing graph nodes...")
    nodes_draw = nx.draw_networkx_nodes(
        G, pos,
        node_size=node_sizes,
        node_color=node_colors,
        cmap=node_cmap,
        alpha=0.9,
        edgecolors=bg_color,
        linewidths=1.2,
        ax=ax
    )

    # Optional labels for nodes (label top 15% highest degree nodes to prevent overlap/clutter)
    # Or label all nodes if size <= 100, but with a small, readable offset font
    if num_nodes <= 100:
        print("[+] Drawing node labels...")
        # Customize labels mapping to only show node IDs
        labels = {n: str(n) for n in G.nodes()}
        
        # Determine labels positions with a small vertical shift to avoid overlaying nodes
        label_pos = {node: (coords[0], coords[1] - 0.02) for node, coords in pos.items()}
        
        nx.draw_networkx_labels(
            G, label_pos,
            labels=labels,
            font_size=8,
            font_color=text_color,
            font_weight="bold",
            alpha=0.85,
            ax=ax
        )

    # -------------------------------------------------------------------------
    # Colorbar and Legend
    # -------------------------------------------------------------------------
    # Add a horizontal colorbar for Edge Weights
    sm_edge = plt.cm.ScalarMappable(cmap=edge_cmap, norm=norm)
    sm_edge.set_array([])
    cbar_ax = fig.add_axes([0.15, 0.08, 0.7, 0.02])  # [left, bottom, width, height]
    cbar = fig.colorbar(sm_edge, cax=cbar_ax, orientation="horizontal")
    cbar.set_label("Edge Weights (Thickness & Opacity scale with Weight)", color=text_color, fontsize=10, labelpad=8)
    cbar.ax.xaxis.set_tick_params(color=text_color, labelcolor=text_color, labelsize=9)
    cbar.outline.set_visible(False)
    
    # -------------------------------------------------------------------------
    # Graph Info and Statistics Panel
    # -------------------------------------------------------------------------
    density = nx.density(G)
    avg_degree = sum(degrees.values()) / num_nodes if num_nodes > 0 else 0
    avg_clustering = nx.average_clustering(G) if num_nodes > 0 else 0
    
    info_text = (
        f"Graph Scale: {num_nodes} Nodes\n"
        f"Edge Count: {num_edges}\n"
        f"Graph Density: {density:.3f}\n"
        f"Avg Node Degree: {avg_degree:.2f}\n"
        f"Avg Clustering Coeff: {avg_clustering:.3f}"
    )
    
    # Draw stats box in the upper left corner
    ax.text(
        0.02, 0.98, info_text,
        transform=ax.transAxes,
        fontsize=10,
        fontfamily="monospace",
        color=text_color,
        verticalalignment="top",
        bbox=dict(
            boxstyle="round,pad=0.8",
            facecolor=card_color,
            edgecolor=grid_color,
            alpha=0.9
        )
    )

    # -------------------------------------------------------------------------
    # Main Styling & Title
    # -------------------------------------------------------------------------
    file_name = os.path.basename(csv_path)
    title_str = f"Network Topology Visualization — {file_name}"
    
    # Add a nice prominent title
    fig.suptitle(
        title_str,
        color=text_color,
        fontsize=18,
        fontweight="bold",
        y=0.96
    )
    
    # Subtitle with metadata
    ax.set_title(
        f"Theme: {theme.upper()} | Layout: {layout_type.upper()} | Generated using NetworkX & Matplotlib",
        color=text_muted,
        fontsize=11,
        pad=20
    )

    # Clean up margins and save
    plt.subplots_adjust(top=0.90, bottom=0.15, left=0.05, right=0.95)
    
    print(f"[+] Saving visualization to: {output_path}")
    plt.savefig(
        output_path,
        facecolor=bg_color,
        edgecolor="none",
        dpi=300,
        bbox_inches="tight"
    )
    
    if show_plot:
        print("[+] Displaying plot window...")
        plt.show()
        
    plt.close(fig)
    print("[+] Visualization process completed successfully.")


# -------------------------------------------------------------------------
# Execution Entry Point
# -------------------------------------------------------------------------
if __name__ == "__main__":
    args = parse_arguments()
    visualize_graph(
        csv_path=args.csv,
        output_path=args.output,
        theme=args.theme,
        layout_type=args.layout,
        show_plot=args.show
    )
