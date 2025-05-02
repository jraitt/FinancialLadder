import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import numpy as np

def create_pie_chart(allocation):
    """
    Create a pie chart visualization of the bond allocation
    """
    labels = list(allocation.keys())
    values = [val * 100 for val in allocation.values()]  # Convert to percentages
    
    # Create readable labels with percentages
    labels_with_pct = [f"{label} ({val:.1f}%)" for label, val in zip(labels, values)]
    
    fig = go.Figure(data=[go.Pie(
        labels=labels_with_pct,
        values=values,
        hole=.3,
        textinfo='label',
        hoverinfo='label+percent',
        marker=dict(
            colors=px.colors.qualitative.Safe,
            line=dict(color='#FFFFFF', width=2)
        )
    )])
    
    fig.update_layout(
        title_text="Bond Fund Allocation",
        showlegend=True,
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=-0.2,
            xanchor="center",
            x=0.5
        ),
        height=500
    )
    
    return fig

def create_bar_chart(allocation, bond_data):
    """
    Create a bar chart showing allocation by maturity
    """
    # Extract maturity ranges and convert to numeric for sorting
    maturity_data = {}
    
    for fund, alloc in allocation.items():
        maturity_range = bond_data.loc[fund, 'Maturity Range (years)']
        # Take the midpoint of the range for sorting
        maturity_parts = maturity_range.split('-')
        if len(maturity_parts) == 2:
            midpoint = (float(maturity_parts[0]) + float(maturity_parts[1])) / 2
        else:
            midpoint = float(maturity_parts[0])
            
        maturity_data[fund] = {
            'allocation': alloc * 100,  # Convert to percentage
            'maturity': midpoint,
            'maturity_range': maturity_range
        }
    
    # Sort by maturity
    sorted_funds = sorted(maturity_data.keys(), key=lambda x: maturity_data[x]['maturity'])
    
    # Create the bar chart
    fig = go.Figure()
    
    for fund in sorted_funds:
        fig.add_trace(go.Bar(
            x=[fund],
            y=[maturity_data[fund]['allocation']],
            name=f"{fund} ({maturity_data[fund]['maturity_range']} years)",
            hovertemplate='%{y:.2f}%<extra></extra>'
        ))
    
    fig.update_layout(
        title_text="Allocation by Bond Maturity",
        xaxis_title="Bond Fund",
        yaxis_title="Allocation (%)",
        barmode='group',
        height=500
    )
    
    return fig

def create_ladder_chart(allocation, bond_data, investment_amount):
    """
    Create a visualization of the bond ladder structure
    """
    # Prepare data for the chart
    funds = list(allocation.keys())
    maturities = []
    for fund in funds:
        maturity_range = bond_data.loc[fund, 'Maturity Range (years)']
        maturity_parts = maturity_range.split('-')
        if len(maturity_parts) == 2:
            midpoint = (float(maturity_parts[0]) + float(maturity_parts[1])) / 2
        else:
            midpoint = float(maturity_parts[0])
        maturities.append(midpoint)
    
    amounts = [allocation[fund] * investment_amount for fund in funds]
    yields = [bond_data.loc[fund, 'Yield (%)'] for fund in funds]
    
    # Calculate expected income
    incomes = [amount * yield_val / 100 for amount, yield_val in zip(amounts, yields)]
    
    # Create DataFrame for the chart
    ladder_df = pd.DataFrame({
        'Fund': funds,
        'Maturity': maturities,
        'Amount': amounts,
        'Yield': yields,
        'Annual Income': incomes
    })
    
    # Sort by maturity
    ladder_df = ladder_df.sort_values('Maturity')
    
    # Create a custom color scale
    colors = px.colors.sequential.Viridis
    
    # Create the chart
    fig = go.Figure()
    
    # Add bars for each fund
    for i, row in ladder_df.iterrows():
        fig.add_trace(go.Bar(
            x=[row['Maturity']],
            y=[row['Amount']],
            name=row['Fund'],
            text=[f"${row['Amount']:.2f}<br>{row['Fund']}<br>Yield: {row['Yield']:.2f}%<br>Income: ${row['Annual Income']:.2f}"],
            hoverinfo='text',
            marker_color=colors[i % len(colors)]
        ))
    
    # Add a line connecting the bars to visualize the ladder
    maturity_points = ladder_df['Maturity'].tolist()
    amount_points = ladder_df['Amount'].tolist()
    
    fig.add_trace(go.Scatter(
        x=maturity_points,
        y=amount_points,
        mode='lines+markers',
        line=dict(color='rgba(0,0,0,0.5)', width=2, dash='dash'),
        marker=dict(size=10, symbol='circle', color='rgba(0,0,0,0.8)'),
        name='Ladder Structure',
        hoverinfo='skip'
    ))
    
    # Update layout
    fig.update_layout(
        title='Bond Ladder Structure',
        xaxis_title='Maturity (Years)',
        yaxis_title='Investment Amount ($)',
        barmode='group',
        height=600,
        showlegend=True,
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=-0.2,
            xanchor="center",
            x=0.5
        )
    )
    
    return fig
