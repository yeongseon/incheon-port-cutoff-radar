# Product Requirements Document
## Incheon Port Cut-off Miss Risk Radar

## 1. Product goal

Build a web-based operational decision support tool that estimates whether a container inbound job can meet terminal cut-off at Incheon Port.

## 2. Users

### Primary users

- freight forwarder operators
- transport dispatch managers
- export operation staff

### User intent

Users want quick answers to:

- Can I still make the cut-off?
- How risky is it?
- When is the latest safe dispatch time?

## 3. Core user story

As a logistics operator,
I want to input origin, destination terminal, and cut-off time,
so that I can know whether dispatching now is safe.

## 4. MVP scope

### Included

- input form for origin / terminal / cut-off
- real-time or near-real-time public data ingestion
- risk score calculation
- latest safe dispatch time recommendation
- reason summary
- dispatch-time simulation

### Excluded

- machine learning prediction model
- enterprise system integration
- SMS / push notifications
- multi-port support
- detailed weather/ocean intelligence engine
- native mobile app

## 5. Functional requirements

### FR-1 Job input

The system shall allow users to input:

- origin
- destination terminal
- cut-off datetime

### FR-2 Data aggregation

The system shall fetch and normalize:

- terminal congestion data
- terminal information data
- vehicle entry data
- traffic data

### FR-3 Risk evaluation

The system shall calculate:

- estimated total lead time
- on-time probability
- cut-off miss risk score

### FR-4 Recommendation

The system shall recommend:

- latest safe dispatch time

### FR-5 Explainability

The system shall provide:

- top reason factors
- brief textual interpretation

### FR-6 Simulation

The system shall allow the user to compare results for:

- current dispatch
- 15 minutes earlier
- 30 minutes earlier
- 60 minutes earlier

## 6. Non-functional requirements

### NFR-1 Response speed

Results should be returned within a few seconds when cached data is available.

### NFR-2 Reliability

External API failures should not crash the user flow.
Fallback and cache logic are required.

### NFR-3 Transparency

The result must include input timestamp and data freshness indication.

### NFR-4 Simplicity

The MVP must stay narrow and easy to demo.

## 7. Key UX principle

The user must understand the answer without reading a long report.

The result page must make these visible first:

1. on-time probability
2. miss risk level
3. latest safe dispatch time

## 8. MVP success metrics

- data ingestion from core APIs works reliably
- one inbound scenario can be processed end-to-end
- latest safe dispatch time is shown correctly
- simulation view works
- demo flow can be explained in under 2 minutes
