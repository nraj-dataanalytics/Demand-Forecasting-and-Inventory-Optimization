# EDA Findings — Store Sales Demand (Weekly Planning)

This document summarizes the key insights from exploratory data analysis (EDA) conducted on the Store Sales dataset.
The goal of EDA was to understand demand behavior and make informed decisions for forecasting and inventory optimization.

---

## 1. Data Coverage & Scale
- Time span: January 2013 to August 2017 (~4.5 years)
- Stores: 54
- Product families: 33
- Store × Family combinations: 1,782
- Final planning grain: **Store × Family × Week**

Weekly aggregation was selected to align with real-world inventory planning cycles.

---

## 2. Demand Behavior
- Daily sales data is highly right-skewed with frequent zero-sales days.
- A small proportion of observations account for very high demand spikes.
- Aggregating to weekly demand significantly reduces noise and stabilizes the signal.
- Weekly demand retains meaningful variation while improving forecastability.

---

## 3. Promotions
- Promotion activity varies substantially across stores and product families.
- Promotion intensity is uneven over time, with clustering around peak demand periods.
- Promotion signals were preserved at the weekly level using:
  - Total promotion days per week
  - Average promotion intensity per week

These features will later support demand explanation and scenario analysis.

---

## 4. Data Quality & Completeness
- No duplicate records detected in any dataset.
- No material missing values in core demand or store attributes.
- Approximately **97.5%** of weekly observations represent complete 7-day weeks.
- Partial weeks occur mainly at the beginning and end of the time series and will be retained.

Overall data quality is high and suitable for forecasting and inventory modeling.

---

## 5. Modeling Implications
- Weekly forecasting is preferred over daily forecasting due to reduced sparsity and noise.
- Demand skewness suggests that robust accuracy metrics (e.g., WAPE, bias) are required.
- Multiple baseline and seasonal models should be evaluated rather than relying on a single approach.
- Promotion effects and demand volatility must be considered in downstream inventory decisions.

These findings directly inform the forecasting strategies implemented in subsequent notebooks.
