import pandas as pd


def ATR(df):
    atr_df = pd.DataFrame()
    atr_df['ATR1'] = abs(df['high'] - df['low'])
    atr_df['ATR2'] = abs(df['high'] - df['close'].shift())
    atr_df['ATR3'] = abs(df['low'] - df['close'].shift())
    atr_df['TrueRange'] = atr_df[['ATR1', 'ATR2', 'ATR3']].max(axis=1)
    return atr_df['TrueRange']


def ATR_percent_of_close(df, period):
    df['ATR'] = ATR(df)
    df['ATR_Percent_Of_Close'] = df['ATR'] / df['close'] * 100
    return df['ATR_Percent_Of_Close'].rolling(window=period).mean().round(decimals=2)