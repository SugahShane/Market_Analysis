from iexfinance import get_historical_data
from datetime import datetime
import pandas as pd
import time


START_DATE = datetime(2018, 1, 1)
END_DATE = datetime.now()
BASE_DIRECTORY = "D:\\Users\\Shane\\Dropbox\\PyCharm Projects\\Market_Analysis\\"
DATA_DIRECTORY = BASE_DIRECTORY + "data\\"
#INPUT_DATA_FILENAME = "MarketDashboardInstruments.csv"
#INPUT_DATA_FILENAME = "PortfolioInstruments.csv"
INPUT_DATA_FILENAME = "TestData.csv"
OUTPUT_DIRECTORY = BASE_DIRECTORY + "output\\"
OUTPUT_EXCEL_FILENAME = "Market Data.xlsx"

def read_equity_list_from_csv():
    print("Reading data file: " + DATA_DIRECTORY + INPUT_DATA_FILENAME)
    df = pd.read_csv(DATA_DIRECTORY + INPUT_DATA_FILENAME)
    return df


def get_equity_price_data(instruments_df):
    instruments_price_data_df = pd.DataFrame()
    for row in instruments_df.itertuples():
        print("Processing: " + getattr(row, "Instrument"))
        try:
            instrument_df = get_historical_data(getattr(row, 'Instrument'),
                                                start=START_DATE,
                                                end=END_DATE,
                                                output_format='pandas')
            instrument_df = instrument_df.assign(Instrument=getattr(row, 'Instrument'))
            instruments_price_data_df = instruments_price_data_df.append(instrument_df, ignore_index=True)
        except Exception:
            print("Could not process " + getattr(row, "Instrument"))
        time.sleep(.5)
    return instruments_price_data_df


def get_cryptocurrency_price_data():
    print("Processing Cryptocurrencies")


instruments_df = read_equity_list_from_csv()
instruments_price_data_df = get_equity_price_data(instruments_df)
#print(instruments_price_data_df.head(20))
