import pytest
import pandas as pd
import numpy as np
from unittest.mock import patch
from bond_utils import get_bond_data

# Mock yfinance for testing get_bond_data
class MockTicker:
    def __init__(self, symbol):
        self.symbol = symbol

    def history(self, period):
        if self.symbol == "BND":
            return pd.DataFrame({'Close': [72.50]})
        elif self.symbol == "BNDX":
            return pd.DataFrame({'Close': [48.75]})
        elif self.symbol == "VFIDX":
            return pd.DataFrame({'Close': [9.40]})
        elif self.symbol == "VFSUX":
            return pd.DataFrame({'Close': [9.60]})
        elif self.symbol == "VGUS":
            return pd.DataFrame({'Close': [60.25]})
        elif self.symbol == "VBIL":
            return pd.DataFrame({'Close': [50.80]})
        elif self.symbol == "VCORX":
            return pd.DataFrame({'Close': [9.01]})
        return pd.DataFrame()

    @property
    def info(self):
        if self.symbol == "BND":
            return {'yield': 0.042, 'expenseRatio': 0.0003}
        elif self.symbol == "BNDX":
            return {'yield': 0.038, 'expenseRatio': 0.0007}
        elif self.symbol == "VFIDX":
            return {'yield': 0.048, 'expenseRatio': 0.0010}
        elif self.symbol == "VFSUX":
            return {'yield': 0.045, 'expenseRatio': 0.0010}
        elif self.symbol == "VGUS":
            return {'yield': 0.043, 'expenseRatio': 0.0007}
        elif self.symbol == "VBIL":
            return {'yield': 0.040, 'expenseRatio': 0.0007}
        elif self.symbol == "VCORX":
            return {'yield': 0.0462, 'expenseRatio': 0.0020}
        return {}

@patch('yfinance.Ticker', new=MockTicker)
def test_get_bond_data_success():
    bond_data = get_bond_data()

    assert isinstance(bond_data, pd.DataFrame)
    assert not bond_data.empty
    assert "BND" in bond_data.index
    assert "Yield (%)" in bond_data.columns
    assert "Expense Ratio (%)" in bond_data.columns
    assert bond_data.loc["BND", "Yield (%)"] == 4.2
    assert bond_data.loc["BND", "Expense Ratio (%)"] == 0.03
    assert bond_data.loc["BNDX", "Current Price ($)"] == 48.75

@patch('yfinance.Ticker', side_effect=Exception("Test API Error"))
def test_get_bond_data_fallback(mock_ticker):
    bond_data = get_bond_data()

    assert isinstance(bond_data, pd.DataFrame)
    assert not bond_data.empty
    assert "BND" in bond_data.index
    assert bond_data.loc["BND", "Yield (%)"] == 4.2
    assert bond_data.loc["BNDX", "Current Price ($)"] == 48.75
    assert "VCORX" in bond_data.index
    assert bond_data.loc["VCORX", "Yield (%)"] == 4.62
    assert bond_data.loc["VCORX", "Current Price ($)"] == 9.01
    assert bond_data.loc["VCORX", "Expense Ratio (%)"] == 0.20
