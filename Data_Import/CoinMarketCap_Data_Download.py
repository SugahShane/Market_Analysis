from coinmarketcap.clients import CoinMarketCapClient
import pandas as pd
import time


BASE_DIRECTORY = "D:\\Users\\Shane\\OneDrive\\PyCharm Projects\\Market_Analysis\\"
DATA_DIRECTORY = BASE_DIRECTORY + "data\\"
INPUT_DATA_FILENAME = DATA_DIRECTORY + "CryptocurrencyInstruments.csv"
SLEEP_PERIOD = 0.5
client = CoinMarketCapClient()


def get_cryptocurrency_list_from_csv(filename_and_path):
    print("Reading data file: " + filename_and_path)
    df = pd.read_csv(filename_and_path)
    return df


def get_latest_cryptocurrency_portfolio_prices(filename_and_path=INPUT_DATA_FILENAME):
    instruments_df = get_cryptocurrency_list_from_csv(filename_and_path)
    for row in instruments_df.itertuples():
        instrument = getattr(row, 'Instrument')
        print("Processing: " + instrument)
        instrument_df = client.cryptocoin.get(symbol=instrument)
        instruments_price_data_df = instruments_price_data_df.append(instrument_df, ignore_index=True)
        time.sleep(SLEEP_PERIOD)
    return instruments_price_data_df
