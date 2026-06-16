
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

def box_construction(inflection_list):
    arr = [sum([ohlcv['open'].iloc[x].item() for x in sub]) / len(sub) for sub in inflection_list]
    arr.sort()
    result = []
    lower_bound = 0.985 # For 15min
    upper_bound = 1.015 # For 15min

    for i in arr:
        if not result:
            result.append([i])
        else:
            if result[-1][0] * lower_bound <= i <= result[-1][0] * upper_bound:
                result[-1].append(i) # Add the new point to the current box if it is within 2% of the first element in the current box
            else:
                result.append([i]) # Create a new box with the new point as the first element 
    
    result = [sum(box) / len(box) for box in result] # Take the average of each box to get the final price level
    
    return result

