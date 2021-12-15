# Start hyperopt with the following command:
# freqtrade hyperopt --config config.json --hyperopt-loss SharpeHyperOptLoss --strategy RsiStrat -e 500 --spaces  buy sell --random-state 8711

# --- Do not remove these libs ---
import numpy as np  # noqa
import pandas as pd  # noqa
from functools import reduce
from pandas import DataFrame

from freqtrade.strategy import (BooleanParameter, CategoricalParameter, DecimalParameter,IStrategy, IntParameter)

# --- Add your lib to import here ---
import talib.abstract as ta
import freqtrade.vendor.qtpylib.indicators as qtpylib

# --- Generic strategy settings ---

class SmaCrossStrat(IStrategy):
    INTERFACE_VERSION = 2
    
    # Determine timeframe and # of candles before strategysignals becomes valid
    timeframe = '1d'
    startup_candle_count: int = 25

    # Determine roi take profit and stop loss points
    minimal_roi = {
        "60":  0.01,
        "30":  0.03,
        "20":  0.04,
        "0":  0.05
    }

    stoploss = -0.10
    trailing_stop = False
    use_sell_signal = True
    sell_profit_only = False
    sell_profit_offset = 0.0
    ignore_roi_if_buy_signal = False

# --- Define spaces for the indicators ---

    # Buy space
    buy_quick_sma = IntParameter(5, 60, default=20, space="buy")
    buy_slow_sma = IntParameter(5, 60, default=20, space="buy")

    # Sell space
    sell_quick_sma = IntParameter(5, 60, default=20, space="sell")
    sell_slow_sma = IntParameter(5, 60, default=20, space="sell")


# --- Used indicators of strategy code ----
    def populate_indicators(self, dataframe: DataFrame, metadata: dict) -> DataFrame:

        # SMA's for buying
        for val in self.buy_quick_sma.range:
            dataframe[f'buy_quick_sma_{val}'] = ta.SMA(dataframe, timeperiod=val)
        for val in self.buy_slow_sma.range:
            dataframe[f'buy_slow_sma_{val}'] = ta.SMA(dataframe, timeperiod=val)

        # SMA's for selling
        for val in self.sell_quick_sma.range:
            dataframe[f'sell_quick_sma_{val}'] = ta.SMA(dataframe, timeperiod=val)
        for val in self.sell_slow_sma.range:
            dataframe[f'sell_slow_sma_{val}'] = ta.SMA(dataframe, timeperiod=val)

        return dataframe

# --- Buy settings ---
    def populate_buy_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
       conditions = []
       conditions.append(qtpylib.crossed_above(
        dataframe[f'buy_quick_sma_{self.buy_quick_sma.value}'],
        dataframe[f'buy_quick_sma_{self.buy_slow_sma.value}']
        ))

       if conditions:
           dataframe.loc[
               reduce(lambda x, y: x & y, conditions),
               'buy'] = 1

       return dataframe

# --- long settings ---
    def populate_sell_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
       conditions = []
       conditions.append(qtpylib.crossed_below(
        dataframe[f'buy_quick_sma_{self.sell_quick_sma.value}'],
        dataframe[f'buy_quick_sma_{self.sell_slow_sma.value}']
        ))

       if conditions:
           dataframe.loc[
               reduce(lambda x, y: x & y, conditions),
               'sell'] = 1

       return dataframe

