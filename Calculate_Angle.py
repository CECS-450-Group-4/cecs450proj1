import json
import math
import os
from pathlib import Path

# 1280x1024

def main():
  tree_relative_angles = generateRelativeAngleList()

  graph_relative_angles = generateRelativeAngleList()



'''
  Returns a list containing the data from the json file.
'''
def getEyeDataList(fileName):
  with open(os.path.join(os.path.dirname(__file__), fileName), 'r') as json_file:
    data = json.load(json_file)

  json_file.close()

  return data


def cleanCoordinateData(raw_data):
  # [Number, Time, Duration, X, Y]
  # Screen size = 1280x1024
  # X if from the left of the screen
  # Y is from the top of the screen
  # To use cartesian coordinate Y = 1024 - Y

  coordinates = []

  for row in raw_data:
    x = row[3]
    y = 1024 - row[4]
    row = (x, y)

    coordinates.append(row)

  return coordinates

# Creates a group of 3 points to calculate the inner angle.
def createAngles(points):
  angles = []
  for i in range(len(points) - 2):
    angles.append((points[i], points[i+1], points[i+2]))

  return angles


def createAngles2(points):
  angles = []
  for i in range(len(points) - 2):
    angles.append((points[i], points[i+1]))

  return angles

# Calculates the relative angle of the 3 given points.
def calculateRelativeAngle(anglePoints):
  a = anglePoints[0]
  b = anglePoints[1]
  c = anglePoints[2]

  ang = math.degrees(
    math.atan2(c[1]-b[1], c[0]-b[0]) - math.atan2(a[1]-b[1], a[0]-b[0]))

  ang = round(ang) # Attempted to round 2 decimals a very small number past 2 was produced.

  # Makes sure the angle is positive.
  if(ang < 0):
    ang = ang + 360
  
  # Makes sure we are always getting the acute angle.
  if(ang > 180):
    ang = 360 - ang

  return ang


def generateRelativeAngleList():
  graph_file = Path.cwd() / "p4.graphFXD.json"
  tree_file = Path.cwd() / "p4.treeFXD.json"

  graph_data = getEyeDataList(graph_file)
  tree_data = getEyeDataList(tree_file)

  graph_points_data = cleanCoordinateData(graph_data)
  tree_points_data = cleanCoordinateData(tree_data)

  graph_angles_data = createAngles(graph_points_data)
  tree_angles_data = createAngles(tree_points_data)
  
  graph_relative_angles = []
  tree_relative_angles = []

  for points in graph_angles_data:
    graph_relative_angles.append(calculateRelativeAngle(points))

  for points in tree_angles_data:
    tree_relative_angles.append(calculateRelativeAngle(points))

  g_ra_av = sum(graph_relative_angles) / len(graph_relative_angles)
  t_ra_av = sum(tree_relative_angles) / len(tree_relative_angles)

  graph_relative_angles.insert(0, g_ra_av)
  tree_relative_angles.insert(0,t_ra_av)
  graph_relative_angles.append(g_ra_av)
  tree_relative_angles.append(t_ra_av)
  return graph_relative_angles, tree_relative_angles

# Calculate dot product of two points
def dot_product(a, b):
  #  Uses the x and y coordinates of both points
  return a[0]*b[0]+a[1]*b[1]

# Calculate the saccade length between two points
def length(x):
  return math.sqrt(x[0]**2+x[1]**2)

def calculateAbsoluteAngle(anglePoints):
  a = anglePoints[0] # Get angle point 1
  b = anglePoints[1] # Get angle point 2
  cosx = dot_product(a, b) / (length(a) * length(b)) # Calc cosine
  rad = math.acos(cosx) # Get radians
  deg = rad * 180 / math.pi # Convert rad to degrees
  deg = round(deg) # Round decimal500
  return deg

# Returns list of absolute angles
def generateAbsoluteAngleList():

  graph_file = Path.cwd() / "p4.graphFXD.json"
  tree_file = Path.cwd() / "p4.treeFXD.json"

  graph_data = getEyeDataList(graph_file)
  tree_data = getEyeDataList(tree_file)

  graph_points_data = cleanCoordinateData(graph_data)
  tree_points_data = cleanCoordinateData(tree_data)

  graph_angles_data = createAngles(graph_points_data)
  tree_angles_data = createAngles(tree_points_data)
  
  graph_absolute_angles = []
  tree_absolute_angles = []

  for points in graph_angles_data:
    graph_absolute_angles.append(calculateAbsoluteAngle(points))

  for points in tree_angles_data:
    tree_absolute_angles.append(calculateAbsoluteAngle(points))

  g_aa_av = sum(graph_absolute_angles) / len(graph_absolute_angles)
  t_aa_av = sum(tree_absolute_angles) / len(tree_absolute_angles)
  graph_absolute_angles.insert(0, g_aa_av)
  tree_absolute_angles.insert(0,t_aa_av)
  graph_absolute_angles.append(g_aa_av)
  tree_absolute_angles.append(t_aa_av)

  return graph_absolute_angles, tree_absolute_angles


def calculateAngles():
  a,b = generateRelativeAngleList()
  c,d = generateAbsoluteAngleList()
  return a,b,c,d

main()

