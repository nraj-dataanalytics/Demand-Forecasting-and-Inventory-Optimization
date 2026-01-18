# Data Design and Modeling Decisions

This document records the core data design decisions for the Demand Forecasting and Inventory Optimization capstone.
These decisions are intentionally locked early to avoid rework and inconsistency during analysis.

---

## Purpose of this document
In real analytics projects, confusion often arises when teams change the data grain, forecast horizon, or evaluation logic midway.
This file exists to clearly document and lock those decisions before any modeling begins.

---

## Core Planning Grain
- **Primary grain:** Store × SKU × Week

Reason:
Weekly aggregation aligns with how inventory replenishment and safety stock decisions are typically made in retail.
Daily data will be aggregated to weekly demand before forecasting.

---

## Forecast Horizon
- **Forecast window:** 8 to 12 weeks ahead

Reason:
This horizon reflects short- to medium-term planning cycles where replenishment and inventory policies are actively adjusted.

---

## Train / Test Strategy
- Time-based split (no random sampling)
- Most recent periods reserved for test evaluation
- Models evaluated only on future, unseen data

Reason:
Time-series forecasting must respect temporal order to avoid data leakage.

---

## Evaluation Metrics
**Primary Metric**
- WAPE (Weighted Absolute Percentage Error)

**Secondary Metrics**
- MAPE
- Forecast Bias (Mean Error)

Reason:
WAPE is more stable for aggregated retail demand and aligns better with business interpretation.
Bias is tracked to identify systematic over- or under-forecasting.

---

## Inventory Modeling Alignment
- Forecast outputs will be used as inputs to:
  - Safety stock calculation
  - Reorder point (ROP) logic
- Inventory policies will be evaluated under multiple scenarios:
  - Demand volatility
  - Lead-time increase
  - Service-level changes

---

## Relationship to SQL Layer
- BigQuery (theLook dataset) will be used for:
  - Enterprise-level KPI trends
  - Demand shift context
- Forecasting dataset (Store Sales) will be used for:
  - Model training and evaluation
  - Inventory optimization logic

These datasets will not be merged at the row level.
They serve complementary but separate analytical purposes.
