# Project Tasks: BondPlanner

This document tracks the development tasks for the BondPlanner application.

## Current Tasks

-   None

## Completed Tasks

-   **2025-07-01**: Removed existing user inputs and replaced with allocation allotment for each bond type by symbol. Added alert if total portfolio allotment does not equal 100%.
-   **2025-07-01**: Removed `calculate_bond_ladder` and `get_age_adjusted_allocation` functions from `bond_utils.py`.
-   **2025-07-01**: Updated default investment amount to 1,000,000 and default bond allocations to BND=35%, BNDX=30%, VFIDX=20%, VFSUX=15%, VGUS=0%, VBIL=0%.


## Completed Tasks

-   **2025-06-05**: In "current bond information" table, make all "Current Price" and "Yield" values two decimal places (xx.xx).

## Discovered During Work

-   Consider creating a `requirements.txt` file to list all project dependencies for easier setup.
-   Add unit tests for `bond_utils.py` and `visualization.py` functions as per `PLANNING.md`.
-   Implement more robust error handling for `yfinance` data fetching.
