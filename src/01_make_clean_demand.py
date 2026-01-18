from __future__ import annotations
import argparse
import os
import pandas as pd


def ensure_dir(path: str) -> None:
    os.makedirs(path, exist_ok=True)


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("--input", required=True, help="Path to weekly_demand.csv")
    p.add_argument("--output", required=True, help="Path to write weekly_demand_clean.csv")
    p.add_argument("--date-col", default="week_start")
    p.add_argument("--sku-col", default="family")
    p.add_argument("--demand-col", default="weekly_sales")
    args = p.parse_args()

    df = pd.read_csv(args.input)

    # Parse + enforce numeric demand
    df[args.date_col] = pd.to_datetime(df[args.date_col])
    df[args.demand_col] = pd.to_numeric(df[args.demand_col], errors="coerce").fillna(0.0)

    key = [args.sku_col, args.date_col]

    # Aggregate duplicates safely
    agg = {args.demand_col: "sum"}
    for col in df.columns:
        if col in key or col == args.demand_col:
            continue
        if pd.api.types.is_numeric_dtype(df[col]):
            agg[col] = "mean"
        else:
            agg[col] = "first"

    df_clean = (
        df.groupby(key, as_index=False)
          .agg(agg)
          .sort_values(key)
          .reset_index(drop=True)
    )

    ensure_dir(os.path.dirname(args.output))
    df_clean.to_csv(args.output, index=False)

    print("✅ Clean demand file created.")
    print("Input rows:", len(df), "| Output rows:", len(df_clean))
    print("Demand sum:", float(df_clean[args.demand_col].sum()))
    print("Head demand:", df_clean[args.demand_col].head(10).tolist())


if __name__ == "__main__":
    main()
