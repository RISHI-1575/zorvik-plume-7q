# Saarathi Simulator Assumptions Register

Every simulator value must appear here before it is used in a paper result.

| ID | Category | Parameter | Value/range | Unit | Source/measurement | Applies to | Uncertainty | Validation status | Owner |
|---|---|---|---:|---|---|---|---|---|---|
| A-001 | PCU | Passenger car | 1.0 | PCU | Reference class | all scenarios | fixed by definition | pending | TBD |
| A-002 | PCU | Two-wheeler | TBD | PCU | IRC baseline + field calibration | reference corridor | composition-dependent | pending | TBD |
| A-003 | Geometry | Number of signal nodes | TBD | nodes | field/OSM verification | reference corridor | corridor-dependent | pending | TBD |
| A-004 | Behaviour | Lateral resolution | TBD | m | SUMO sublane calibration | reference corridor | calibration parameter | pending | TBD |

## Status values

- `provisional`: convenient initial value, not yet sourced;
- `sourced`: supported by a cited standard/paper but not corridor-specific;
- `measured`: obtained from field observations;
- `calibrated`: fitted using the calibration dataset;
- `validated`: passed the held-out validation gate;
- `rejected`: tested and found unsuitable.

## Rule

No parameter may be described as “Indian” or “Bengaluru” merely because it appears plausible. It must be sourced, measured, calibrated or explicitly labelled provisional.
