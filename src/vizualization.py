import ast
import plotly.graph_objects as go
import plotly.express as px
import numpy as np
import cv2
import os

import hylite
from hylite import HyData, HyImage, HyCloud, HyLibrary, HyHeader, HyCollection, HyScene
from hylite import io

def create_masked_image(folder_path):
    '''
    This function will create a new RGB_masked.png image.
    The image size is similar to the sensors and it will 
    have masks with label as text on it.
    '''
    rgb_path = os.path.join(folder_path, 'RGB.png')
    mask_path = os.path.join(folder_path, 'mask.hdr')
    image = cv2.imread(rgb_path)
    mask = io.load(mask_path)
    # Resizing to sensor frame size
    new_width = image.shape[0] // 6
    new_height = image.shape[1] // 6
    new_image = cv2.resize(image, (new_height, new_width))

    # Add mask on image
    mask_data = mask.data.astype(np.uint8)
    mask_data = mask_data.T[0]
    contours, _ = cv2.findContours(mask_data, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    output_image = new_image

    for i, contour in enumerate(contours):
        x, y, w, h = cv2.boundingRect(contour)
        cv2.drawContours(output_image, [contour], -1, (0, 0, 255), 2)
        mask_value = mask_data[y + h // 2, x + w // 2]
        label_position = (x + w + 5, y + h // 2)  # Adjust position as needed
        cv2.putText(output_image, str(mask_value), label_position, cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 0, 0), 2)
    folder_location = os.path.dirname(rgb_path)
    cv2.imwrite(os.path.join(folder_location,'RGB_masked.png'), output_image)


def viz(batch_name, df_plot, fingerprint_library=None, reference_Spectrums=None,
        sensor='', download=True):
    fig = go.Figure()
    buttons = []
    start = 0
    end = start
    visible_dict = {}
    y_axis_dict = {}
    for key_index, (key, plots) in enumerate(df_plot.items()):
        df = plots[0]
        y_axis_dict[key] = plots[1]
        wavelengths = list(df.columns)[1:]
        data = []
        max_energy = df.iloc[:, 1:].max().max() # For plotting vertical lines
        min_energy = df.iloc[:, 1:].min().min() # For plotting vertical lines
        for index, row in df.iterrows():
            sample_name = list(row)[0]
            energy = list(row)[1:]
            graph = go.Scatter(x=wavelengths, y=energy, name = sample_name, mode='lines',
                               visible=(key_index == 0),
                            #    hoverinfo='x'
                               )
            data.append(graph)
            fig.add_trace(graph)
            end += 1
        
        # Visualisation for Reference Spectrum libraries
        if reference_Spectrums is not None:
            wavelengths = list(reference_Spectrums.columns)[1:]
            for index, row in reference_Spectrums.iterrows():
                polymer_name = row['polymer']
                energy = list(row)[1:]
                graph = go.Scatter(x=wavelengths, y=energy, name = polymer_name, mode='lines',
                                visible=(key_index == 0),
                                #    hoverinfo='x'
                                )
                data.append(graph)
                fig.add_trace(graph)
                end += 1
            
        
        # Visualisation for fingerprint libraries
        if fingerprint_library is not None:
            lib = fingerprint_library if sensor=='imaging' else fingerprint_library[fingerprint_library['sensor'] == sensor]
            unique_groups = lib['polymer'].unique()
            color_map = {group: px.colors.qualitative.Light24[i % len(px.colors.qualitative.Light24)] for i, group in enumerate(unique_groups)}
            for index, row in lib.iterrows():
                group_name = row['polymer']
                colour = row['colour']
                wavelengths = [float(x) for x in ast.literal_eval(row['wavelengths'])]
                for i, x_value in enumerate(wavelengths):
                    line = go.Scatter(
                        x=[x_value]*2,  # Duplicate x values for vertical lines
                        y=np.linspace(min_energy, max_energy, num=2).tolist(),  # Alternate y values for vertical lines
                        mode='lines+text',
                        name=group_name,
                        line={'color': colour},
                        legendgroup=group_name,
                        # showlegend=False,
                        showlegend=True if i == 0 else False,
                        visible=(key_index == 0),
                        textposition="top left",
                    )
                    # For library text
                    # fig.add_annotation(
                    #     x=x_value,
                    #     y=max_energy,
                    #     text=group_name,
                    #     textangle=-90,
                    #     showarrow=False,
                    #     font=dict(size=14)
                    # )
                    data.append(line)
                    fig.add_trace(line)
                    # Add a vertical line at x=2 using data coordinates
                    
                    end += 1

        visible_dict[key] = (start, end)
        start = end

        

        
    # Buttons for dropdown menu
    for dd_key, limit in visible_dict.items():
        visible = [False] * len(fig.data)
        visible[limit[0] : limit[1]] = [True] * (limit[1]-limit[0])
        buttons.append(dict(
            label=dd_key,
            method="update",
            args=[{"visible": visible},
                  {'yaxis': {'title': y_axis_dict[dd_key]}},
                    {"title": f"{batch_name} : {sensor} - {dd_key}"}]
        ))
    
    # fig.add_annotation(textangle=-90)
    # Add dropdown menu
    fig.update_layout(
        updatemenus=[go.layout.Updatemenu(
            buttons=buttons,
            direction="down",
            pad={"r": 10, "t": 10},
            showactive=False,
            x=0.1,
            xanchor="left",
            y=1.1,
            yanchor="top"
        )]
    )

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
    fig.update_traces(textposition='top center')

    if download:
        fig.write_html(text + ".html")
     
    fig.show()
    