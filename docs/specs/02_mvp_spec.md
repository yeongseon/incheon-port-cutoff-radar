# MVP Specification
## Incheon Port Cut-off Miss Risk Radar

## 1. MVP objective

Prove that public operational data can be transformed into a per-job dispatch decision.

## 2. MVP statement

A user inputs a single inbound job and receives:

- on-time arrival probability
- miss risk score
- latest safe dispatch time
- reason breakdown
- simple dispatch-time simulation

## 3. Inputs

### Required inputs

- origin
- destination terminal
- cut-off datetime

### Optional inputs

- conservative mode on/off
- container type placeholder
- manual safety buffer override

## 4. Outputs

### Primary outputs

- on-time probability
- risk score (0-100)
- risk label (Low / Medium / High)
- latest safe dispatch time

### Secondary outputs

- reason contribution list
- scenario comparison table

## 5. Core formula structure

Estimated total lead time =

- road travel time
- terminal waiting time
- gate entry adjustment
- safety buffer

## 6. MVP rules

### Risk score buckets

- 0-34: Low
- 35-69: Medium
- 70-100: High

### On-time probability rough mapping

A deterministic score can first be mapped into a probability band.

### Latest safe dispatch time

```
Latest safe dispatch time =
  cut-off time - estimated total lead time - required confidence buffer
```

## 7. MVP assumptions

- current public data is enough for a first operational estimate
- the first model can be rule-based
- explainability is more important than predictive sophistication
- terminal-level precision is enough for MVP

## 8. MVP constraints

- no guarantee of exact real-world arrival
- no enterprise SLA
- no dynamic route engine in v1
- no deep weather/ocean model in v1

## 9. Demo scenario

Example:

- Origin: Songdo warehouse
- Terminal: selected Incheon terminal
- Cut-off: 17:00

Result:

- on-time probability: 41%
- miss risk: High
- latest safe dispatch time: 14:20
- top reasons: traffic, terminal congestion, entry flow
