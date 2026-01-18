from __future__ import annotations
import argparse
import os
from dataclasses import dataclass
from typing import Tuple
import numpy as np
import pandas as pd
from scipy.stats import norm


def ensure_dir(path: str) -> None:
    os.makedirs(path, exist_ok=True)


def write_csv(df: pd.DataFrame, path: str) -> None:
    os.makedirs(os.path.dirname(path), exist_ok=True)
    df.to_csv(path, index=False)


def z_from_service_level(sl: float) -> float:
    sl = float(np.clip(sl, 0.50, 0.9999))
    return float(norm.ppf(sl))


@dataclass
class PolicyConfig:
    date_col: str
    sku_col: str
    demand_col: str
    service_col: str = "service_level_target"
    review_period: int = 1
    lead_time: int = 3
    order_up_to_periods: int = 12
    seed_multiplier: float = 1.0


def compute_rop_S(demand: np.ndarray, sl: float, lt: int, h: int) -> Tuple[float, float, float]:
    x = np.clip(demand.astype(float), 0, None)
    mu = float(x.mean())
    sigma = float(x.std(ddof=0))
    z = z_from_service_level(sl)

    rop = mu * lt + z * sigma * np.sqrt(lt)
    S = mu * (lt + h) + z * sigma * np.sqrt(lt + h)
    return rop, S, mu


def simulate_one(df_sku: pd.DataFrame, cfg: PolicyConfig) -> pd.DataFrame:
    df_sku = df_sku.sort_values(cfg.date_col).reset_index(drop=True).copy()
    sku = str(df_sku[cfg.sku_col].iloc[0])

    demand = pd.to_numeric(df_sku[cfg.demand_col], errors="coerce").fillna(0.0).to_numpy()
    demand = np.clip(demand.astype(float), 0, None)

    if cfg.service_col in df_sku.columns and df_sku[cfg.service_col].notna().any():
        sl = float(df_sku[cfg.service_col].dropna().iloc[0])
    else:
        sl = 0.95

    rop, S, mu = compute_rop_S(demand, sl, cfg.lead_time, cfg.order_up_to_periods)

    # seed inventory
    on_hand = cfg.seed_multiplier * mu * cfg.lead_time
    backlog = 0.0
    pipeline = []  # (arrival_t, qty)
    rows = []

    n = len(df_sku)

    for t in range(n):
        dt = df_sku.loc[t, cfg.date_col]
        d = float(demand[t])

        # receive
        arrivals = sum(q for (arr_t, q) in pipeline if arr_t == t)
        pipeline = [(arr_t, q) for (arr_t, q) in pipeline if arr_t != t]
        on_hand += arrivals

        # ship demand first
        shipped = min(on_hand, d)
        on_hand -= shipped
        unmet = d - shipped
        backlog += unmet

        on_order = float(sum(q for _, q in pipeline))
        inv_pos = on_hand + on_order - backlog

        # order decision
        order_qty = 0.0
        order_placed = 0
        if (t % cfg.review_period) == 0 and inv_pos <= rop:
            order_qty = max(0.0, float(S - inv_pos))
            order_placed = 1
            arr = t + cfg.lead_time
            if arr < n:
                pipeline.append((arr, order_qty))

        rows.append({
            cfg.date_col: dt,
            "sku": sku,
            "demand": d,
            "shipped": shipped,
            "unmet": unmet,
            "on_hand": on_hand,
            "backlog": backlog,
            "arrivals": float(arrivals),
            "on_order": on_order,
            "inventory_position": inv_pos,
            "rop": rop,
            "S": S,
            "service_level_target": sl,
            "order_qty": order_qty,
            "order_placed": order_placed,
        })

    return pd.DataFrame(rows)


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("--input", required=True)
    p.add_argument("--output-dir", required=True)
    p.add_argument("--date-col", default="week_start")
    p.add_argument("--sku-col", default="family")
    p.add_argument("--demand-col", default="weekly_sales")
    p.add_argument("--service-col", default="service_level_target")
    p.add_argument("--review-period", type=int, default=1)
    p.add_argument("--lead-time", type=int, default=3)
    p.add_argument("--order-up-to-periods", type=int, default=12)
    p.add_argument("--seed-multiplier", type=float, default=1.0)
    args = p.parse_args()

    df = pd.read_csv(args.input)
    df[args.date_col] = pd.to_datetime(df[args.date_col])
    df[args.demand_col] = pd.to_numeric(df[args.demand_col], errors="coerce").fillna(0.0)

    cfg = PolicyConfig(
        date_col=args.date_col,
        sku_col=args.sku_col,
        demand_col=args.demand_col,
        service_col=args.service_col,
        review_period=args.review_period,
        lead_time=args.lead_time,
        order_up_to_periods=args.order_up_to_periods,
        seed_multiplier=args.seed_multiplier,
    )

    sims = []
    for _, g in df.groupby(cfg.sku_col, sort=False):
        sims.append(simulate_one(g, cfg))

    sim_all = pd.concat(sims, ignore_index=True)

    overall = pd.DataFrame({
        "total_demand": [sim_all["demand"].sum()],
        "total_shipped": [sim_all["shipped"].sum()],
        "fill_rate": [sim_all["shipped"].sum() / (sim_all["demand"].sum() + 1e-9)],
        "total_unmet": [sim_all["unmet"].sum()],
    })

    kpi_by_sku = sim_all.groupby("sku", as_index=False).agg(
        total_demand=("demand", "sum"),
        total_shipped=("shipped", "sum"),
        total_unmet=("unmet", "sum"),
        stockout_periods=("unmet", lambda x: int((x > 0).sum())),
        avg_on_hand=("on_hand", "mean"),
        orders=("order_placed", "sum"),
    )
    kpi_by_sku["fill_rate"] = kpi_by_sku["total_shipped"] / (kpi_by_sku["total_demand"] + 1e-9)

    ensure_dir(args.output_dir)
    write_csv(sim_all, os.path.join(args.output_dir, "sim_transactions.csv"))
    write_csv(kpi_by_sku, os.path.join(args.output_dir, "sim_kpi_by_sku.csv"))
    write_csv(overall, os.path.join(args.output_dir, "sim_kpi_overall.csv"))

    print("✅ Policy simulation complete.")
    print(overall.to_string(index=False))


if __name__ == "__main__":
    main()
