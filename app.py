import streamlit as st
import pandas as pd
import numpy as np
import yfinance as yf
from bond_utils import calculate_bond_ladder, get_bond_data, get_age_adjusted_allocation
from visualization import create_pie_chart, create_bar_chart, create_ladder_chart

# Set page configuration
st.set_page_config(
    page_title="Bond Portfolio Planner JR",
    page_icon="📊",
    layout="wide"
)

# Application title and description
st.title("Bond Portfolio Planner")
st.markdown("""
This tool helps you create a personalized portfolio allocation strategy based on your investment amount, 
age, and other preferences.
""")

# Sidebar for inputs
st.sidebar.header("Investment Parameters")

# Input for investment amount
investment_amount = st.sidebar.number_input(
    "Amount to Invest ($)",
    min_value=1000,
    max_value=10000000,
    value=100000,
    step=1000,
    help="Enter the total amount you want to invest Bonds"
)

# Age adjustment option
use_age_adjustment = st.sidebar.radio(
    "Adjust for Age?",
    ["Yes", "No"],
    index=0,
    help="If selected, the bond allocation will be adjusted based on your age"
)

# If age adjustment is selected, show age input
if use_age_adjustment == "Yes":
    age = st.sidebar.slider(
        "Your Age",
        min_value=20,
        max_value=80,
        value=40,
        step=1,
        help="Your current age will be used to adjust your bond allocation"
    )
else:
    age = None

# Additional parameters
st.sidebar.subheader("Additional Parameters")

investment_horizon = st.sidebar.slider(
    "Investment Horizon (years)",
    min_value=1,
    max_value=30,
    value=10,
    step=1,
    help="How long you plan to hold your bond investments"
)

risk_tolerance = st.sidebar.select_slider(
    "Risk Tolerance",
    options=["Very Conservative", "Conservative", "Moderate", "Aggressive", "Very Aggressive"],
    value="Moderate",
    help="Your comfort level with investment risk"
)

# International bond option
st.sidebar.subheader("International Diversification")
include_international = st.sidebar.radio(
    "Include International Bonds?",
    ["Yes", "No"],
    index=0,
    help="Select 'Yes' to include Vanguard Total International Bond ETF (BNDX) in your allocation"
)

if include_international == "Yes":
    st.sidebar.info("Including international bonds (BNDX) provides geographic diversification and can reduce overall portfolio volatility.")
else:
    st.sidebar.info("Excluding international bonds will redistribute that allocation to domestic bond funds.")

# Bond fund selection
st.sidebar.subheader("Bond Funds")
st.sidebar.markdown("""
The allocation will be calculated using these bond funds:
- **BND**: Vanguard Total Bond Market ETF
- **BNDX**: Vanguard Total International Bond ETF
- **VFIDX**: Vanguard Intermediate-Term Investment-Grade Fund
- **VFSUX**: Vanguard Short-Term Investment-Grade Fund
- **VGUS**: Vanguard Ultra-Short Treasury ETF (1-12 months)
- **VBIL**: Vanguard Ultra-Short Treasury Bills ETF (0-3 months)
""")

# Informational section - collapsible
with st.expander("Bond Quality and Maturity Explained."):
    st.markdown("""
    ### Bond Quality
    
    Bond quality, often referred to as credit quality, indicates the likelihood that a bond issuer will 
    default on its debt obligations. Bonds are typically rated by credit rating agencies (e.g., Moody's, 
    Standard & Poor's) from highest (e.g., AAA) to lowest (e.g., D).
    
    -   **Investment Grade Bonds**: These are bonds issued by financially stable entities with a low 
        risk of default. They typically offer lower yields but are considered safer.
    -   **High-Yield (Junk) Bonds**: These are bonds issued by companies or governments with a higher 
        risk of default. They offer higher yields to compensate investors for the increased risk.
    
    ### Bond Maturity and Interest Rate Sensitivity
    
    **Maturity** refers to the length of time until the bond's principal is repaid to the investor. 
    Bonds can have short-term (e.g., less than 3 years), intermediate-term (e.g., 3-10 years), or 
    long-term (e.g., over 10 years) maturities.
    
    **Interest Rate Sensitivity** (or duration) describes how much a bond's price is likely to change 
    when interest rates move.
    
    -   **Inverse Relationship**: Bond prices and interest rates generally move in opposite directions. 
        When interest rates rise, existing bond prices fall (and vice-versa).
    -   **Longer Maturity = Higher Sensitivity**: Bonds with longer maturities are more sensitive to 
        changes in interest rates. A small change in interest rates will have a larger impact on the 
        price of a long-term bond than on a short-term bond.
    
    ### Bonds vs. Stocks: Historical Relationship
    
    Historically, bonds and stocks have often exhibited a low or negative correlation, meaning they tend 
    to move in different directions or have less synchronized movements.
    
    -   **Diversification**: This low correlation makes bonds a valuable diversification tool in a 
        portfolio. When stocks perform poorly, bonds may hold their value or even increase, providing 
        a cushion against overall portfolio losses.
    -   **Risk and Return**: Stocks generally offer higher potential returns over the long term but come 
        with higher volatility and risk. Bonds typically offer lower, more stable returns with less 
        volatility, making them suitable for capital preservation and income generation.
    """)

# Main content
st.header("Your Selected Bond Strategy")

# Fetch bond data
with st.spinner("Fetching latest bond fund data..."):
    try:
        bond_data = get_bond_data()
        
        # Display bond data in table
        st.subheader("Current Bond Fund Information")
        # Format 'Current Price ($)' and 'Yield (%)' columns to two decimal places for display
        bond_data_display = bond_data.copy()
        bond_data_display['Current Price ($)'] = bond_data_display['Current Price ($)'].apply(lambda x: f"{x:.2f}" if pd.notna(x) else "N/A")
        bond_data_display['Yield (%)'] = bond_data_display['Yield (%)'].apply(lambda x: f"{x:.2f}" if pd.notna(x) else "N/A")
        st.dataframe(bond_data_display)
        
        # Calculate bond ladder allocation
        allocation = calculate_bond_ladder(
            investment_amount=investment_amount,
            age=age,
            investment_horizon=investment_horizon,
            risk_tolerance=risk_tolerance,
            bond_data=bond_data,
            include_international=(include_international == "Yes")
        )
        
        # Display results in columns
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Bond Allocation")
            # Display pie chart of allocation
            fig_pie = create_pie_chart(allocation)
            st.plotly_chart(fig_pie, use_container_width=True)
        
        with col2:
            st.subheader("Allocation by Maturity")
            # Display bar chart by maturity
            fig_bar = create_bar_chart(allocation, bond_data)
            st.plotly_chart(fig_bar, use_container_width=True)
        
        # Display allocation table
        st.subheader("Detailed Allocation")
        
        # Create allocation table
        allocation_table = pd.DataFrame({
            "Fund": allocation.keys(),
            "Allocation (%)": [round(val * 100, 2) for val in allocation.values()],
            "Amount ($)": [round(val * investment_amount, 2) for val in allocation.values()]
        })
        
        st.dataframe(allocation_table)
        
        # Display ladder visualization
        st.subheader("Amount Vs. Maturity")
        fig_ladder = create_ladder_chart(allocation, bond_data, investment_amount)
        st.plotly_chart(fig_ladder, use_container_width=True)
        
        # Age-based recommendation section
        if age is not None:
            st.subheader("Age-Based Recommendation")
            age_recommendation = get_age_adjusted_allocation(age)
            
            st.markdown(f"""
            Based on your age ({age}), we recommend:
            
            - **Short-term bonds**: {age_recommendation['short']}%
            - **Intermediate-term bonds**: {age_recommendation['intermediate']}%
            - **Long-term bonds**: {age_recommendation['long']}%
            
            Your current allocation is aligned with this recommendation.
            """)
            
        # Expected returns section
        st.subheader("Expected Returns and Considerations")
        
        # Calculate weighted average yield
        weighted_yield = sum(allocation[fund] * bond_data.loc[fund, 'Yield (%)'] for fund in allocation)
        
        st.markdown(f"""
        - **Estimated Annual Yield**: {weighted_yield:.2f}%
        - **Estimated Annual Income**: ${(weighted_yield/100 * investment_amount):.2f}
        
        **Important Considerations**:
        
        - Bond prices move inversely to interest rates
        - Longer-term bonds generally offer higher yields but with increased interest rate risk
        - Diversification across different bond types helps manage overall portfolio risk
        - Review and rebalance your bond ladder periodically, especially as bonds mature
        """)
        
    except Exception as e:
        st.error(f"Error processing bond data: {str(e)}")
        st.info("Please try again later or check your input parameters.")

# Footer
st.markdown("---")
st.markdown("""
**Disclaimer**: This tool provides general investment information and not personalized investment advice. 
Past performance is not indicative of future results. Consider consulting with a financial advisor before 
making investment decisions.
""")
