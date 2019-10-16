import json
import pprint
import os

files = ["p4GZD.json", "p4.graphGZD.json", "p4.treeGZD.json"]

def main():
    data = getEyeDataList("p4GZD.json")

    clean_data = cleanPupilData(data)
    
    pupil_average = 0

    for eyes in clean_data:
        pupil_average += ((eyes[1] + eyes[2])/2)
        
    pupil_baseline = pupil_average/len(clean_data)

    print("Baseline pupil size: ", pupil_baseline)

    tree_data = getEyeDataList("p4.treeGZD.json")
    clean_tree_data = cleanPupilData(tree_data)
    tree_variance_data = calcPupilVariance(pupil_baseline, clean_tree_data)

    # print(tree_variance_data)

    graph_data = getEyeDataList("p4.graphGZD.json")
    clean_graph_data = cleanPupilData(graph_data)
    graph_variance_data = calcPupilVariance(pupil_baseline, clean_graph_data)

    # print(graph_variance_data)


'''
    Returns a list containing the data from the json file.
'''
def getEyeDataList(fileName):
    with open(os.path.join(os.path.dirname(__file__), fileName), 'r') as json_file:
        data = json.load(json_file)

    json_file.close()

    return data

'''
    Given a list of raw gaze data, returns a list of clean tuples. 
    (Time, Left Pupil, Right Pupil)
'''
def cleanPupilData(raw_data):
    time = -1
    left = -1
    right = -1
    pupils = (time, left, right)
    pupil_data = []

    #[Time, Number, ScreenX (Right), ScreenY(Left), CamX, CamY, Distance(Left), Pupil(Left), Code
    #               ScreenX (Right), ScreenY(Right), CamX, CamY, Distnce(Right), Pupil(Right), Code]

    for row in raw_data:
        if(row[8] < 2 and row[15] < 2 ):
            time = row[0]
            left = row[7]
            right = row[14]
            pupils = (time, left, right)
            pupil_data.append(pupils)

    return pupil_data


'''
    Given a baseline number and a list of pupil data, will return a list of
    tuples. (Time, Average Variance)
'''
def calcPupilVariance(baseline, pupil_data):
    time = -1
    variance = -1
    entry = (time, variance)
    variance_data = []

    for row in pupil_data:
        time = row[0]
        variance = (((row[1] + row[2] / 2) - baseline) / baseline)
        entry = (time, variance)
        variance_data.append(entry)

    return variance_data


main()