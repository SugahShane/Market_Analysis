from Data_Import.IEX_Data_Download import *
from Data_Import.CoinMarketCap_Data_Download import *
from Data_Import.Quandl_Data_Download import *
import pandas as pd
from datetime import datetime


START_DATE = datetime(2017, 1, 1)
END_DATE = datetime.now()
TODAY_DATE = datetime.now().strftime('%m-%d-%Y')
BASE_DIRECTORY = "D:\\Users\\Shane\\OneDrive\\Programming Projects\\Investing\\Market_Analysis\\"
DATA_DIRECTORY = BASE_DIRECTORY + "data\\"
EQUITY_PORTFOLIO_CSV_FILENAME = DATA_DIRECTORY + "PortfolioInstruments.csv"
CRYPTOCURRENCY_PORTFOLIO_CSV_FILENAME = DATA_DIRECTORY + "CoinMarketCapCryptocurrencyIDs.csv"
#OUTPUT_DIRECTORY = "D:\\Users\\Shane\\OneDrive\\Documents\\Trading\\Research\\Data\\Portfolio Data\\"
OUTPUT_DIRECTORY = BASE_DIRECTORY + "output\\"
OUTPUT_EXCEL_FILENAME = OUTPUT_DIRECTORY + "Portfolio Data.xlsx"


def write_excel_file(last_df, historical_df, cryptocurrency_last_price_df, commodity_df):
    print("Writing Excel File: " + OUTPUT_EXCEL_FILENAME)
    writer = pd.ExcelWriter(OUTPUT_EXCEL_FILENAME)
    last_df.to_excel(writer, 'Last Day')
    historical_df.to_excel(writer, 'Historical')
    cryptocurrency_last_price_df.to_excel(writer, 'Cryptocurrency')
    commodity_df.to_excel(writer, 'Commodities')
    writer.save()


portfolio_last_price_dict = get_last_prices_from_instruments_in_csv_file(EQUITY_PORTFOLIO_CSV_FILENAME)
portfolio_last_price_df = pd.DataFrame.from_dict([portfolio_last_price_dict])
portfolio_historical_price_df = get_historical_equity_prices_from_csv_file(EQUITY_PORTFOLIO_CSV_FILENAME,
                                                                           START_DATE,
                                                                           END_DATE)
cryptocurrency_last_price_df = \
    get_latest_cryptocurrency_portfolio_prices_from_coinmarketcap(CRYPTOCURRENCY_PORTFOLIO_CSV_FILENAME)
commodity_df = get_latest_commodity_prices_from_quandl()

write_excel_file(portfolio_last_price_df,
                 portfolio_historical_price_df,
                 cryptocurrency_last_price_df,
                 commodity_df)
