# Start hyperopt with the following command:
# freqtrade backtesting --config config.json --strategy RsiStrategy

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

class RsiStrategy(IStrategy):
    INTERFACE_VERSION = 2
    
    # Determine timeframe and # of candles before strategysignals becomes valid
    timeframe = '1d'
    startup_candle_count: int = 25

    # Determine roi take profit and stop loss points
    minimal_roi = {
        "0": 0.474,
        "4817": 0.241,
        "7799": 0.121,
        "29209": 0
    }

    stoploss = -0.226

    trailing_stop = False
    use_sell_signal = True
    sell_profit_only = False
    sell_profit_offset = 0.0
    ignore_roi_if_buy_signal = False

# --- Used indicators of strategy code ----
    def populate_indicators(self, dataframe: DataFrame, metadata: dict) -> DataFrame:

        # Add hyperopt parameter guards to dataframe
        dataframe['buy_rsi'] = 30
        dataframe['sell_rsi'] = 81

        dataframe['RSI'] = ta.RSI(dataframe, timeperiod=14)

        return dataframe

# --- Buy settings ---
    def populate_buy_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
       dataframe.loc[
            (
                (dataframe['RSI'] < dataframe['buy_rsi'] )
            ),
            'buy'] = 1

       return dataframe

# --- Sell settings ---
    def populate_sell_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
       dataframe.loc[
            (
                (dataframe['RSI'] > dataframe['sell_rsi'] )
            ),
            'sell'] = 1

       return dataframe

