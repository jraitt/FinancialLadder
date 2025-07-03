import pandas as pd
import numpy as np
import yfinance as yf

def get_bond_data():
    """
    Fetch current data for the bond funds used in the ladder
    """
    # List of bond funds
    bond_funds = ["BND", "BNDX", "VCORX", "VFIDX", "VFSUX", "VGUS", "VBIL"]
    
    # Map display names
    display_names = {
        "BND": "Vanguard Total Bond Market ETF",
        "BNDX": "Vanguard Total International Bond ETF",
        "VFIDX": "Vanguard Intermediate-Term Investment-Grade Fund",
        "VFSUX": "Vanguard Short-Term Investment-Grade Fund",
        "VGUS": "Vanguard Ultra-Short Treasury ETF",  # 1-12 months maturity
        "VBIL": "Vanguard Ultra-Short Treasury Bills ETF",  # 0-3 months maturity
        "VCORX": "Vanguard Core Bond Fund Investor Shares"
    }
    
    # Map maturity ranges (in years)
    maturity_ranges = {
        "BND": "7-8",
        "BNDX": "8-9",
        "VFIDX": "5-6",
        "VFSUX": "2-3",
        "VGUS": "0-1",  # Ultra-short-term Treasury (1-12 months)
        "VBIL": "0-0.25",  # Ultra-short Treasury Bills (0-3 months)
        "VCORX": "8-10"
    }
    
    # Map credit quality
    credit_quality = {
        "BND": "Mixed Investment Grade",
        "BNDX": "Mixed Investment Grade",
        "VFIDX": "Investment Grade",
        "VFSUX": "Investment Grade",
        "VGUS": "U.S. Treasury",  # Highest quality
        "VBIL": "U.S. Treasury Bills",  # Highest quality, shortest term
        "VCORX": "Mixed Investment Grade"
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
                    "VBIL": 4.0,
                    "VCORX": 4.62
                }
                yield_value = fallback_yields[fund]

            # Get expense ratio
            if 'netExpenseRatio' in info and info['netExpenseRatio'] is not None:
                er_value = info['netExpenseRatio']
            else:
                fallback_er = {
                    "BND": 0.03,
                    "BNDX": 0.07,
                    "VCORX": 0.20,
                    "VFIDX": 0.10,
                    "VFSUX": 0.10,
                    "VGUS": 0.07,
                    "VBIL": 0.07
                }
                er_value = fallback_er[fund]
            
            # Add to DataFrame
            bond_data.loc[fund, 'Name'] = display_names[fund]
            bond_data.loc[fund, 'Maturity Range (years)'] = maturity_ranges[fund]
            bond_data.loc[fund, 'Credit Quality'] = credit_quality[fund]
            bond_data.loc[fund, 'Current Price ($)'] = round(hist['Close'].iloc[-1], 2) if not hist.empty else np.nan
            bond_data.loc[fund, 'Expense Ratio (%)'] = round(er_value, 2)
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
                "VBIL": 50.80,
                "VCORX": 9.01
            }
            
            fallback_yields = {
                "BND": 4.2,
                "BNDX": 3.8,
                "VFIDX": 4.8,
                "VFSUX": 4.5,
                "VGUS": 4.3,
                "VBIL": 4.0,
                "VCORX": 4.62
            }

            fallback_er = {
                "BND": 0.03,
                "BNDX": 0.07,
                "VCORX": 0.20,
                "VFIDX": 0.10,
                "VFSUX": 0.10,
                "VGUS": 0.07,
                "VBIL": 0.07
            }
            
            bond_data.loc[fund, 'Current Price ($)'] = round(fallback_prices[fund], 2)
            bond_data.loc[fund, 'Expense Ratio (%)'] = round(fallback_er[fund], 2)
            bond_data.loc[fund, 'Yield (%)'] = round(fallback_yields[fund], 2)
        
        return bond_data
