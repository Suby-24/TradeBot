import pandas as pd
import numpy as np
import plotly.graph_objects as go

def plot_inflection_points(inflection_list, ohlcv_df, horizontal_lines_list=None):
    """
    Plots the baseline price curve, overlays nested inflection point clusters,
    and optionally draws straight horizontal reference lines across the entire canvas.
    """
    fig = go.Figure()
    
    # 1. Original Plotting Logic: Underlying Price Line
    fig.add_trace(go.Scatter(
        x=ohlcv_df.index,
        y=ohlcv_df['open'],
        mode='lines',
        name='Open Price',
        line=dict(color='#34495e', width=1.5)
    ))
    
    # 2. Original Plotting Logic: Overlay Inflection Point Scatter Markers
    for box_idx, cluster in enumerate(inflection_list):
        if not cluster:
            continue
            
        # Map structural index locations back to raw open prices
        cluster_prices = [ohlcv_df['open'].iloc[x] for x in cluster]
        
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
        
    # 3. New Feature: Draw Straight Lines Based on Input Price 1D-Array
    if horizontal_lines_list is not None:
        # Subtle, high-contrast palette for reference levels
        palette = ['#e74c3c', '#2ecc71', '#f1c40f', '#9b5de5', '#00bbf9']
        
        for idx, price in enumerate(horizontal_lines_list):
            line_color = palette[idx % len(palette)]
            
            fig.add_hline(
                y=price,
                line_dash="dash",               # Clean dashed pattern for support/resistance
                line_color=line_color,
                line_width=1.5,
                annotation_text=f"Level: ${price:,.1f}",
                annotation_position="bottom right"
            )
        
    # 4. Global Chart Layout Realignment
    fig.update_layout(
        title='Suby Bot - Structural Analysis Framework',
        xaxis_title='Data Row Index',
        yaxis_title='Price (USDT)',
        template='plotly_white',
        hovermode='closest'
    )
    
    fig.show()

def plot_price_list(price_list):
    """
    Plots a simple, interactive line chart from a flat list of prices.
    """
    # Create the interactive chart
    fig = go.Figure()
    
    # Add the price path line
    fig.add_trace(go.Scatter(
        x=list(range(len(price_list))),  # X-axis is just the index sequence (0, 1, 2...)
        y=price_list,                    # Y-axis is your raw price data
        mode='lines+markers',            # Combines the trend line with individual data points
        name='Price',
        line=dict(color='#2ecc71', width=2),
        marker=dict(size=5, color='#34495e')
    ))
    
    # Clean, distraction-free chart layout
    fig.update_layout(
        title='Suby Bot - Price Stream Visualization',
        xaxis_title='Sequence Index',
        yaxis_title='Price (USDT)',
        template='plotly_white',
        hovermode='x unified'            # Shows price clearly when hovering anywhere on the timeline
    )
    
    fig.show()