import pandas as pd
import numpy as np
import time
import draw

ohlcv = pd.read_csv('ohlcv_data_15min.csv')
inflection_points = [[0]] # Store the timeframe of the inflection points using nested list
tail_up = {} # uptail
tail_down = {} # downtail 
positive_volume = negative_volume = 0
rise = True #indicate the trend of the price movement, True for rising, False for falling
time_period = 10 # Time period for calculating the average volume

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
    
    result = [sorted(box, reverse=True)[0] for box in result] #Taking the max value 
    return result

def trend_analysis(ohlcv, trend, strength):
    all_volumes = ohlcv['volume'].tolist()
    threshold = np.percentile(all_volumes, 80)

    top_20_volume = {
        box_id: vol
        for box_id, vol in trade_volume.items()
        if vol >= threshold
    }
    p_v = n_v = 0
    p_trend_strength = n_trend_strength = 0

    for i,k in top_20_volume.items():
        calc = ohlcv.loc[i, "open"] - ohlcv.loc[i, "close"]

        if calc > 0:
            n_v += abs(calc)
        else:
            p_v += abs(calc)

    if p_v > n_v:
        p_trend_strength = p_v/(p_v+n_v)
        trend = True
    else:
        n_trend_strength = n_v/(p_v+n_v)
        trend = False

    strength = abs(p_trend_strength - n_trend_strength) # 60% or higher holding huge dominance

    if trend == True:
        print("Increasing trend")
    else:
        print("Decreasing trend")
    
    if strength > 0.6:
        print("Huge dominance")
    elif strength > 0.1 and strength < 0.3:
        print("Weak dominacne")
    else:
        print("Normal")


def open_position(ohlcv, time_period, trend_lines, tail_up, tail_down):
    trade_volume = ohlcv['volume']
    total_trade_volume = sum(trade_volume) # Total trade volume
    current_price = 80000
    trend = True # Positive Trend by default
    strength = 0.0 # Strength of dominance
    #current_price = get_current_price('BTC/USDC:USDC') # Get the urrent price of BTC/USDC perpetual contract on Binance Futures
    temp = trend_lines.copy()
    temp.append(current_price)
    temp.sort()
    current_index = temp.index(current_price)

    price_level = (current_price - trend_lines[current_index-1]) / (trend_lines[current_index+1] - trend_lines[current_index - 1]) # Price level between the two closest trend lines
    
    trend_analysis(ohlcv, trend, strength)


    #단순히 위치보고 롱/숏 잡는 거 넘어서 방향을 고려해야함. 최근 가장 많은 거래가 터진 캔들을 또는 이전 캔들이 어땠는지 확인 필요
    #거래량이 많이 터진 캔들 파악하고 그 캔들이 속해있는 그룹도 확인
    #고점에 가까운지 저점에 가까운지 확인하고 전 캔들들의 롱숏 비율도 확인 필요. 
    
    if total_trade_volume < 3500: # Avg trade volume so expect moving sideways
        if price_level < 0.2: # Price is closer to the lower trend line so expect price to go up
            print("Open long position")
        elif price_level > 0.8: # Price is closer to the upper trend line so expect price to go down
            print("Open short position")
    elif total_trade_volume >= 5000: # High trade volume so expect trend breakout
       if price_level < 0.5: # Price is closer to the lower trend line so expect price to go up
           pass
    else:
        pass


for i in range(len(ohlcv)):
    if(ohlcv['open'].iloc[i] < ohlcv['close'].iloc[i]): # Price is rising
        tail_up[ohlcv['timestamp'].iloc[i]] = (ohlcv['low'].iloc[i] - ohlcv['open'].iloc[i])*0.4 + (ohlcv['volume'].iloc[i])*0.6 # Calculate the uptail
        positive_volume += ohlcv['volume'].iloc[i]
        if rise == False:
            z_score(inflection_points, i, ohlcv['open'].iloc[i]) # Passing inflection points and open price
            #DistanceBasedClustering(inflection_points, i, ohlcv['open'].iloc[i]) # Passing inflection points and open price
            rise = True
    elif (ohlcv['open'].iloc[i] > ohlcv['close'].iloc[i]): #Price is falling
        tail_down[ohlcv['timestamp'].iloc[i]] = (ohlcv['high'].iloc[i] - ohlcv['open'].iloc[i])*0.4 + (ohlcv['volume'].iloc[i])*0.6 # Calculate the downtail
        negative_volume += ohlcv['volume'].iloc[i]
        if rise == True:
            z_score(inflection_points, i, ohlcv['open'].iloc[i]) # Passing inflection points and open price
            #DistanceBasedClustering(inflection_points, i, ohlcv['open'].iloc[i]) # Passing inflection points and open price
            rise = False

tail_up_sorted = dict(sorted(tail_up.items(), key=lambda item: item[1], reverse=True)) # Sort the uptail dictionary by value in descending order
tail_down_sorted = dict(sorted(tail_down.items(), key=lambda item: item[1], reverse=True)) # Sort the downtail dictionary by value in descending order

trend_lines = box_construction(inflection_points) # Construct the trend lines based on the inflection points

#draw.plot_inflection_points(inflection_points, ohlcv, trend_lines)

open_position(ohlcv, time_period, trend_lines, tail_up_sorted, tail_down_sorted)

