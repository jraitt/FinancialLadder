# BondPlanner

This project provides a Streamlit application to help users create a personalized bond portfolio allocation strategy. It allows users to input investment parameters such as amount, age, investment horizon, and risk tolerance, and then visualizes the recommended bond ladder strategy.

## Features

- **Personalized Allocation**: Adjusts bond allocation based on user's age and risk tolerance.
- **Bond Fund Data**: Fetches and displays current information for various Vanguard bond ETFs and funds.
- **Interactive Visualizations**: Presents allocation data through pie charts, bar charts, and a bond ladder visualization.
- **International Diversification**: Option to include international bonds (BNDX) for broader diversification.
- **Expected Returns**: Estimates annual yield and income based on the calculated allocation.

## Setup and Installation

To run this application locally, follow these steps:

1.  **Clone the repository**:
    ```bash
    git clone https://github.com/your-repo/BondPlanner.git
    cd BondPlanner
    ```

2.  **Create a virtual environment** (recommended):
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows: `venv\Scripts\activate`
    ```

3.  **Install dependencies**:
    ```bash
    pip install -r requirements.txt
    ```
    *(Note: You may need to create a `requirements.txt` file if it doesn't exist, listing `streamlit`, `pandas`, `numpy`, `yfinance`, `plotly`, `SQLAlchemy`, `SQLModel`, `pydantic`, `black`, `pytest`, `fastapi`)*

4.  **Run the Streamlit application**:
    ```bash
    streamlit run app.py
    ```

The application will open in your default web browser.

## Project Structure

-   `app.py`: Main Streamlit application file.
-   `bond_utils.py`: Contains functions for fetching bond data and calculating bond ladder allocations.
-   `visualization.py`: Contains functions for creating various charts and visualizations.
-   `README.md`: Project overview and setup instructions.
-   `PLANNING.md`: Project architecture, goals, style, and constraints.
-   `TASK.md`: List of current and completed tasks.

## Usage

1.  Adjust the investment parameters in the sidebar.
2.  View the "Current Bond Fund Information" table.
3.  Analyze the "Bond Allocation" and "Allocation by Maturity" charts.
4.  Review the "Detailed Allocation" table and "Bond Ladder Visualization".
5.  Check the "Expected Returns and Considerations" section for estimated income.

## Contributing

Contributions are welcome! Please refer to `PLANNING.md` and `TASK.md` for guidelines and current development status.

## License

This project is licensed under the MIT License.
