import pandas as pd
import numpy as np
import time

ohlcv = pd.read_csv('ohlcv_data_15min.csv')
inflection_points = [[0]] # Store the timeframe of the inflection points using nested list 
rise = True #indicate the trend of the price movement, True for rising, False for falling

def z_score(inflection_list, open_price): # Calculate the z-score of the open price with respect to the list of inflection points
    if(len(inflection_list) < 2 or np.std(inflection_list[-1]) == 0): # If the list is empty or has zero standard deviation, add the open price as the first element
        inflection_list.append([open_price])
        return
    # Need to check the impact of the new point to the original list    
    arr = np.array(inflection_list[-1])
    mean = np.mean(arr)
    std = np.std(arr)
    z = (open_price - mean) / std
    if(abs(z) > 2): # If the z-score is greater than 2, it is considered an outlier
        inflection_list.append([open_price]) # Create a new box with the open price as the first element
    else:
        inflection_list[-1].append(open_price) # Add the open price to the current box
        
    

for i in range(len(ohlcv)):
    if(ohlcv['open'].iloc[i] < ohlcv['close'].iloc[i]): # Price is rising
        if rise == False:
              z_score(inflection_points, ohlcv['open'].iloc[i]) # Passing inflection points and open price
              rise = True
    elif (ohlcv['open'].iloc[i] > ohlcv['close'].iloc[i]): #Price is falling
        if rise == True:
            z_score(inflection_points, ohlcv['open'].iloc[i]) # Passing inflection points and open price 
            rise = False

print(inflection_points)

            




