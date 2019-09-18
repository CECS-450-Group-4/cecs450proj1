import numpy as np
import pandas as pd
from pathlib import Path

def load_file(path, names):
    if not path.is_file():
        raise FileNotFoundError(str(path))
        
    data = pd.read_csv(file, sep="\t", names=names, header=None)
    return data

EVD_cols = ["time", "event", "event_key", "data_1", "data_2", "description"]
FXD_cols = ["fix_number", "timestamp", "duration", "gazepoint_x", "gazepoint_y"]
GZD_cols = ["gazepoint_X_L" ,"gazepoint_Y_L", "cam_X_L", "cam_Y_L",
                "distance_L", "pupil_L", "validity_L", "gazepoint_X_R",
                "gazepoint_Y_R", "cam_X_R", "cam_Y_R", "distance_R", "pupil_R", 
                 "validity_R"]

path = Path.cwd() / "p4"

file = path / "p4.graphEVD.txt"
graphEVD = load_file(file, EVD_cols)

file = path / "p4.graphFXD.txt"
graphFXD = load_file(file, FXD_cols)

file = path / "p4.graphGZD.txt"
graphGZD = load_file(file, GZD_cols)

file = path / "p4.treeEVD.txt"
treeEVD = load_file(file, EVD_cols)

file = path / "p4.treeFXD.txt"
treeFXD = load_file(file, FXD_cols)

file = path / "p4.treeGZD.txt"
treeGZD = load_file(file, GZD_cols)

print(graphGZD)

indexNames = graphGZD[(graphGZD['validity_L'] >= 2) | (graphGZD['validity_R'] >= 2)].index
graphGZD.drop(indexNames, inplace=True)
print(graphGZD)