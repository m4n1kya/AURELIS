# Contributing to AURELIS

Thank you for your interest in contributing to **AURELIS**. We welcome bug fixes, quantitative financial engine improvements, documentation enhancements, and dashboard refinements.

## Development Workflow

1. **Fork & Clone**
   ```bash
   git clone https://github.com/m4n1kya/AURELIS.git
   cd AURELIS
   ```
2. **Install Dependencies**
   ```bash
   make install
   ```
3. **Create a Feature Branch**
   ```bash
   git checkout -b feat/your-feature-name
   ```
4. **Run Tests & Linting**
   Ensure both the Python test suite and the Next.js linter pass with zero errors before opening a pull request:
   ```bash
   make test
   make lint
   ```

## Commit Message Convention

We follow the [Conventional Commits](https://www.conventionalcommits.org/) specification:
- `feat(engine): ...` — New engine capabilities or financial metrics
- `fix(api): ...` — Bug fixes in the FastAPI service layer
- `docs: ...` — Documentation updates
- `test: ...` — Unit or integration test additions
- `chore: ...` — Build, CI, or dependency maintenance

## Architectural Invariants

- **Strict Engine Decoupling**: The `engine/` package must remain pure Python with zero dependencies on FastAPI, Uvicorn, or web frameworks.
- **Deterministic Reproducibility**: Given identical ledger inputs and cached evidence, `Evaluator.evaluate()` must always produce identical output payloads.
