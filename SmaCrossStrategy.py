# Start hyperopt with the following command:
# freqtrade backtesting --config config.json --strategy SmaCrossStrategy

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

class SmaCrossStrategy(IStrategy):
    INTERFACE_VERSION = 2
    
    # Determine timeframe and # of candles before strategysignals becomes valid
    timeframe = '1d'
    startup_candle_count: int = 25

    # Determine roi take profit and stop loss points
    minimal_roi = {
        "0": 0.553,
        "8580": 0.377,
        "15227": 0.153,
        "45742": 0
    }

    stoploss = -0.239

    trailing_stop = False
    use_sell_signal = True
    sell_profit_only = False
    sell_profit_offset = 0.0
    ignore_roi_if_buy_signal = False

# --- Used indicators of strategy code ----
    def populate_indicators(self, dataframe: DataFrame, metadata: dict) -> DataFrame:

        dataframe['buy_quick_sma'] = ta.SMA(dataframe, timeperiod=15)
        dataframe['buy_slow_sma'] = ta.SMA(dataframe, timeperiod=40)
        dataframe['sell_quick_sma'] = ta.SMA(dataframe, timeperiod=11)
        dataframe['sell_slow_sma'] = ta.SMA(dataframe, timeperiod=48)
        
        return dataframe

# --- Buy settings ---
    def populate_buy_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
       dataframe.loc[
            (
                (qtpylib.crossed_above(dataframe['buy_quick_sma'], dataframe['buy_slow_sma']))
            ),
            'buy'] = 1
       return dataframe

# --- long settings ---
    def populate_sell_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
       dataframe.loc[
            (
                (qtpylib.crossed_below(dataframe['sell_quick_sma'], dataframe['sell_slow_sma']))
            ),
            'sell'] = 1
       return dataframe

