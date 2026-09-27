# Ziva Incident Analyser

#### Video Demo: https://youtu.be/GkYPM9pEPvY

## Description

Ziva Incident Analyser is a command-line Python program that reviews a CSV timeline of robot telemetry events and highlights simple safety-relevant patterns around a collision. It is a small, deterministic prototype inspired by the incident-investigation side of autonomous mobile robotics.

The program is designed around a fictional warehouse robot incident. A robot may produce events from multiple sources, such as LiDAR, perception software, a motion controller, and a safety system. Those events are stored in a CSV file, but the rows may not always be arranged chronologically. Ziva Incident Analyser reads the events, validates the data, converts timestamps into Python `datetime` values, sorts the full timeline, prints the evidence in order, and reports findings based on three predefined rules.

Run the program with:

```bash
python3 project.py sample_incident.csv
```

The input CSV must contain these columns:

```text
timestamp,source,event_type,details
```

The included `sample_incident.csv` represents a short warehouse incident timeline. It contains a sensor scan, an obstacle detection, a delayed brake command, and a collision.

## Incident Rules

The analyser deliberately uses deterministic rules instead of machine learning or an LLM. This makes every finding easy to inspect and explain.

First, it checks for stale sensor data. If the latest `sensor_scan` before a `collision` happened more than two seconds earlier, the program reports that sensor data was stale before the collision. This does not prove that a sensor failed; it only identifies that the newest recorded scan was old at the time of the collision.

Second, it checks for delayed braking. If a `brake_command` occurs more than two seconds after an `obstacle_detected` event, the program reports delayed braking. The analyser remembers the most recent obstacle detection and compares its timestamp with the next brake command.

Third, it checks for a missing response. If the program sees an obstacle detection followed by a collision without a brake command in between, it reports that no brake response was recorded before the collision.

The output separates the raw evidence timeline from the incident findings. This is intentional: the timeline shows what was recorded, while the findings show which deterministic conditions were met. The program does not claim to determine a confirmed root cause. A real robotics investigation would require more context, such as localization data, planner state, actuator feedback, hardware health, ROS bag recordings, and human review.

## Validation

The program handles several invalid-input cases with clear error messages. It requires exactly one CSV file path, reports when the file cannot be found, checks that the required CSV columns are present, and identifies the row number of an invalid timestamp. Timestamps are expected to use ISO 8601 format, such as:

```text
2026-09-27T10:00:06
```

## Files

- `project.py` contains the command-line program. It loads and validates the CSV data, parses timestamps, sorts events, prints the timeline, applies the three incident rules, and prints the report.
- `test_project.py` contains pytest tests for the stale-sensor, delayed-braking, and missing-response checks. Each rule is tested with both a triggering case and a non-triggering case.
- `sample_incident.csv` is a valid example incident timeline for demonstrating the program.
- `PRD.md` documents the original product requirements and scope.
- `ROADMAP.md` records the project milestones and development plan.

## Testing

Run the tests with:

```bash
pytest test_project.py
```

The project uses only Python’s standard library for its implementation: `sys`, `csv`, and `datetime`. Pytest is used for testing.

## Design Choices

I separated the program into small functions so that each responsibility is clear. `load_events` handles file reading and validation, `parse_event` converts one CSV row’s timestamp, `sort_events` establishes chronological order, and each incident rule has its own function. This structure keeps the detection logic independent from the command-line interface and makes the rules straightforward to test.

Ziva Incident Analyser is intentionally narrow in scope. It is not a live telemetry platform, a robotics simulator, a ROS integration, or an automated root-cause system. It is a transparent first step toward a future incident-analysis tool for robots: CSV evidence in, structured timeline and explainable findings out.