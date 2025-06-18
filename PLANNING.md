# Project Planning: BondPlanner

This document outlines the architectural decisions, coding standards, and overall planning for the BondPlanner application.

## 1. Project Goals

-   To provide a user-friendly Streamlit application for bond portfolio allocation.
-   To offer personalized bond ladder strategies based on user inputs (age, investment amount, risk tolerance, etc.).
-   To visualize bond allocations and expected returns clearly.
-   To ensure maintainability, scalability, and testability of the codebase.

## 2. Architecture Overview

The application follows a modular architecture, separating concerns into distinct Python files:

-   `app.py`: Handles the Streamlit UI, user input, and orchestration of other modules.
-   `bond_utils.py`: Contains core business logic related to fetching bond data, calculating allocations, and age-based recommendations.
-   `visualization.py`: Responsible for generating all charts and visualizations using Plotly.

## 3. Coding Standards and Conventions

-   **Language**: Python 3.9+
-   **Formatting**: Adhere to PEP8 guidelines. Use `black` for automated code formatting.
-   **Type Hinting**: All functions and variables should use type hints for clarity and maintainability.
-   **Docstrings**: Every function, class, and module should have a Google-style docstring explaining its purpose, arguments, and return values.
-   **Comments**: Use inline comments for non-obvious logic, explaining the "why" rather than just the "what".
-   **Naming**:
    -   Variables and functions: `snake_case`
    -   Classes: `PascalCase`
    -   Constants: `UPPER_SNAKE_CASE`
-   **Imports**: Prefer relative imports within the project. Organize imports alphabetically.

## 4. Data Handling and Validation

-   **Data Fetching**: Use `yfinance` for fetching real-time bond fund data. Implement robust error handling and fallback mechanisms for data retrieval failures.
-   **Data Structures**: Utilize `pandas.DataFrame` for tabular data (e.g., bond information, allocation tables).
-   **Data Validation**: Use `pydantic` for validating input data where complex data models are involved (though less critical for simple Streamlit inputs).

## 5. Testing Strategy

-   **Unit Tests**: All core logic (functions in `bond_utils.py`, `visualization.py`) must have corresponding unit tests.
-   **Framework**: `pytest` will be used for running tests.
-   **Test Structure**: Tests will reside in a `tests/` directory, mirroring the main application's module structure (e.g., `tests/bond_utils/test_bond_utils.py`).
-   **Test Coverage**: Aim for high test coverage, including:
    -   Expected use cases
    -   Edge cases (e.g., zero investment, extreme ages, empty data)
    -   Failure cases (e.g., API errors, invalid inputs)

## 6. Dependencies

-   `streamlit`: For building the web application UI.
-   `pandas`: For data manipulation and analysis.
-   `numpy`: For numerical operations.
-   `yfinance`: For fetching financial data.
-   `plotly`: For interactive data visualizations.
-   `SQLAlchemy` / `SQLModel`: (If database integration becomes necessary in the future).
-   `pydantic`: For data validation.
-   `black`: For code formatting.
-   `pytest`: For unit testing.
-   `fastapi`: (If a separate API backend is introduced in the future).

## 7. Future Enhancements (Potential TODOs)

-   Implement user authentication and personalized dashboards.
-   Integrate with a database for storing user portfolios.
-   Add more sophisticated bond analytics (e.g., duration, convexity).
-   Allow users to select custom bond funds.
-   Implement backtesting capabilities for strategies.
-   Improve error logging and monitoring.

## 8. Constraints

-   **File Size**: No single Python file should exceed 500 lines of code. Refactor into smaller modules if necessary.
-   **Performance**: Ensure the application remains responsive, especially during data fetching and chart rendering.
-   **Security**: Handle API keys and sensitive information securely (though not currently applicable for `yfinance`).
