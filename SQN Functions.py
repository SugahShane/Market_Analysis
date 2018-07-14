import pandas as pd
import math


def SQN(period, percentBarChangeDataFrame):
    if(percentBarChangeDataFrame.count < period):
        raise Exception('Not enough data in data frame for period')

    avg = percentBarChangeDataFrame[0:period - 1].mean()
    stdev = percentBarChangeDataFrame[0:period - 1].std()

    multiplier = 0
    if period < 100:
        multiplier = math.sqrt(period)
    else:
        multiplier = 100

    return avg / stdev * multiplier


