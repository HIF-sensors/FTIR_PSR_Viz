import plotly.graph_objects as go

def viz(df):
    wavelengths = list(df.columns)[1:]
    data = []
    for index, row in df.iterrows():
        sample_name = list(row)[0]
        energy = list(row)[1:]
        graph = go.Line(x=wavelengths, y=energy, name = sample_name)
        data.append(graph)
    fig = go.Figure(data=data)
    fig.update_layout(
        xaxis_title='Wavelength',
        yaxis_title='Energy'
    )
    fig.update_layout(hovermode="x unified")
    fig.show()
    pass