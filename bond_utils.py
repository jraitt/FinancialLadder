import pandas as pd
import numpy as np
import yfinance as yf

def get_bond_data():
    """
    Fetch current data for the bond funds used in the ladder
    """
    # List of bond funds
    bond_funds = ["BND", "BNDX", "VFIDX", "VFSUX", "VGUS", "VBIL"]
    
    # Map display names
    display_names = {
        "BND": "Vanguard Total Bond Market ETF",
        "BNDX": "Vanguard Total International Bond ETF",
        "VFIDX": "Vanguard Intermediate-Term Investment-Grade Fund",
        "VFSUX": "Vanguard Short-Term Investment-Grade Fund",
        "VGUS": "Vanguard Ultra-Short Treasury ETF",  # 1-12 months maturity
        "VBIL": "Vanguard Ultra-Short Treasury Bills ETF"  # 0-3 months maturity
    }
    
    # Map maturity ranges (in years)
    maturity_ranges = {
        "BND": "7-8",
        "BNDX": "8-9",
        "VFIDX": "5-6",
        "VFSUX": "2-3",
        "VGUS": "0-1",  # Ultra-short-term Treasury (1-12 months)
        "VBIL": "0-0.25"  # Ultra-short Treasury Bills (0-3 months)
    }
    
    # Map credit quality
    credit_quality = {
        "BND": "Mixed Investment Grade",
        "BNDX": "Mixed Investment Grade",
        "VFIDX": "Investment Grade",
        "VFSUX": "Investment Grade",
        "VGUS": "U.S. Treasury",  # Highest quality
        "VBIL": "U.S. Treasury Bills"  # Highest quality, shortest term
    }
    
    # Create DataFrame
    bond_data = pd.DataFrame(index=bond_funds)
    
    try:
        # Fetch data for each fund
        for fund in bond_funds:
            ticker = yf.Ticker(fund)
            info = ticker.info
            
            # Get recent price data
            hist = ticker.history(period="1mo")
            
            # Calculate yield (this is an approximation)
            if 'yield' in info and info['yield'] is not None:
                yield_value = info['yield'] * 100
            else:
                # Fallback yields if not available
                fallback_yields = {
                    "BND": 4.2,
                    "BNDX": 3.8,
                    "VFIDX": 4.8,
                    "VFSUX": 4.5,
                    "VGUS": 4.3,
                    "VBIL": 4.0
                }
                yield_value = fallback_yields[fund]
            
            # Add to DataFrame
            bond_data.loc[fund, 'Name'] = display_names[fund]
            bond_data.loc[fund, 'Maturity Range (years)'] = maturity_ranges[fund]
            bond_data.loc[fund, 'Credit Quality'] = credit_quality[fund]
            bond_data.loc[fund, 'Current Price ($)'] = round(hist['Close'].iloc[-1], 2) if not hist.empty else np.nan
            bond_data.loc[fund, 'Yield (%)'] = round(yield_value, 2)
            
        return bond_data
    
    except Exception as e:
        # If there's an error fetching data, use fallback data
        for fund in bond_funds:
            bond_data.loc[fund, 'Name'] = display_names[fund]
            bond_data.loc[fund, 'Maturity Range (years)'] = maturity_ranges[fund]
            bond_data.loc[fund, 'Credit Quality'] = credit_quality[fund]
            
            # Fallback values
            fallback_prices = {
                "BND": 72.50,
                "BNDX": 48.75,
                "VFIDX": 9.40,
                "VFSUX": 9.60,
                "VGUS": 60.25,
                "VBIL": 50.80
            }
            
            fallback_yields = {
                "BND": 4.2,
                "BNDX": 3.8,
                "VFIDX": 4.8,
                "VFSUX": 4.5,
                "VGUS": 4.3,
                "VBIL": 4.0
            }
            
            bond_data.loc[fund, 'Current Price ($)'] = round(fallback_prices[fund], 2)
            bond_data.loc[fund, 'Yield (%)'] = round(fallback_yields[fund], 2)
        
        return bond_data

def get_age_adjusted_allocation(age):
    """
    Calculate the recommended allocation percentages based on age
    Returns percentages for short, intermediate, and long-term bonds
    """
    # Basic rule: 100 - age = percentage for more aggressive allocations
    # The older, the more conservative (more short-term bonds)
    
    aggressive_portion = max(20, 100 - age)  # No less than 20% in intermediate/long
    
    # Distribution between intermediate and long
    long_term_pct = int(aggressive_portion * 0.4)
    intermediate_pct = int(aggressive_portion * 0.6)
    short_term_pct = 100 - long_term_pct - intermediate_pct
    
    return {
        'short': short_term_pct,
        'intermediate': intermediate_pct,
        'long': long_term_pct
    }

def calculate_bond_ladder(investment_amount, age, investment_horizon, risk_tolerance, bond_data, include_international=True):
    """
    Calculate the optimal bond ladder allocation based on inputs
    
    Parameters:
    - investment_amount: Total amount to invest
    - age: Investor's age (used for age-appropriate allocation)
    - investment_horizon: Number of years for investment
    - risk_tolerance: Level of risk comfort
    - bond_data: DataFrame with bond fund information
    - include_international: Whether to include international bonds (BNDX)
    """
    # Define risk tolerance multipliers
    risk_multipliers = {
        "Very Conservative": 0.7,
        "Conservative": 0.85,
        "Moderate": 1.0,
        "Aggressive": 1.15,
        "Very Aggressive": 1.3
    }
    
    # Define term categories for each fund
    term_categories = {
        "BND": "intermediate",    # Total Bond Market
        "BNDX": "long",           # International Bond
        "VFIDX": "intermediate",  # Intermediate Investment-Grade
        "VFSUX": "short",         # Short-Term Investment-Grade
        "VGUS": "short",          # Ultra-Short Treasury ETF (1-12 months)
        "VBIL": "short"           # Ultra-Short Treasury Bills ETF (0-3 months)
    }
    
    # Base allocation (before adjustments)
    base_allocation = {
        "BND": 0.25,
        "BNDX": 0.15,
        "VFIDX": 0.20,
        "VFSUX": 0.15,
        "VGUS": 0.15,
        "VBIL": 0.10
    }
    
    # Adjust for age if specified
    if age is not None:
        age_allocation = get_age_adjusted_allocation(age)
        
        # Calculate total allocation per term category in base allocation
        term_totals = {"short": 0, "intermediate": 0, "long": 0}
        for fund, alloc in base_allocation.items():
            term_totals[term_categories[fund]] += alloc
        
        # Adjust each fund proportionally within its term category
        adjusted_allocation = {}
        for fund, alloc in base_allocation.items():
            term = term_categories[fund]
            term_ratio = alloc / term_totals[term] if term_totals[term] > 0 else 0
            adjusted_allocation[fund] = (age_allocation[term] / 100) * term_ratio
    else:
        adjusted_allocation = base_allocation.copy()
    
    # Adjust for investment horizon
    # For longer horizons, increase allocation to longer-term bonds
    horizon_factor = min(1.5, max(0.5, investment_horizon / 10))
    
    for fund in adjusted_allocation:
        if term_categories[fund] == "long":
            adjusted_allocation[fund] *= horizon_factor
        elif term_categories[fund] == "short":
            adjusted_allocation[fund] *= (2 - horizon_factor)
    
    # Adjust for risk tolerance
    risk_factor = risk_multipliers[risk_tolerance]
    
    for fund in adjusted_allocation:
        if term_categories[fund] == "long":
            adjusted_allocation[fund] *= risk_factor
        elif term_categories[fund] == "short":
            adjusted_allocation[fund] *= (2 - risk_factor)
    
    # Handle international bond inclusion
    if not include_international and "BNDX" in adjusted_allocation:
        # Redistribute BNDX allocation to other funds
        bndx_allocation = adjusted_allocation.pop("BNDX")
        
        # Redistribute proportionally to domestic funds
        domestic_funds = [f for f in adjusted_allocation.keys()]
        domestic_total = sum(adjusted_allocation[f] for f in domestic_funds)
        
        for fund in domestic_funds:
            # Add proportional share of BNDX allocation
            if domestic_total > 0:
                ratio = adjusted_allocation[fund] / domestic_total
                adjusted_allocation[fund] += bndx_allocation * ratio
    
    # Normalize to ensure sum is 1.0
    total = sum(adjusted_allocation.values())
    for fund in adjusted_allocation:
        adjusted_allocation[fund] /= total
    
    return adjusted_allocation
