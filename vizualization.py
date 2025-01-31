import ast
import plotly.graph_objects as go
import plotly.express as px

def viz(batch_name, df, library, sensor='SWIR'):
    wavelengths = list(df.columns)[1:]
    data = []
    for index, row in df.iterrows():
        sample_name = list(row)[0]
        energy = list(row)[1:]
        graph = go.Scatter(x=wavelengths, y=energy, name = sample_name, mode='lines')
        data.append(graph)
    fig = go.Figure(data=data)
    # Select specific library according to sensor
    # Iterate over the rows in the library and
    # draw a vertical line at each wavelength
    # Name them as polymer groups
    # append the lines in data
    line_groups = {}
    lib = library[library['sensor'] == sensor]
    # Generate a color map
    unique_groups = lib['polymer'].unique()
    color_map = {group: px.colors.qualitative.Plotly[i % len(px.colors.qualitative.Plotly)] for i, group in enumerate(unique_groups)}
    for index, row in lib.iterrows():
        group_name = row['polymer']
        wavelengths = [float(x) for x in ast.literal_eval(row['wavelengths'])]
        for i, x_value in enumerate(wavelengths):
            fig.add_vline(
                x=x_value, 
                # line_dash="dash", 
                line_color=color_map[group_name], 
                opacity=0.5, 
                name=group_name,
                legendgroup=group_name,
                showlegend = True
                # showlegend=True if i == 0 else False
            )
        # line = go.Scatter(x=wavelengths, y=[1] * len(wavelengths), mode='lines', name=group_name)
        # data.append(line)
    # fig = go.Figure(data=data)
    fig.update_layout(
        xaxis_title='Wavelength',
        yaxis_title='Reflectance'
    )
    fig.update_layout(hovermode="x unified")
    # TODO
    # change the name according to the table name
    fig.write_html(batch_name + ".html")
     
    fig.show()
    