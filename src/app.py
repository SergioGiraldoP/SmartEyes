#%%Libraries------------------------------------------------------------------------------------
#Dash
import dash
from dash import Dash, ctx
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State, ALL
import dash_bootstrap_components as dbc
import dash_leaflet as dl

#Plotly
#import plotly.express as px
import plotly.graph_objects as go

#json
#import json

#Pandas
import pandas as pd

#Pillow
from PIL import Image

#Matplotlib
#import matplotlib.pyplot as plt

#%%Back End--------------------------------------------------------------------------------------------------------------------
#Import Data Frame
Datos = pd.read_csv('Datos.csv')

#%%Detection Image---------------------------------------------------------------------------------------------------------------
#Strating image
pil_image = Image.open("Predictions/image-0001.jpg")
#%%Map--------------------------------------------------------------------------------------------------------------------------
#Base Layer

url_template = 'https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}'

#%%Marker Groups

no_detections = []
Senal_Curva = []
Senal_Preventiva = []
Senal_Reglamentaria = []
Senal_Guia = []
Marca_KM = []
Senal_Horizontal = []
Senal_Obstaculo = []
Cono = []
Senal_Blanca = []
Senal_Direccion = []
Senal_Informativa = []
Senal_PR = []


for i in range(0,len(Datos)):

    if Datos['Labels'][i] == '(no detections)':
        no_detections.append(dl.Marker(id=f'{i}', position=[Datos['Latitud'][i],Datos['Longitud'][i]], title="Sin Detección", riseOnHover=True, children=[dl.Tooltip(content="Sin Detección")]))
        
    elif Datos['Labels'][i] == 'Senal_Curva':
        Senal_Curva.append(dl.Marker(id=f'{i}', 
                                    position=[Datos['Latitud'][i],Datos['Longitud'][i]],
                                    title="Curva", 
                                    riseOnHover=True, 
                                    children=[dl.Tooltip(content=f'{Datos["Labels"][i]}')] 
                                              ))
            
    elif Datos['Labels'][i] == 'Senal_Preventiva':
        Senal_Preventiva.append(dl.Marker(id=f'{i}', position=[Datos['Latitud'][i],Datos['Longitud'][i]], title="Preventiva", riseOnHover=True, children=[dl.Tooltip(content="Preventiva")]))
        
    elif Datos['Labels'][i] == 'Senal_Reglamentaria':
        Senal_Reglamentaria.append(dl.Marker(id=f'{i}', position=[Datos['Latitud'][i],Datos['Longitud'][i]], title="Reglamentaria", riseOnHover=True, children=[dl.Tooltip(content="Reglamentaria")]))
        
    elif Datos['Labels'][i] == 'Senal_Guia':
        Senal_Guia.append(dl.Marker(id=f'{i}', position=[Datos['Latitud'][i],Datos['Longitud'][i]], title="Guía", riseOnHover=True, children=[dl.Tooltip(content="Guía")]))
        
    elif Datos['Labels'][i] == 'Marca_KM':
        Marca_KM.append(dl.Marker(id=f'{i}', position=[Datos['Latitud'][i],Datos['Longitud'][i]], title="Marca KM", riseOnHover=True, children=[dl.Tooltip(content="Marca KM")]))
        
    elif Datos['Labels'][i] == 'Senal_Horizontal':
        Senal_Horizontal.append(dl.Marker(id=f'{i}', position=[Datos['Latitud'][i],Datos['Longitud'][i]], title="Horizontal", riseOnHover=True, children=[dl.Tooltip(content="Horizontal")]))
        
    elif Datos['Labels'][i] == 'Senal_Obstaculo':
        Senal_Obstaculo.append(dl.Marker(id=f'{i}', position=[Datos['Latitud'][i],Datos['Longitud'][i]], title="Obstaculo", riseOnHover=True, children=[dl.Tooltip(content="Obstaculo")]))
        
    elif Datos['Labels'][i] == 'Cono':
        Cono.append(dl.Marker(id=f'{i}', position=[Datos['Latitud'][i],Datos['Longitud'][i]], title="Cono", riseOnHover=True, children=[dl.Tooltip(content="Cono")]))

    elif Datos['Labels'][i] == 'Senal_Blanca':
        Senal_Blanca.append(dl.Marker(id=f'{i}', position=[Datos['Latitud'][i],Datos['Longitud'][i]], title="Blanca", riseOnHover=True, children=[dl.Tooltip(content="Blanca")]))
        
    elif Datos['Labels'][i] == 'Senal_Direccion':
        Senal_Direccion.append(dl.Marker(id=f'{i}', position=[Datos['Latitud'][i],Datos['Longitud'][i]], title="Dirección", riseOnHover=True, children=[dl.Tooltip(content="Dirección")]))

    elif Datos['Labels'][i] == 'Senal_Informativa':
        Senal_Informativa.append(dl.Marker(id=f'{i}', position=[Datos['Latitud'][i],Datos['Longitud'][i]], title="Informativa", riseOnHover=True, children=[dl.Tooltip(content="Informativa")]))
        
    elif Datos['Labels'][i] == 'Senal_PR':
        Senal_PR.append(dl.Marker(id=f'{i}', 
                                  position=[Datos['Latitud'][i],Datos['Longitud'][i]], 
                                  title="PR", 
                                  riseOnHover=True, 
                                  children=[dl.Tooltip(content="PR")],
                                  clickData={'Image':f'{Datos["Image"][i]}'})) 
        

#%%3d Plot ---------------------------------------------------------------------------------------

fig = go.Figure(data=go.Scatter3d(
    x = Datos['Latitud'],
    y = Datos['Longitud'],
    z = Datos['Altitud'],
    marker=dict(
        size=1),
    line=dict(
        color='black',
        width=3),
    ))

fig.update_layout(template='simple_white')

#%%Layout------------------------------------------------------------------------------------------
app= Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])
server = app.server

app.layout = dbc.Container([ 
    
    html.Div([

        dbc.Row([
            dbc.Col([     
                dl.Map([ 
                    dl.LayersControl(
                        [dl.BaseLayer(dl.TileLayer(url=url_template), name='Esri Satellite', checked=True)] +
                        [dl.Overlay(dl.LayerGroup(no_detections), name='Sin Detecciión', checked=False),
                        dl.Overlay(dl.LayerGroup(Senal_Curva), name='Curva', checked=True),
                        dl.Overlay(dl.LayerGroup(Senal_Preventiva), name='Preventiva', checked=True),
                        dl.Overlay(dl.LayerGroup(Senal_Reglamentaria), name='Reglamentaria', checked=True),
                        dl.Overlay(dl.LayerGroup(Senal_Guia), name='Guía', checked=True),
                        dl.Overlay(dl.LayerGroup(Marca_KM), name='Marca KM', checked=True),
                        dl.Overlay(dl.LayerGroup(Senal_Horizontal), name='Horizontal', checked=True),
                        dl.Overlay(dl.LayerGroup(Senal_Obstaculo), name='Obstáculo', checked=True),
                        dl.Overlay(dl.LayerGroup(Cono), name='Cono', checked=True),
                        dl.Overlay(dl.LayerGroup(Senal_Blanca), name='Blanca', checked=True),
                        dl.Overlay(dl.LayerGroup(Senal_Direccion), name='Dirección', checked=True),
                        dl.Overlay(dl.LayerGroup(Senal_Informativa), name='Informativa', checked=True),
                        dl.Overlay(dl.LayerGroup(Senal_PR), name='PR', checked=True)
                        ]
                    )],
                    id='Mapa',
                    center=[4.87131969998978, -74.2903111799816],
                    zoom=13,
                    style={'height': '100vh', 'width':'66.7vw'})
            ],
            width=8,
            style={'margin':'0px', 'padding':'0'}),

            dbc.Col([
                dcc.Graph(
                    id='image_360_2',
                    figure=fig, 
                    style={'height': '50vh', 'width':'33.3vw'}),


                html.Img(
                    id='image_360',
                    src= pil_image,
                    style={'height': '50vh', 'width':'33.3vw'})


            ],
            width=3,
            style={'margin':'0px', 'padding':'0'})],
        )
    ])

],
fluid=True)

#%%
#Senal_Curva[0].id
#%%

#Callbacks


@app.callback(Output('image_360', 'src'),
              [Input(no_detections[i].id, 'clickData')for i in range(0,len(no_detections))],
              [Input(Senal_Curva[i].id, 'clickData')for i in range(0,len(Senal_Curva))],
              [Input(Senal_Preventiva[i].id, 'clickData')for i in range(0,len(Senal_Preventiva))],
              [Input(Senal_Reglamentaria[i].id, 'clickData')for i in range(0,len(Senal_Reglamentaria))],
              [Input(Senal_Guia[i].id, 'clickData')for i in range(0,len(Senal_Guia))],
              [Input(Marca_KM[i].id, 'clickData')for i in range(0,len(Marca_KM))],
              [Input(Senal_Horizontal[i].id, 'clickData')for i in range(0,len(Senal_Horizontal))],
              [Input(Senal_Obstaculo[i].id, 'clickData')for i in range(0,len(Senal_Obstaculo))],
              [Input(Cono[i].id, 'clickData')for i in range(0,len(Cono))],
              [Input(Senal_Blanca[i].id, 'clickData')for i in range(0,len(Senal_Blanca))],
              [Input(Senal_Direccion[i].id, 'clickData')for i in range(0,len(Senal_Direccion))],
              [Input(Senal_Informativa[i].id, 'clickData')for i in range(0,len(Senal_Informativa))],
              [Input(Senal_PR[i].id, 'clickData')for i in range(0,len(Senal_PR))]
              )

def imn_ret(*title):
    pil_image = Image.open("Predictions/image-0001.jpg")
    marker_id = dash.callback_context.triggered[0]['prop_id'].split(".")[0]
    if any(marker_id):
        Imagen = Datos['Image'][int(marker_id)]
        pil_image = Image.open(f"Predictions/{Imagen}")
    return pil_image



if __name__ == '__main__':
    app.run_server(debug=True)
# %%
