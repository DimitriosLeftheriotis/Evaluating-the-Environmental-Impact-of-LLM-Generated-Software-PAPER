import os
import csv
import statistics
from pathlib import Path
import argparse

def get_median_emissions(results_dir="results", output_file="median_emissions.csv"):
    """
    Traverses the results directory, reads the 10 benchmark runs for each CSV file,
    computes the TRUE mathematical median of the 'emissions' column (averaging the 
    5th and 6th sorted elements for 10 runs), and writes the summary to CSV.
    """
    results_path = Path(results_dir)
    
    if results_path.is_file():
        csv_files = [results_path]
        results_path = results_path.parent
    elif results_path.exists():
        csv_files = [
            f for f in results_path.rglob("*.csv") 
            if not f.name.endswith("summary.csv") and not f.name.startswith("median_")
        ]
    else:
        print(f"[-] Directory or file '{results_dir}' not found.")
        return []

    results = []

    for file_path in csv_files:
        try:
            rel_parts = file_path.relative_to(results_path).parts
        except ValueError:
            rel_parts = file_path.parts

        llm = rel_parts[0] if len(rel_parts) > 0 else "unknown"
        category = rel_parts[1] if len(rel_parts) > 1 else "unknown"
        algorithm = rel_parts[2] if len(rel_parts) > 2 else "unknown"
        scale = file_path.stem.split('_')[-1]

        emissions_values = []
        with open(file_path, mode="r", encoding="utf-8") as f:
            reader = list(csv.DictReader(f))
            for row in reader:
                val = row.get("emissions")
                if val:
                    try:
                        emissions_values.append(float(val))
                    except ValueError:
                        pass

        if not emissions_values:
            continue

        # True mathematical median: averages 5th and 6th values for 10 elements
        median_val = statistics.median(emissions_values)

        results.append({
            "llm": llm,
            "category": category,
            "algorithm": algorithm,
            "scale": scale,
            "median_emissions": median_val
        })

    # Sort output cleanly by category, algorithm, scale, llm
    results.sort(key=lambda x: (x["category"], x["algorithm"], int(x["scale"]) if str(x["scale"]).isdigit() else 0, x["llm"]))

    if output_file:
        fieldnames = ["llm", "category", "algorithm", "scale", "median_emissions"]
        with open(output_file, mode="w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(results)
        print(f"[+] Processed {len(results)} files. True median emissions output saved to: {os.path.abspath(output_file)}")

    return results

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Calculate TRUE median emissions across 10 benchmark runs.")
    parser.add_argument("--results_dir", "-r", default="results", help="Path to results directory")
    parser.add_argument("--output", "-o", default="median_emissions.csv", help="Output CSV file path")
    args = parser.parse_args()

    get_median_emissions(args.results_dir, args.output)
