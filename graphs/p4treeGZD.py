
##average - baseline / baseline
import json
import plotly
import plotly.graph_objects as go
import numpy as np

tuples_li = []
average_li = []
final_li = []
baseline_li = []
baselineholder = 0.0
final_holder = 0.0
difference_holder = 0.0

def get_figures(in_list):
    fig = 0.0
    for i in final_li:
        fig = "{:,.2f}".format(i)
        return fig

def print_list_formatted(in_list = []):
    for i in in_list:
        print("{:,.2f}".format(i), end = ' ')

with open('./json/p4treeGZD.json') as json_file:
    data = json.load(json_file)
    for p in data:
        if int(p['LeftCode']) < 2 and int(p['RightCode']) < 2:
            print('Time: ' + p['Time'])
            print('Left Pupil: ' + p['LeftPupil'])
            print('Right Pupil: ' + p['RightPupil'])
            tuple_holder = (int(p['Time']), float(p['LeftPupil']), float(p['RightPupil']))
            tuples_li.append(tuple_holder)
            print('')
    for i in tuples_li:
        print(i)
        
    for d in tuples_li:
        average_holder = (d[1] + d[2]) / 2
        average_li.append(average_holder)

    #print average_li
    print_list_formatted(average_li)
    print("\n\nThe size of average_li is: ", len(average_li))
    for k in average_li:
        final_holder = final_holder + k
    
    final_holder = final_holder / len(average_li)
    print("\nThe baseline is: ", "{:,.2f}".format(final_holder))

    for j in average_li:
        baselineholder = (j - final_holder) / final_holder
        baseline_li.append(baselineholder)
    
    for g in average_li:
        difference_holder = g - final_holder
        final_li.append(difference_holder)
        print("{:,.2f}".format(difference_holder), end = ' ')
        
    
    #---------------------------------------------------------------    
    
    # Create traces
    fig = go.Figure()
    xVals = np.arange(373)
        
    fig.add_trace(go.Scatter(x= xVals, y=average_li,
                    mode='lines',
                    name='Pupil Dilation'))
    fig.add_trace(go.Scatter(x=[3.29,373], y=[3.29,3.29], mode='lines', name='Pupil Baseline'))
    
    fig.show()
    plotly.offline.plot(fig, filename='p4treeGZD.html')