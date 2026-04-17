# Frontend Specification
## Incheon Port Cut-off Miss Risk Radar

## 1. Pages

### 1.1 Home / Input page

Components:

- origin input (zone select)
- terminal select
- cut-off datetime input
- conservative mode toggle
- submit button

### 1.2 Result page

Components:

- probability card
- risk score card
- latest safe dispatch time card
- short verdict banner
- data freshness note

### 1.3 Reason analysis section

Components:

- contribution bar chart
- reason summary cards

### 1.4 Simulation section

Components:

- scenario comparison table
- probability line/bar chart

## 2. UX priorities

- show the answer fast
- put the latest safe dispatch time above the fold
- avoid dense logistics jargon
- show degraded data warnings clearly

## 3. UI states

### Loading

- skeleton cards
- loading banner

### Success

- main result cards
- reasons
- simulation

### Partial data

- result shown with warning badge

### Failure

- friendly retry message

## 4. Tech stack

- React 19
- TypeScript
- Vite 8
- Tailwind CSS v4
- Recharts
- React Router v7
