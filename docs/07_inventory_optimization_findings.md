# Inventory Optimization Findings — ABC–XYZ Based Policy Design

This document summarizes the inventory optimization stage of the Demand Forecasting
and Inventory Optimization project. This phase converts forecast outputs into
actionable inventory policies used by supply chain planners.

---

## 1. Objective
The goal of this stage was to:
- Translate demand forecasts into inventory decisions
- Control stockout risk while minimizing excess inventory
- Apply differentiated service levels based on business importance and demand variability

This reflects real-world inventory planning rather than purely academic forecasting.

---

## 2. Input Data
Inventory calculations were based on:
- Weekly demand forecasts (best model per series)
- Forecast error statistics from a time-based holdout
- Store and product family attributes
- Lead time and review period assumptions

All calculations were performed at the **Store × Family** level.

---

## 3. ABC Classification (Value-Based Segmentation)
Products were classified using total sales over the last 52 weeks:

- **A items**: High revenue contribution
- **B items**: Medium revenue contribution
- **C items**: Low revenue contribution

This segmentation answers:
> “Which items matter most financially?”

ABC classification ensures inventory investment is focused where business impact is highest.

---

## 4. XYZ Classification (Variability-Based Segmentation)
Demand variability was measured using the coefficient of variation (CV):

- **X**: Stable, predictable demand
- **Y**: Moderate variability
- **Z**: Highly volatile or intermittent demand

This segmentation answers:
> “How predictable is the demand?”

XYZ classification highlights operational risk and forecasting uncertainty.

---

## 5. Combined ABC–XYZ Strategy
ABC and XYZ classifications were combined to form actionable segments such as:

- **AX**: High value, stable demand
- **AY / AZ**: High value, increasing risk
- **CX / CZ**: Low value, varying predictability

This combination allows inventory policies to reflect both financial importance and demand risk.

---

## 6. Service Level Assignment
Differentiated service levels were assigned by ABC–XYZ class:

- **AX** → Very high service level (e.g., 98%)
- **BX / AY** → High service level (e.g., 95%)
- **CY / CZ** → Lower service level (e.g., 90%)

This avoids a “one-size-fits-all” approach and aligns inventory investment with business priorities.

---

## 7. Forecast Uncertainty and Safety Stock
Safety stock was calculated using forecast error (not raw demand volatility):

Safety Stock = z × σ × √(Lead Time)

Where:
- z = service level factor
- σ = standard deviation of forecast errors
- Lead Time = replenishment lead time (weeks)

Using forecast error ensures safety stock reflects actual prediction risk.

---

## 8. Reorder Point Calculation
Reorder points were computed as:

Reorder Point = (Mean Demand × Lead Time) + Safety Stock

This determines when replenishment orders should be placed to meet service targets.

---

## 9. Key Business Insights
- High-value, stable items justify higher safety stock protection
- Volatile items require careful risk trade-offs rather than blanket coverage
- Forecast bias directly impacts inventory outcomes
- Differentiated policies significantly improve inventory efficiency

---

## 10. Practical Use by Planners
The final output can be used to:
- Set store-level reorder points
- Compare service level scenarios (90% vs 95% vs 98%)
- Support inventory review meetings
- Feed dashboards for ongoing monitoring

This completes the end-to-end analytics workflow from data to decision.
