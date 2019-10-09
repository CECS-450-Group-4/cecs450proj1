import json
import math
import os

# 1280x1024

def main():
  tree_data = getEyeDataList("p4.treeFXD.json")
  tree_points_data = cleanCoordinateData(tree_data)
  tree_angles_data = createAngles(tree_points_data)
  tree_relative_angles = generateRelativeAngleList(tree_angles_data)

  # print(tree_relative_angles)


  graph_data = getEyeDataList("p4.graphFXD.json")
  graph_points_data = cleanCoordinateData(graph_data)
  graph_angles_data = createAngles(graph_points_data)
  graph_relative_angles = generateRelativeAngleList(graph_angles_data)

  # print(graph_relative_angles)


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


def generateRelativeAngleList(listOfAngles):
  relativeAngles = []

  for points in listOfAngles:
    relativeAngles.append(calculateRelativeAngle(points))

  return relativeAngles




main()

