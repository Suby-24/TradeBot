import test
import pandas as pd
import numpy as np
import plotly.graph_objects as go

def plot_inflection_points(inflection_list, ohlcv_df):
    """
    Plots the baseline price curve and overlays the inflection points
    stored as indices inside your nested list.
    """
    fig = go.Figure()
    
    # 1. Plot the continuous underlying price line 
    # X-axis and Y-axis
    fig.add_trace(go.Scatter(
        x=ohlcv_df.index,
        y=ohlcv_df['open'],
        mode='lines',
        name='Open Price',
        line=dict(color='#34495e', width=1.5)
    ))
    
    # 2. Extract and plot the points for each box
    for box_idx, cluster in enumerate(inflection_list):
        if not cluster:
            continue
            
        # Your lookup method: Map index locations back to raw prices
        cluster_prices = [ohlcv_df['open'].iloc[x] for x in cluster]
        
        # Overlay the points as isolated scatter markers
        fig.add_trace(go.Scatter(
            x=cluster,
            y=cluster_prices,
            mode='markers',
            name=f'Box {box_idx} Points',
            marker=dict(
                size=9, 
                line=dict(width=1, color='DarkSlateGrey')
            ),
            hoverinfo='name+x+y'
        ))
        
    # 3. Clean up presentation details
    fig.update_layout(
        title='Suby Bot - Inflection Point Clusters',
        xaxis_title='Data Row Index',
        yaxis_title='Price (USDT)',
        template='plotly_white',
        hovermode='closest'
    )
    
    fig.show()