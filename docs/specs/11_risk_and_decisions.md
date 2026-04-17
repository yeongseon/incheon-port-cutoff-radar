# Risks and Key Decisions
## Incheon Port Cut-off Miss Risk Radar

## 1. Product decisions

### Decision 1: Use a rule-based engine first

Reason:

- easier to explain
- faster to implement
- better for MVP credibility

### Decision 2: Support only Incheon Port in v1

Reason:

- stronger scope control
- better demo clarity
- better source alignment

### Decision 3: Prioritize latest safe dispatch time

Reason:

- actionable output matters more than raw metrics

## 2. Risks

### Risk 1: Public data may not capture all real-world operational variables

**Mitigation:** position product as decision support, not certainty engine

### Risk 2: Existing status services may reduce perceived novelty

**Mitigation:** emphasize per-job decision support and recommendation layer

### Risk 3: External API quality or availability may vary

**Mitigation:** cache strategy, degraded mode, freshness warnings

### Risk 4: Traffic estimation may be approximate in MVP

**Mitigation:** clearly label assumptions, keep route logic simple at first
