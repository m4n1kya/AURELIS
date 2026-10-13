## Summary

Briefly describe the changes introduced in this pull request and the motivation behind them.

## Type of Change

- [ ] `feat`: New capability or quantitative metric
- [ ] `fix`: Bug fix in engine, API, or frontend
- [ ] `refactor`: Internal code restructuring without behavioral change
- [ ] `docs`: Documentation or architecture specification update
- [ ] `test`: Addition or update of automated tests

## Verification Checklist

- [ ] `pytest tests/ -v` passes locally with zero failures
- [ ] `cd frontend && npm run lint && npm run build` succeeds with zero warnings/errors
- [ ] Core `engine/` remains completely independent of web framework dependencies