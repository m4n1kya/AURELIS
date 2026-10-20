# AURELIS System Architecture

## 1. Design Philosophy

AURELIS is architected around a strict separation between **deterministic quantitative simulation** and **unstructured multimodal perception**:

1. **Deterministic Core (`engine/`)**: All cash-flow projections, reserve boundary checks, currency conversions, and affordability classifications execute deterministically in pure Python. LLMs are never permitted to guess balances or compute arithmetic.
2. **Multimodal Evidence Extraction (`engine/data_processor.py` & `engine/llm_client.py`)**: Unstructured inputs—such as receipt images and natural-language payment notifications—are parsed into typed schema mutations (`amend_amount`, `amend_date`, `cancel`, `confirm`) and cached via SHA-256 content addressing.
3. **Decoupled Presentation (`api/` & `frontend/`)**: The FastAPI service layer wraps the core engine without mutating its internal logic, serving structured JSON trajectories to the Next.js visualization client.

---

## 2. 90-Day Cash-Flow Projection Model

Given a purchase or financing request at date $t_0$, `FinancialState.build_forecast_with_rules(t_0, days=90)` constructs a daily liquidity vector $B = [b_0, b_1, \dots, b_{90}]$ over the horizon $[t_0, t_0 + 90]$:

$$b_k = b_{k-1} + \sum_{e \in E_{\text{scheduled}}(t_k)} \text{sgn}(e) \cdot \text{FX}(e, t_k) + \sum_{r \in R_{\text{inferred}}(t_k)} r_{\text{amount}}$$

### Recurrence Inference Rules
- **Historical Window**: Only `settled` events with $t_{\text{settlement}} \le t_0$ are inspected to infer recurring obligations.
- **Cadence Detection**:
  - **Weekly**: Consecutive settlement intervals $\Delta t \in [6, 8]$ days project forward every $7$ days.
  - **Monthly**: Consecutive settlement intervals $\Delta t \in [28, 31]$ days project forward every $30$ days.
- **Deduplication Invariant**: If an explicit `pending` or `scheduled` event already exists for category $C$ on date $t_k$, the inferred recurrence rule for $C$ on $t_k$ is suppressed to prevent double-counting.

---

## 3. Affordability Evaluation Contract

A candidate payment plan $P = \{(d_1, a_1), \dots, (d_m, a_m)\}$ is considered **safe** if and only if the post-payment daily balance never drops below the user's minimum reserve threshold $M_{\min}$ across the entire 90-day horizon:

$$\forall k \in \{0, \dots, 90\}: \quad b_k - \sum_{d_j \le t_k} a_j \ge M_{\min}$$

---

## 4. API Specification

| Method | Endpoint | Description |
| :--- | :--- | :--- |
| `GET` | `/api/health` | Returns service health and engine mode (`{"status": "ok", "engine": "deterministic"}`). |
| `GET` | `/api/requests` | Lists all available financial evaluation requests with user and amount metadata. |
| `GET` | `/api/analyze/{request_id}` | Executes the 90-day deterministic simulation for `request_id` and returns the decision, daily forecast, chart markers, state events, and evidence audit log. |
| `GET` | `/api/metrics/{request_id}` | Computes standardized financial health indicators (liquidity ratio, emergency fund ratio, margin of safety, discretionary spending ratio, burn rate, runway, DTI). |

---

## 5. Quantitative Health & Liquidity Indicators

To provide deeper context alongside deterministic affordability simulations, AURELIS evaluates key solvency and runway metrics:

- **Liquidity Coverage Ratio**:
  $$\text{LCR} = \frac{\text{Current Available Balance}}{\text{Monthly Obligations}}$$
- **Emergency Reserve Coverage (Months)**:
  $$\text{ERC} = \frac{\text{Current Available Balance}}{\text{Monthly Essential Expenses}}$$
- **Margin of Safety**:
  $$\text{MoS} = \frac{\text{Current Balance} - M_{\min}}{\text{Current Balance}}$$
- **Net Burn Rate**:
  $$\text{BR}_{\text{net}} = \max(0, \text{Monthly Outflows} - \text{Monthly Inflows})$$
- **Cash Runway (Months)**:
  $$\text{Runway} = \begin{cases} \infty & \text{if } \text{BR}_{\text{net}} \le 0 \\ \frac{\text{Liquid Reserves}}{\text{BR}_{\text{net}}} & \text{if } \text{BR}_{\text{net}} > 0 \end{cases}$$

