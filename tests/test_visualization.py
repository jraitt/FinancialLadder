import pytest
import pandas as pd
from visualization import create_pie_chart, create_bar_chart, create_ladder_chart
import plotly.graph_objects as go
import plotly.express as px
from unittest.mock import MagicMock, patch

# Sample data for testing
@pytest.fixture
def sample_bond_data():
    return pd.DataFrame({
        'Name': [
            "Vanguard Total Bond Market ETF",
            "Vanguard Total International Bond ETF",
            "Vanguard Intermediate-Term Investment-Grade Fund",
            "Vanguard Short-Term Investment-Grade Fund",
            "Vanguard Ultra-Short Treasury ETF",
            "Vanguard Ultra-Short Treasury Bills ETF"
        ],
        'Maturity Range (years)': ["7-8", "8-9", "5-6", "2-3", "0-1", "0-0.25"],
        'Credit Quality': [
            "Mixed Investment Grade",
            "Mixed Investment Grade",
            "Investment Grade",
            "Investment Grade",
            "U.S. Treasury",
            "U.S. Treasury Bills"
        ],
        'Current Price ($)': [72.50, 48.75, 9.40, 9.60, 60.25, 50.80],
        'Yield (%)': [4.2, 3.8, 4.8, 4.5, 4.3, 4.0]
    },
        index=["BND", "BNDX", "VFIDX", "VFSUX", "VGUS", "VBIL"]
    )

@pytest.fixture
def sample_allocation():
    return {
        "BND": 0.35,
        "BNDX": 0.30,
        "VFIDX": 0.20,
        "VFSUX": 0.15,
        "VGUS": 0.0,
        "VBIL": 0.0
    }

@patch('plotly.graph_objects.Figure.add_trace')
@patch('plotly.graph_objects.Figure.update_layout')
@patch('plotly.express.colors.qualitative.Safe', ['red', 'blue', 'green', 'yellow', 'purple', 'orange'])
def test_create_pie_chart(mock_update_layout, mock_add_trace):
    allocation = {
        "BND": 0.35,
        "BNDX": 0.30,
        "VFIDX": 0.20,
        "VFSUX": 0.15,
        "VGUS": 0.0,
        "VBIL": 0.0
    }

    create_pie_chart(allocation)

    # Check if add_trace was called with correct data (excluding 0% allocations)
    mock_add_trace.assert_called_once()
    args, kwargs = mock_add_trace.call_args
    assert isinstance(args[0], go.Pie)
    assert args[0].labels == [f"BND (35.0%)", f"BNDX (30.0%)", f"VFIDX (20.0%)", f"VFSUX (15.0%)"]
    assert args[0].values == [35.0, 30.0, 20.0, 15.0]

    mock_update_layout.assert_called_once()

@patch('plotly.graph_objects.Figure.add_trace')
@patch('plotly.graph_objects.Figure.update_layout')
def test_create_bar_chart(mock_update_layout, mock_add_trace, sample_allocation, sample_bond_data):
    create_bar_chart(sample_allocation, sample_bond_data)

    # Check if add_trace was called for each non-zero allocation
    assert mock_add_trace.call_count == 4  # BND, BNDX, VFIDX, VFSUX

    # Verify data for each call
    expected_funds = ["VFSUX", "VFIDX", "BND", "BNDX"] # Expected order after sorting by maturity
    expected_allocations = [15.0, 20.0, 35.0, 30.0]

    for i, (args, kwargs) in enumerate(mock_add_trace.call_args_list):
        assert isinstance(args[0], go.Bar)
        assert args[0].x[0] == expected_funds[i]
        assert args[0].y[0] == expected_allocations[i]

    mock_update_layout.assert_called_once()

@patch('plotly.graph_objects.Figure.add_trace')
@patch('plotly.graph_objects.Figure.update_layout')
@patch('plotly.express.colors.sequential.Viridis', ['red', 'blue', 'green', 'yellow', 'purple', 'orange'])
def test_create_ladder_chart(mock_update_layout, mock_add_trace, sample_allocation, sample_bond_data):
    create_ladder_chart(sample_allocation, sample_bond_data, 1000000)

    # Check if add_trace was called for each non-zero allocation (bars) + 1 for scatter
    assert mock_add_trace.call_count == 5  # 4 bars + 1 scatter

    # Verify data for bar calls
    bar_calls = [call for call in mock_add_trace.call_args_list if isinstance(call.args[0], go.Bar)]
    assert len(bar_calls) == 4

    # Verify data for the scatter call
    scatter_call = next(call for call in mock_add_trace.call_args_list if isinstance(call.args[0], go.Scatter))
    args, kwargs = scatter_call
    assert args[0].mode == 'lines+markers'
    # The order of maturities in the scatter plot should be sorted
    expected_x = [2.5, 5.5, 7.5, 8.5] # VFSUX, VFIDX, BND, BNDX (sorted by maturity midpoint)
    expected_y = [150000.0, 200000.0, 350000.0, 300000.0] # Corresponding amounts
    assert list(args[0].x) == expected_x
    assert list(args[0].y) == expected_y

    mock_update_layout.assert_called_once()