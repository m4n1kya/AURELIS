# Changelog

All notable changes to **AURELIS** are documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/), and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.3.0] - 2026-10-20

### Added
- Personal liquidity and cash runway metrics in `engine/financial_metrics.py` (`calculate_net_burn_rate`, `calculate_cash_runway_months`, `calculate_debt_service_coverage_ratio`, `calculate_discretionary_spending_ratio`, `calculate_rule_of_72`).
- Public package export of core quantitative financial metrics directly from `engine/__init__.py`.
- REST API endpoint `GET /api/metrics/{request_id}` providing on-demand financial health, reserve buffer, and runway diagnostics.
- Expanded test suites in `tests/test_financial_metrics.py` and `tests/test_api.py` validating metrics logic and API contracts.

### Changed
- Aligned `AurelisService.analyze` response schema with frontend `Dashboard.tsx` expectations by providing `state.events` and `timeline` data points.
- Expanded technical architecture documentation (`docs/ARCHITECTURE.md`) with mathematical specifications for runway, burn rate, and health indicators.

## [1.2.0] - 2026-10-13

### Added
- Quantitative financial metrics library (`engine/financial_metrics.py`) covering liquidity, solvency, capital efficiency, and distress indicators (Altman Z-Score, DuPont ROE, IRR, MIRR, NPV).
- Comprehensive technical architecture documentation (`docs/ARCHITECTURE.md`).
- Standardized Python packaging metadata and tool configuration via `pyproject.toml`.

### Changed
- Consolidated container build specifications under `docker/` with multi-service orchestration in `docker-compose.yml`.
- Upgraded GitHub Actions CI pipelines to Python 3.11 and Node.js 20 with dependency caching.

## [1.1.0] - 2026-09-20

### Added
- FastAPI service bridge (`api/main.py` and `api/aurelis_service.py`) with request latency telemetry (`X-Process-Time`) and Pydantic health contracts.
- Automated unit and integration test suites (`tests/test_engine.py`, `tests/test_api.py`, `tests/test_formatting.py`).

## [1.0.0] - 2026-09-12

### Added
- Deterministic 90-day cash-flow projection engine (`engine/finance.py`, `engine/evaluator.py`).
- Multi-currency spot rate normalization (`engine/exchange_rates.py`).
- Multimodal receipt and message evidence processor (`engine/data_processor.py`, `engine/llm_client.py`).
- Next.js 16 real-time financial intelligence dashboard (`frontend/`).