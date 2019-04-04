from iexfinance import *
from datetime import datetime
import pandas as pd
import time


START_DATE = datetime(2017, 1, 1)
END_DATE = datetime.now()
BASE_DIRECTORY = "D:\\Users\\Shane\\OneDrive\\PyCharm Projects\\Market_Analysis\\"
DATA_DIRECTORY = BASE_DIRECTORY + "data\\"
#INPUT_DATA_FILENAME = "MarketDashboardInstruments.csv"
#INPUT_DATA_FILENAME = "PortfolioInstruments.csv"
INPUT_DATA_FILENAME = "TestData.csv"
OUTPUT_DIRECTORY = BASE_DIRECTORY + "output\\"
OUTPUT_EXCEL_FILENAME = "Market Data.xlsx"
SLEEP_PERIOD = 0.1

def read_equity_list_from_csv(filename_and_path):
    print("Reading data file: " + filename_and_path)
    df = pd.read_csv(filename_and_path)
    return df


def get_instrument_list_historical_price_data(instruments_df, start_date=START_DATE, end_date=END_DATE):
    instruments_price_data_df = pd.DataFrame()
    for row in instruments_df.itertuples():
        instrument_df = get_historical_price_data_from_iex(getattr(row, 'Instrument'), start_date, end_date)
        instrument_df['Date'] = instrument_df.index.values
        instruments_price_data_df = instruments_price_data_df.append(instrument_df, ignore_index=True, sort=True)
        time.sleep(SLEEP_PERIOD)
    return instruments_price_data_df


def get_historical_price_data_from_iex(instrument, start_date=START_DATE, end_date=END_DATE):
    print("Processing: " + instrument)
    try:
        instrument_df = stocks.get_historical_data(instrument,
                                            start=start_date,
                                            end=end_date,
                                            output_format='pandas')
        instrument_df = instrument_df.assign(Instrument=instrument)
    except Exception:
        print("Could not process " + instrument)
    return instrument_df


def get_last_price_from_iex(instrument):
    print("Processing: " + instrument)
    stock = stocks.Stock(instrument)
    return stock.get_price()


def get_batch_last_price_from_iex(instruments_df):
    return stocks.Stock(instruments_df['Instrument'].values.tolist()).get_price()


def get_historical_equity_prices_from_csv_file(filename, start_date=START_DATE, end_date=END_DATE):
    instruments_df = read_equity_list_from_csv(filename)
    return get_instrument_list_historical_price_data(instruments_df, start_date, end_date)


def get_historical_monthly_equity_prices_from_csv_file(filename, start_date=START_DATE, end_date=END_DATE):
    instruments_df = get_historical_equity_prices_from_csv_file(filename, start_date, end_date)

    # Filter down to only the price at the start of each month
    instruments_df.sort_index(inplace=True)


def get_last_prices_from_instruments_in_csv_file(filename):
    instruments_df = read_equity_list_from_csv(filename)
    return get_batch_last_price_from_iex(instruments_df)


