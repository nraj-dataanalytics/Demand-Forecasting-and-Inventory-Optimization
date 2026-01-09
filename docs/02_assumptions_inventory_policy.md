# Inventory Policy and Modeling Assumptions

This project uses a consistent set of assumptions across forecasting, inventory optimization, and scenario analysis. These assumptions are intentionally simple and transparent, reflecting how early-stage planning models are often built before being refined with operational data.

---

## Planning cadence
- Demand is reviewed on a **weekly** basis
- Forecast horizon ranges from **8 to 12 weeks**, aligned with typical retail planning cycles

---

## Service level targets
Service levels vary by product importance:
- A-items: 95%
- B-items: 90%
- C-items: 85%

These targets reflect a trade-off between customer service and inventory cost.

---

## Lead time assumptions
- Baseline lead time: **2 weeks**
- Stress scenario: **30% increase in lead time**

Lead time variability is tested through scenario simulations rather than assumed to be constant.

---

## Cost assumptions (modeled)
- Annual holding cost rate: **25%**
- Stockout cost proxy: estimated lost contribution margin per unit

These costs are modeled to compare relative trade-offs, not to estimate exact financial impact.

---

## Inventory policy logic
- Safety stock is calculated using service-level z-scores and demand variability
- Reorder Point (ROP) = Expected demand during lead time + safety stock

All inventory policies are derived from forecast outputs and are evaluated under multiple scenarios.
