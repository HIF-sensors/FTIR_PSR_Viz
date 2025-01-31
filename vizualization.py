import ast
import plotly.graph_objects as go
import plotly.express as px
import numpy as np

def viz(batch_name, df_plot, library, sensor='SWIR'):
    for key, df in df_plot.items():
        wavelengths = list(df.columns)[1:]
        data = []
        max_energy = df.iloc[:, 1:].max().max()+1 # For plotting vertical lines
        min_energy = df.iloc[:, 1:].min().min()-1 # For plotting vertical lines
        for index, row in df.iterrows():
            sample_name = list(row)[0]
            energy = list(row)[1:]
            graph = go.Scatter(x=wavelengths, y=energy, name = sample_name, mode='lines')
            data.append(graph)
        
        # Select specific library according to sensor
        # Iterate over the rows in the library and
        # draw a vertical line at each wavelength
        # Name them as polymer groups
        # append the lines in data
        lib = library[library['sensor'] == sensor]
        unique_groups = lib['polymer'].unique()
        color_map = {group: px.colors.qualitative.Plotly[i % len(px.colors.qualitative.Plotly)] for i, group in enumerate(unique_groups)}
        for index, row in lib.iterrows():
            group_name = row['polymer']
            wavelengths = [float(x) for x in ast.literal_eval(row['wavelengths'])]
            for i, x_value in enumerate(wavelengths):
                line = go.Scatter(
                    x=[x_value]*5,  # Duplicate x values for vertical lines
                    y=np.linspace(min_energy, max_energy, num=5).tolist(),  # Alternate y values for vertical lines
                    mode='lines',
                    name=group_name,
                    line=dict(color=color_map[group_name]),
                    legendgroup=group_name,
                    showlegend=True if i == 0 else False
                )
                data.append(line)

    fig = go.Figure(data=data)
    text = batch_name + "_" + sensor
    fig.update_layout(
        # yaxis_range=[0, 1],
        xaxis_title='Wavelength',
        yaxis_title='Reflectance',
        title={
            'text': batch_name + " : " + sensor,
            'font': {
                'size': 24,
                'color': 'black',
                'family': 'Arial',
                'weight': 'bold'
            },
            'x': 0.5,
            'xanchor': 'center'
        },
    )
    fig.update_layout(hovermode="x unified")
    fig.write_html(text + ".html")
     
    fig.show()
    