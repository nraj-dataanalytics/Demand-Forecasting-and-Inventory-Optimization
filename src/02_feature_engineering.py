from __future__ import annotations
import argparse
import os
import numpy as np
import pandas as pd


def ensure_dir(path: str) -> None:
    os.makedirs(path, exist_ok=True)


def add_time_features(df: pd.DataFrame, date_col: str) -> pd.DataFrame:
    df = df.copy()
    df["year"] = df[date_col].dt.year
    df["month"] = df[date_col].dt.month
    df["quarter"] = df[date_col].dt.quarter
    df["weekofyear"] = df[date_col].dt.isocalendar().week.astype(int)
    return df


def add_lags_rolls(df: pd.DataFrame, sku_col: str, demand_col: str) -> pd.DataFrame:
    df = df.copy()
    df = df.sort_values([sku_col, "week_start"])

    for lag in [1, 2, 4, 8]:
        df[f"lag_{lag}"] = df.groupby(sku_col)[demand_col].shift(lag)

    # rolling windows
    for w in [4, 8, 12]:
        df[f"roll_mean_{w}"] = df.groupby(sku_col)[demand_col].shift(1).rolling(w).mean().reset_index(level=0, drop=True)
        df[f"roll_std_{w}"] = df.groupby(sku_col)[demand_col].shift(1).rolling(w).std().reset_index(level=0, drop=True)

    # volatility proxy
    df["cv_8"] = df["roll_std_8"] / (df["roll_mean_8"] + 1e-9)

    return df


def add_abc(df: pd.DataFrame, sku_col: str, demand_col: str) -> pd.DataFrame:
    df = df.copy()
    totals = df.groupby(sku_col)[demand_col].sum().sort_values(ascending=False)
    share = totals / (totals.sum() + 1e-9)
    cum = share.cumsum()

    def cls(x):
        if x <= 0.80:
            return "A"
        elif x <= 0.95:
            return "B"
        else:
            return "C"

    abc_map = cum.apply(cls).to_dict()
    df["abc_class"] = df[sku_col].map(abc_map)

    # simple service target mapping
    svc = {"A": 0.98, "B": 0.95, "C": 0.90}
    df["service_level_target"] = df["abc_class"].map(svc)

    return df


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("--input", required=True)
    p.add_argument("--output", required=True)
    p.add_argument("--date-col", default="week_start")
    p.add_argument("--sku-col", default="family")
    p.add_argument("--demand-col", default="weekly_sales")
    args = p.parse_args()

    df = pd.read_csv(args.input)
    df[args.date_col] = pd.to_datetime(df[args.date_col])
    df[args.demand_col] = pd.to_numeric(df[args.demand_col], errors="coerce").fillna(0.0)

    # IMPORTANT: do NOT reindex here. We trust the cleaned file’s grain.
    df = add_time_features(df, args.date_col)
    df = add_lags_rolls(df, args.sku_col, args.demand_col)
    df = add_abc(df, args.sku_col, args.demand_col)

    ensure_dir(os.path.dirname(args.output))
    df.to_csv(args.output, index=False)

    print("✅ Feature engineering complete.")
    print("Rows:", len(df), "| Cols:", df.shape[1])
    print("Demand sum:", float(df[args.demand_col].sum()))
    print("Sample columns:", df.columns[:20].tolist())


if __name__ == "__main__":
    main()
