Ziva Incident Analyser — Product Requirements Document

===== Status =====

M0 — Product definition and incident model.

===== Purpose =====

Ziva Incident Analyser is a command-line Python program that reads a robot incident log from a CSV file, reconstructs the chronological timeline, detects predefined operational anomalies, and generates an evidence-grounded incident report.

It is a small CS50P capstone and an early conceptual ancestor of Ziva Robotics.

===== Problem =====

When an autonomous mobile robot (AMR) collides with an obstacle, engineers need a quick way to inspect the recorded event log and identify suspicious patterns.

A raw event log is difficult to read and does not clearly distinguish recorded facts from possible explanations.

===== Target user =====

A developer, robotics student, or operator investigating a single simulated warehouse robot incident.

===== User story =====

As an investigator, I want to provide a robot incident CSV file and receive an ordered timeline with evidence-backed findings, so that I can understand what the log suggests happened without overstating the root cause.

===== Input =====

The program accepts one CSV file passed as a command-line argument:

python project.py sample_incident.csv

The CSV must contain these columns:

1. Timestamp

ISO 8601 timestamp for the event

2. Source

Component that recorded the event

3. event_type

Type of event

4. details

Short contextual description

The initial supported event types are:

sensor_scan

obstacle_detected

brake_command

collision

===== Incident scenario =====

A warehouse autonomous mobile robot approaches a shelf.

It records a sensor scan, detects the shelf, sends a brake command after a delay, and then collides with the shelf.

===== Deterministic detection rules =====

1. Stale sensor evidence

If the most recent sensor_scan occurred more than two seconds before the collision, report that sensor evidence may have been stale.

2. Delayed braking response

If a brake_command occurred more than two seconds after obstacle_detected, report delayed braking evidence.

3. Missing response

If an obstacle was detected but no brake_command was recorded before the collision, report a missing braking response.

===== Output =====

The program prints:

Incident summary

Chronological event timeline

Findings with exact supporting evidence

Limitations and uncertainty

Example finding:

FINDING: Delayed braking response
EVIDENCE: Obstacle detected at 10:00:02.
          Brake command recorded at 10:00:05.
          Delay: 3.0 seconds.
LIMITATION: The event log does not prove why braking was delayed.

===== Success criteria =====

The project succeeds when a user can run one command on a valid CSV file and receive:

a validated, ordered incident timeline;

deterministic findings with timestamps;

a readable report;

no unsupported claim of a confirmed root cause.

===== Non-goals =====

This CS50P version will not include:

ROS 2, Gazebo, or robot hardware;

live telemetry;

AI, machine learning, or LLM-based diagnosis;

databases, accounts, web or mobile interfaces;

complex simulation or physics;

root-cause claims presented as proven facts.