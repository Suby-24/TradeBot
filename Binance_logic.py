import pandas as pd
import numpy as np

class BinanceLogic:
    def __init__(self, ohlcv_dataframe):
        """
        Initializes the analytical engine with the raw market dataset.
        All global state variables are encapsulated safely inside the class.
        """
        self.ohlcv = ohlcv_dataframe
        self.inflection_points = [[0]] 
        self.rise = True 
        
        # Calculate context-aware global variables dynamically based on data input
        temp_sorted = self.ohlcv.sort_values(by='close')
        self.p10 = temp_sorted['close'].quantile(0.10)
        self.p90 = temp_sorted['close'].quantile(0.90)

    def calc_inflection_points(self):
        """Processes the dataset sequentially to fill the inflection points list."""
        for i in range(len(self.ohlcv)):
            open_p = self.ohlcv['open'].iloc[i]
            close_p = self.ohlcv['close'].iloc[i]
            
            if open_p < close_p:  # Price is rising
                if not self.rise:
                    self._update_z_score(i, open_p)
                    self.rise = True
            elif open_p > close_p:  # Price is falling
                if self.rise:
                    self._update_z_score(i, open_p)
                    self.rise = False
        return self.inflection_points

    def _update_z_score(self, idx, open_price):
        """Internal helper method (indicated by underscore) to handle clustering mechanics."""
        if len(self.inflection_points[-1]) == 0:
            self.inflection_points[-1] = [idx]
            return
            
        temp = self.inflection_points[-1].copy()
        arr = np.array([self.ohlcv['open'].iloc[x] for x in temp])
        
        arr_max, arr_min = max(arr), min(arr)
        mean = np.mean(arr)
        std = np.std(arr)
        z = (open_price - mean) / std if std != 0 else 0

        dataset_normal_range = self.p90 - self.p10
        dataset_median = (self.p90 + self.p10) / 2
        dynamic_breakout_allowance = (dataset_normal_range / dataset_median) * 0.1

        upper_pct_change = (open_price - arr_max) / arr_max if arr_max != 0 else 0
        lower_pct_change = (arr_min - open_price) / arr_min if arr_min != 0 else 0

        if abs(z) > 2 or upper_pct_change > dynamic_breakout_allowance or lower_pct_change > dynamic_breakout_allowance:
            self.inflection_points.append([idx])
        else:
            self.inflection_points[-1].append(idx)

    def construct_boxes(self):
        """Constructs and returns key macro trend lines/boundaries."""
        arr = [sum([self.ohlcv['open'].iloc[x].item() for x in sub]) / len(sub) for sub in self.inflection_points]
        result = []
        sensitivity_factor = 0.45

        dataset_normal_range = self.p90 - self.p10
        dataset_median = (self.p90 + self.p10) / 2
        base_percentage_variance = (dataset_normal_range / dataset_median) * sensitivity_factor
        
        lower_bound_step = 1.0 - base_percentage_variance
        upper_bound_step = 1.0 + base_percentage_variance
        max_creep_allowance = base_percentage_variance * 1.3
        lower_bound_macro = 1.0 - max_creep_allowance
        upper_bound_macro = 1.0 + max_creep_allowance

        for i in arr:
            if not result:
                result.append([i])
            else:
                step_ok = result[-1][-1] * lower_bound_step <= i <= result[-1][-1] * upper_bound_step
                macro_ok = result[-1][0] * lower_bound_macro <= i <= result[-1][0] * upper_bound_macro
                
                if step_ok and macro_ok:
                    result[-1].append(i) 
                else:
                    result.append([i])
        
        return [sorted(box, reverse=True)[0] for box in result]

    def run_trend_analysis(self):
        """Analyzes directional strength using volume profiles."""
        trade_volume = self.ohlcv['volume']
        threshold = np.percentile(trade_volume.tolist(), 80)

        top_20_volume = {i: vol for i, vol in trade_volume.items() if vol >= threshold}
        p_v = n_v = 0

        for i, k in top_20_volume.items():
            calc = self.ohlcv.loc[i, "open"] - self.ohlcv.loc[i, "close"]
            if calc > 0:
                n_v += abs(calc)
            else:
                p_v += abs(calc)

        if p_v > n_v:
            trend_bool = True
            p_trend_strength = p_v / (p_v + n_v)
            n_trend_strength = 0
            print("Increasing trend")
        else:
            trend_bool = False
            n_trend_strength = n_v / (p_v + n_v)
            p_trend_strength = 0
            print("Decreasing trend")

        strength = abs(p_trend_strength - n_trend_strength)
        if strength > 0.6:
            print("Huge dominance")
        elif 0.1 < strength < 0.3:
            print("Weak dominance")
        else:
            print("Normal")
            
        return trend_bool, strength

    def get_past_8h_volume(self):
        """Calculates total trading volume for the past 8 hours (32 candles)."""
        lookback = 32
        if len(self.ohlcv) < lookback:
            return sum(self.ohlcv['volume'])
        return sum(self.ohlcv['volume'].iloc[-lookback:])

    def check_trade_opportunity(self, current_price, trend_lines):
        """Evaluates volume, trend markers, and positions to suggest an action."""
        total_trade_volume = self.get_past_8h_volume()
        print(f"Current 8H Volume: {total_trade_volume}")
        
        temp_lines = trend_lines.copy()
        temp_lines.append(current_price)
        temp_lines.sort()
        current_index = temp_lines.index(current_price)

        if current_index - 1 < 0 or current_index + 1 >= len(temp_lines):
            price_level = 0.5  # Boundary fallback default
        else:
            denom = temp_lines[current_index + 1] - temp_lines[current_index - 1]
            price_level = (current_price - temp_lines[current_index - 1]) / denom if denom != 0 else 0.5
        
        self.run_trend_analysis()
        print(f"Relative Price Level inside box: {price_level}")

        if 30000 < total_trade_volume < 75000:  # Sideways volume assumption range
            if price_level < 0.2:
                print("Signal: Open long position")
                return "LONG"
            elif price_level > 0.8:
                print("Signal: Open short position")
                return "SHORT"
        elif total_trade_volume >= 250000:  # Breakout volume confirmation range
            print("Signal: Trend breakout expected soon")
            return "BREAKOUT_WATCH"
        else:
            print("Signal: Market noise. Wait a minute.")
            return "HOLD"