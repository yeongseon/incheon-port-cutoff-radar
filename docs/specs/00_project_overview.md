# Incheon Port Cut-off Miss Risk Radar
## Project Overview

## 1. What this project is

Incheon Port Cut-off Miss Risk Radar is a decision-support web service for inbound container operations.

A user enters:

- origin
- destination terminal
- gate-in cut-off time

The system returns:

- estimated on-time arrival probability
- cut-off miss risk score
- latest safe dispatch time
- top contributing reasons

## 2. Why this project exists

Current port-related systems mainly expose operational status such as congestion level, turnaround time, and terminal-related information.

However, field operators still need to answer a more direct question:

> "Can this specific job still make the cut-off if we dispatch now?"

This project focuses on that question.

## 3. Problem statement

In port logistics operations, missing gate-in cut-off can cause:

- shipment delay
- replanning
- extra operational cost
- missed sailing risk

At the same time, users often need to manually combine:

- road traffic information
- terminal congestion
- entry flow information
- terminal operational hints

This project converts those fragmented data points into one operational decision.

## 4. Product positioning

This service does **not** replace existing status dashboards.

Instead, it acts as an upper decision layer on top of:

- terminal congestion data
- terminal information data
- gate entry statistics
- traffic information

## 5. Primary target users

- freight forwarder operators
- dispatch coordinators
- export logistics staff
- port-related planning staff
- students building a maritime ICT capstone

## 6. First-release scope

The first release is an MVP for **Incheon Port only**.

It will support:

- one port
- limited terminal list
- web UI only
- rule-based risk engine
- no external enterprise integrations

## 7. Success criteria

The MVP is successful if a user can:

1. input a single inbound job
2. get a result in a few seconds
3. understand whether the job is risky
4. see a recommended latest dispatch time
5. understand the main reasons behind the result
