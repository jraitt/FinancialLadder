import streamlit as st
import pandas as pd
import numpy as np
import yfinance as yf
from bond_utils import calculate_bond_ladder, get_bond_data, get_age_adjusted_allocation
from visualization import create_pie_chart, create_bar_chart, create_ladder_chart

# Set page configuration
st.set_page_config(
    page_title="Bond Ladder Planning Tool",
    page_icon="📊",
    layout="wide"
)

# Application title and description
st.title("Bond Ladder Planning Tool")
st.markdown("""
This tool helps you create a personalized bond ladder strategy based on your investment amount, 
age, and other preferences. Bond laddering is a strategy that involves buying bonds with different 
maturity dates to manage interest rate risk and provide liquidity at regular intervals.
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
    help="Enter the total amount you want to invest in your bond ladder"
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
        help="Your current age will be used to adjust the bond ladder allocation"
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
with st.expander("What is a Bond Ladder?"):
    st.markdown("""
    ### Bond Ladder Concept
    
    A bond ladder is an investment strategy where you purchase bonds with staggered maturity dates. 
    Instead of buying a single bond that matures in, say, 10 years, you might buy several bonds that 
    mature in 2, 4, 6, 8, and 10 years.
    
    ### Key Benefits
    
    1. **Reduced Interest Rate Risk**: By spreading investments across different maturities, you reduce 
       the impact of interest rate fluctuations.
    
    2. **Liquidity Management**: As bonds mature at regular intervals, you have the flexibility to 
       either reinvest or use the proceeds.
    
    3. **Income Stability**: The ladder provides a consistent stream of income as different bonds mature.
    
    4. **Diversification**: Using different types of bond funds adds another layer of diversification.
    
    ### How This Tool Works
    
    This tool helps you allocate your investment across various bond funds with different maturity ranges 
    to create an effective bond ladder. If you choose age adjustment, the allocation will be tailored to 
    be more conservative as your age increases.
    """)

# Main content
st.header("Your Bond Ladder Strategy")

# Fetch bond data
with st.spinner("Fetching latest bond fund data..."):
    try:
        bond_data = get_bond_data()
        
        # Display bond data in table
        st.subheader("Current Bond Fund Information")
        st.dataframe(bond_data)
        
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
        st.subheader("Bond Ladder Visualization")
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
