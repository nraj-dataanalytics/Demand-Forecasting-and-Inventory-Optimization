# Forecasting Findings — Weekly Demand (Baseline & Comparative Models)

This document summarizes the results and insights from the forecasting stage of the
Demand Forecasting and Inventory Optimization project. The goal of this phase was to
identify reliable forecasting approaches and understand their implications for inventory decisions.

---

## 1. Forecasting Setup
- Planning grain: **Store × Family × Week**
- Evaluation method: **Time-based holdout**
- Holdout window: **Last 12 weeks**
- Series evaluated: **Top 30 Store–Family combinations by total sales**
- Primary metrics:
  - **WAPE (Weighted Absolute Percentage Error)**
  - **Forecast Bias (over / under forecasting)**
  - MAPE (supporting metric)

This setup mirrors how forecasts are evaluated in real supply chain planning teams.

---

## 2. Models Evaluated
The following models were benchmarked for each series:

- **Naive** (last observed value)
- **Seasonal Naive** (same week last year)
- **Moving Average (8-week)**
- **Exponential Smoothing (ETS)**
- **SARIMAX with promotion variables**

All advanced models were compared against simple baselines to ensure added complexity
provided real value.

---

## 3. Overall Model Performance (Leaderboard Insight)
- Simple baseline models (Naive, Moving Average) performed **as well as or better**
  than more complex models on average.
- Seasonal Naive captured seasonality but did not consistently outperform simpler baselines.
- ETS and SARIMAX struggled on highly intermittent and volatile demand patterns.

Key takeaway:
> **Complex models did not reliably outperform strong baselines for this dataset.**

This highlights the importance of benchmarking and avoiding unnecessary model complexity.

---

## 4. Forecast Bias Analysis
- Bias was explicitly measured to identify systematic over- or under-forecasting.
- Some models showed positive bias (over-forecasting risk → excess inventory).
- Others showed negative bias (under-forecasting risk → stockouts).

Bias tracking proved critical for downstream inventory policy decisions.

---

## 5. Promotion Signal Findings
- Promotion variables were included in SARIMAX models.
- In aggregate, promotion features did not materially improve forecast accuracy.
- Likely reasons:
  - Promotion impact varies by product family and store
  - Future promotion schedules are often uncertain
  - Simple global structures cannot capture heterogeneous promo effects

This informed a cautious approach to promotion-driven forecasting in inventory planning.

---

## 6. Series-Level Model Selection
- Rather than choosing a single global model, the **best-performing model was selected per series**
  based on WAPE.
- This approach reflects real-world practice, where different items behave differently.
- Best model choices were carried forward into inventory optimization.

---

## 7. Business Implications
- Strong baselines are difficult to beat and often sufficient for planning.
- Forecast accuracy must be interpreted alongside **bias**, not in isolation.
- Forecast reliability directly affects safety stock and reorder point calculations.

These findings directly informed the inventory optimization strategies implemented next.
