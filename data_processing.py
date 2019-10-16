import numpy as np
import pandas as pd
from pathlib import Path
import plotly.graph_objects as go
import plotly.express as px
import math
from plotly.subplots import make_subplots
from Calculate_Angle import calculateAngles

def load_file(path, names):
    if not path.is_file():
        raise FileNotFoundError(str(path))
        
    data = pd.read_csv(path, sep="\t", names=names, header=None)
    return data

def load_datasets():
    EVD_cols = ["time", "event", "event_key", "data_1", "data_2", "description"]
    FXD_cols = ["fix_number", "timestamp", "duration", "gazepoint_x", "gazepoint_y"]
    GZD_cols = ["timestamp", "number", "gazepoint_X_L" ,"gazepoint_Y_L", "cam_X_L", "cam_Y_L",
                "distance_L", "pupil_L", "validity_L", "gazepoint_X_R",
                "gazepoint_Y_R", "cam_X_R", "cam_Y_R", "distance_R", "pupil_R", 
                 "validity_R"]
    path = Path.cwd() / "p4"
    graphEVD = load_file(path / "p4.graphEVD.txt", EVD_cols)
    graphFXD = load_file(path / "p4.graphFXD.txt", FXD_cols)
    graphGZD = load_file(path / "p4.graphGZD.txt", GZD_cols)
    treeEVD = load_file(path / "p4.treeEVD.txt", EVD_cols)
    treeFXD = load_file(path / "p4.treeFXD.txt", FXD_cols)
    treeGZD = load_file(path / "p4.treeGZD.txt", GZD_cols)
    GZD = load_file(path /"p4GZD.txt", GZD_cols)
    return graphEVD, graphFXD, graphGZD, treeEVD, treeFXD, treeGZD, GZD

def remove_invalid_data(GZD):
    indexNames = GZD[(GZD['validity_L'] > 0) | (GZD['validity_R'] > 0)].index
    GZD.drop(indexNames, inplace=True)
    return GZD

def l_r_dilation(GZD):
    x =  round((GZD['pupil_R'].add(GZD['pupil_L'])).div(2), 4)
    avg = round(x.mean(), 4)
    x.fillna(avg)
    return x

def add_dilation_to_fxd(GZD, FXD):
    GZD['dilation'] = l_r_dilation(GZD)
    FXD = pd.merge_ordered(FXD, GZD[['timestamp', 'dilation']], fill_method='ffill', left_by='timestamp')
    avg = FXD['dilation'].mean()
    FXD['dilation'] = FXD['dilation'].fillna(avg)
    return FXD

def add_angles_to_fxd(graphFXD, treeFXD):
    graph_relative_angle, tree_relative_angle, graph_absolute_angle, tree_absolute_angle = calculateAngles()
    graphFXD['relative_angle'] = graph_relative_angle
    treeFXD['relative_angle'] = tree_relative_angle
    graphFXD['absolute_angle'] = graph_absolute_angle
    treeFXD['absolute_angle'] = tree_absolute_angle
    return graphFXD, treeFXD


def hover(FXD):
    hover_text = []

    for index, row in FXD.iterrows():
        hover_text.append(('Relative Angle: {relative_angle}<br>'+
                            'Absolute Angle: {absolute_angle}<br>'+
                            'Pupil Dilation: {dilation}<br>')
                            .format(relative_angle=row['relative_angle'], 
                            absolute_angle=row['absolute_angle'],
                            dilation=row['dilation']))
    return hover_text


graphEVD, graphFXD, graphGZD, treeEVD, treeFXD, treeGZD, GZD = load_datasets()

graphGZD = remove_invalid_data(graphGZD)
treeGZD = remove_invalid_data(treeGZD)
GZD = remove_invalid_data(GZD)

graphFXD = add_dilation_to_fxd(graphGZD, graphFXD)
treeFXD = add_dilation_to_fxd(treeGZD, treeFXD)

graphFXD, treeFXD = add_angles_to_fxd(graphFXD, treeFXD)

graphFXD['text'] = hover(graphFXD)
treeFXD['text'] = hover(treeFXD)

print(graphFXD)
print(treeFXD)

sizeref = 4*graphFXD['dilation'].max()/(1000)

fig = make_subplots(rows=2, cols=1, shared_xaxes=True,
        subplot_titles=("Graph Visualization Fixation Duration v. Saccade Length",
        "Tree Visualization Fixation Duration v. Saccade Length"))

fig.add_trace(go.Scatter(x=graphFXD['relative_angle'], y=graphFXD['absolute_angle'],
    text = graphFXD['text'], marker_size=graphFXD['dilation']), row=1,col=1)
fig.add_trace(go.Scatter(x=treeFXD['relative_angle'], y=treeFXD['absolute_angle'],
    text = treeFXD['text'], marker_size=treeFXD['dilation']), row=2,col=1)

fig.update_traces(mode='markers', marker=dict(sizemode='area', sizeref=sizeref, line_width=2))

fig.update_layout(
    title_text='Comparison of Graph and Tree Visualizations',
    xaxis=dict(title='Relative Angle (degrees)', gridcolor='white', gridwidth=2,),
    yaxis=dict(title='Absolute Angle (degrees)', gridcolor='white', gridwidth=2,),
    paper_bgcolor='rgb(243, 243, 243)',
    plot_bgcolor='rgb(243, 243, 243)',
)

fig.show()
