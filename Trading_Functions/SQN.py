import numpy as np
import pandas as pd
import math

STRONG_BULL_SQN = 1.5
BULL_SQN = 0.7
NEUTRAL_SQN = 0
BEAR_SQN = -0.45

VERY_VOLATILE_ATR = 3.5
VOLATILE_ATR = 1.65
NORMAL_ATR = 1


def sqn(df, period):
    if len(df.index) < period:
        raise Exception('Not enough data in data frame for period')

    percent_change_df = (df - df.shift()) / df.shift()
    avg_df = percent_change_df.rolling(window=period).mean()
    stdev_df = percent_change_df.rolling(window=period).std()

    multiplier = 0
    if period < 100:
        multiplier = math.sqrt(period)
    else:
        multiplier = 10

    return (avg_df / stdev_df * multiplier).round(decimals=2)


def market_classification(df):
    return df.apply(get_market_classification, axis=1)


def get_market_classification(row):
    if row["SQN_100"] > STRONG_BULL_SQN:
        sqn100_market_category = "Strong Bull"
    elif row["SQN_100"] > BULL_SQN:
        sqn100_market_category = "Bull"
    elif row["SQN_100"] > NEUTRAL_SQN:
        sqn100_market_category = "Neutral"
    elif row["SQN_100"] > BEAR_SQN:
        sqn100_market_category = "Bear"
    else:
        sqn100_market_category = "Strong Bear"

    if row["ATR_Percent_Of_Close"] > VERY_VOLATILE_ATR:
        sqn100_market_category += " Very Volatile"
    elif row["ATR_Percent_Of_Close"] > VOLATILE_ATR:
        sqn100_market_category += " Volatile"
    elif row["ATR_Percent_Of_Close"] > NORMAL_ATR:
        sqn100_market_category += " Normal"
    else:
        sqn100_market_category += " Quiet"

    return sqn100_market_category
