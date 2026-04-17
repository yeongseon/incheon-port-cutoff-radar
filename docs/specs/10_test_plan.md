# Test Plan
## Incheon Port Cut-off Miss Risk Radar

## 1. Test categories

### 1.1 Unit tests

- score calculation
- latest safe dispatch calculation
- reason attribution
- normalization functions

### 1.2 Integration tests

- external client adapters
- cache + DB interactions
- API endpoint responses

### 1.3 End-to-end tests

- submit job
- receive result
- open simulation
- verify displayed values

## 2. Must-test scenarios

### Scenario A: Low congestion + good traffic

Expected:

- low risk
- high probability
- later safe dispatch time

### Scenario B: High congestion + bad traffic

Expected:

- high risk
- lower probability
- earlier safe dispatch time

### Scenario C: One source unavailable

Expected:

- partial result or clear warning
- no crash

## 3. Acceptance criteria

- all core flows pass
- deterministic calculations are reproducible
- partial-source failure is handled gracefully

## 4. Current test results

| Suite | Tests | Status |
|-------|-------|--------|
| Unit - Risk Engine | 23 | ✅ Pass |
| Unit - Normalizers | 13 | ✅ Pass |
| Integration - API | 10 | ✅ Pass |
| **Total** | **46** | **✅ All Pass** |
