import plotly.graph_objects as go

def viz(df):
    wavelengths = list(df.columns)[1:]
    data = []
    for index, row in df.iterrows():
        sample_name = list(row)[0]
        energy = list(row)[1:]
        graph = go.Scatter(x=wavelengths, y=energy, name = sample_name, mode='lines')
        data.append(graph)
    fig = go.Figure(data=data)
    fig.update_layout(
        xaxis_title='Wavelength',
        yaxis_title='Reflectance'
    )
    fig.update_layout(hovermode="x unified")
    # TODO
    # change the name according to the table name
    fig.write_html("T16.html")
     
    fig.show()
    