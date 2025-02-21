# imports
import plotly.graph_objs as go
import plotly.express as px
import pandas as pd
import numpy as np

import hylite
from hylite import io

def viz2(df):
    # colors = px.colors.qualitative.Plotly
    # def hex_rgba(hex, transparency):
    #     col_hex = hex.lstrip('#')
    #     col_rgb = list(int(col_hex[i:i+2], 16) for i in (0, 2, 4))
    #     col_rgb.extend([transparency])
    #     areacol = tuple(col_rgb)
    #     return areacol

    # rgba = [hex_rgba(c, transparency=0.2) for c in colors]

    x = [float(c) for c in df.columns]
    y_upper = []
    y_mean = []
    y_lower = []
    for (columnName, columnData) in df.items(): 
        mean = columnData.mean().item()
        std = np.std(columnData)
        y_upper.append(mean+std)
        y_mean.append(mean)
        y_lower.append(mean-std)
    
    fig = go.Figure()
    # Add the shaded region
    fig.add_trace(go.Scatter(
        x=np.concatenate([x, x[::-1]]),  # x, then x reversed
        y=np.concatenate([y_upper, y_lower[::-1]]),  # upper, then lower reversed
        fill='tozeroy',  # or 'tozerox' if you have y=constant
        fillcolor='rgba(255,0,0,0.3)',  # Red with some transparency
        line=dict(color='rgba(255,255,255,0)'),  # No line
        name='Shaded Area & Mean',
        hoverinfo='none', # Remove hover info for shaded area
        showlegend=True, # Make sure this is True initially
        legendgroup='S'
    ))

    # # standard deviation area
    # fig.add_traces(go.Scatter(x=x,
    #                             y=y_upper,
    #                             # fill='tozerox',
    #                             # fillcolor='red',
    #                             # line=dict(color='rgba(255,255,255,0)'),
    #                             showlegend=True,
    #                             ))

    # line trace
    fig.add_traces(go.Scatter(x=x,
                            y=y_mean,
                            line=dict(color='red', width=2.5),
                            mode='lines',
                            showlegend=False,
                            legendgroup='S'
                            )
                                )
    # # standard deviation area
    # fig.add_traces(go.Scatter(x=x,
    #                             y=y_lower,
    #                             # fill='tozerox',
    #                             # fillcolor='red',
    #                             # line=dict(color='rgba(255,255,255,0)'),
    #                             showlegend=True,
    #                             ))
    # set x-axis
    # fig.update_layout(xaxis=dict(range=[1,len(df)]))

    fig.show()

if __name__ == '__main__':
    header = io.load('/Users/nova98/Documents/Nova/Spectrolysis/raw_data_car2car/Sisurock/20241211_Car2Car.shed/Car2Car_Table_12.hyc/b1_1_2.hyc/masked_spectrum/S19_FENIX.hdr')
    fenix_data = np.squeeze(header.data, axis=1)
    df = pd.DataFrame(fenix_data, columns=header.get_wavelengths())
    viz2(df)