import pandas as pd
import numpy as np
import time
import draw

ohlcv = pd.read_csv('ohlcv_data_15min.csv')
inflection_points = [[0]] # Store the timeframe of the inflection points using nested list
tail_up = {} # uptail
tail_down = {} # downtail 
rise = True #indicate the trend of the price movement, True for rising, False for falling

def z_score(inflection_list, idx, open_price): # Calculate the z-score of the open price with respect to the list of inflection points
    if(len(inflection_list[-1]) == 0):
        inflection_list[-1] = [idx] # Create a new box with the idx as the first element
        return
    elif(len(inflection_list[-1]) == 1): # If the list has only one box with one element, add the open price to the current box
        inflection_list[-1].append(idx)
        return
    # Need to check the impact of the new point to the original list        
    arr = np.array([ohlcv['open'].iloc[x] for x in inflection_list[-1]]) # Convert the list of inflection points to a numpy array
    mean = np.mean(arr)
    std = np.std(arr)

    z = (open_price - mean) / std if std != 0 else 0

    if(abs(z) > 2): # If the z-score is greater than 2, it is considered an outlier
        inflection_list.append([idx]) # Create a new box with the idx as the first element
    else:
        inflection_list[-1].append(idx) # Add the open price to the current box
        
def DistanceBasedClustering(inflection_list, idx, open_price): # Perform distance-based clustering on the inflection points
    if(len(inflection_list[-1]) == 0):
        inflection_list[-1] = [idx] # Create a new box with the idx as the first element
        return
    elif(len(inflection_list[-1]) == 1): # If the list has only one box with one element, add the open price to the current box
        inflection_list[-1].append(idx)
        return
    # Need to check the distance of the new point to the original list    
    arr = np.array(inflection_list[-1])
    
    mean = np.mean(arr)
    max_point = np.max(arr)
    min_point = np.min(arr)
    range = np.ptp(arr)
    median = np.median(arr)

def box_construction(inflection_list):
    arr = [sum([ohlcv['open'].iloc[x].item() for x in sub]) / len(sub) for sub in inflection_list]
    arr.sort()
    result = []
    for i in arr:
        if not result:
            result.append([i])
        else:
            if result[-1][0] * 0.985 <= i <= result[-1][0] * 1.015:
                result[-1].append(i) # Add the new point to the current box if it is within 2% of the first element in the current box
            else:
                result.append([i]) # Create a new box with the new point as the first element 
    result = [sum(box) / len(box) for box in result] # Take the average of each box to get the final price level
    return result   
     
    
for i in range(len(ohlcv)):
    if(ohlcv['open'].iloc[i] < ohlcv['close'].iloc[i]): # Price is rising
        tail_up[ohlcv['timestamp'].iloc[i]] = ohlcv['low'].iloc[i] - ohlcv['open'].iloc[i] # Calculate the uptail
        if rise == False:
            z_score(inflection_points, i, ohlcv['open'].iloc[i]) # Passing inflection points and open price
            #DistanceBasedClustering(inflection_points, i, ohlcv['open'].iloc[i]) # Passing inflection points and open price
            rise = True
    elif (ohlcv['open'].iloc[i] > ohlcv['close'].iloc[i]): #Price is falling
        tail_down[ohlcv['timestamp'].iloc[i]] = ohlcv['high'].iloc[i] - ohlcv['open'].iloc[i] # Calculate the downtail
        if rise == True:
            z_score(inflection_points, i, ohlcv['open'].iloc[i]) # Passing inflection points and open price
            #DistanceBasedClustering(inflection_points, i, ohlcv['open'].iloc[i]) # Passing inflection points and open price
            rise = False

tail_up_sorted = dict(sorted(tail_up.items(), key=lambda item: item[1], reverse=True)) # Sort the uptail dictionary by value in descending order
tail_down_sorted = dict(sorted(tail_down.items(), key=lambda item: item[1], reverse=True)) # Sort the downtail dictionary by value in descending order

draw.plot_inflection_points(inflection_points, ohlcv, box_construction(inflection_points))


