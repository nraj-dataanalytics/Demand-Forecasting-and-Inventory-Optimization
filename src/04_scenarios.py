from __future__ import annotations
import argparse
import os
import pandas as pd
import subprocess
import sys


def run(cmd: str):
    print(f"\n▶ Running:\n{cmd}")
    result = subprocess.run(cmd, shell=True)
    if result.returncode != 0:
        sys.exit("❌ Scenario failed")


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--input", required=True)
    p.add_argument("--date-col", default="week_start")
    p.add_argument("--sku-col", default="family")
    p.add_argument("--demand-col", default="weekly_sales")
    p.add_argument("--out-dir", default="reports/scenarios")
    args = p.parse_args()

    py = ".\\.venv\\Scripts\\python.exe"
    base_out = os.path.join(args.out_dir, "baseline")
    surge_out = os.path.join(args.out_dir, "demand_up_20pct")
    lead_out = os.path.join(args.out_dir, "lead_time_6")

    os.makedirs(args.out_dir, exist_ok=True)

    # 1️⃣ Baseline
    run(
        f'{py} src/03_policy_simulation.py '
        f'--input {args.input} '
        f'--output-dir {base_out} '
        f'--date-col {args.date_col} '
        f'--sku-col {args.sku_col} '
        f'--demand-col {args.demand_col} '
        f'--lead-time 3 --order-up-to-periods 12'
    )

    # 2️⃣ Demand surge (+20%)
    df = pd.read_csv(args.input)
    df[args.demand_col] = df[args.demand_col] * 1.2
    surge_input = os.path.join(args.out_dir, "tmp_demand_up.csv")
    df.to_csv(surge_input, index=False)

    run(
        f'{py} src/03_policy_simulation.py '
        f'--input {surge_input} '
        f'--output-dir {surge_out} '
        f'--date-col {args.date_col} '
        f'--sku-col {args.sku_col} '
        f'--demand-col {args.demand_col} '
        f'--lead-time 3 --order-up-to-periods 12'
    )

    # 3️⃣ Longer lead time
    run(
        f'{py} src/03_policy_simulation.py '
        f'--input {args.input} '
        f'--output-dir {lead_out} '
        f'--date-col {args.date_col} '
        f'--sku-col {args.sku_col} '
        f'--demand-col {args.demand_col} '
        f'--lead-time 6 --order-up-to-periods 12'
    )

    # Collect comparison
    def load_kpi(path):
        return pd.read_csv(os.path.join(path, "sim_kpi_overall.csv"))

    comp = pd.concat(
        [
            load_kpi(base_out).assign(scenario="baseline"),
            load_kpi(surge_out).assign(scenario="demand_up_20pct"),
            load_kpi(lead_out).assign(scenario="lead_time_6"),
        ],
        ignore_index=True
    )

    comp.to_csv(os.path.join(args.out_dir, "scenario_comparison.csv"), index=False)
    print("\n✅ Scenarios complete. Comparison:")
    print(comp)


if __name__ == "__main__":
    main()
