from Data_Import.IEX_Data_Download import *


START_DATE = datetime(2017, 1, 1)
END_DATE = datetime.now()
TODAY_DATE = datetime.now().strftime('%m-%d-%Y')
BASE_DIRECTORY = "D:\\Users\\Shane\\OneDrive\\PyCharm Projects\\Market_Analysis\\"
DATA_DIRECTORY = BASE_DIRECTORY + "data\\"
PORTFOLIO_CSV_FILENAME = DATA_DIRECTORY + "PortfolioInstruments.csv"
OUTPUT_DIRECTORY = "D:\\Users\\Shane\\OneDrive\\Documents\\Trading\\Research\\Data\\Portfolio Data\\"
OUTPUT_EXCEL_FILENAME = OUTPUT_DIRECTORY + "Portfolio Data.xlsx"


def write_excel_file(last_df, historical_df):
    print("Writing Excel File: " + OUTPUT_EXCEL_FILENAME)
    writer = pd.ExcelWriter(OUTPUT_EXCEL_FILENAME)
    last_df.to_excel(writer, 'Last Day Data')
    historical_df.to_excel(writer, 'Historical Data')
    writer.save()


portfolio_last_price_dict = get_last_prices_from_instruments_in_csv_file(PORTFOLIO_CSV_FILENAME)
portfolio_last_price_df = pd.DataFrame.from_dict([portfolio_last_price_dict])

portfolio_historical_price_df = get_historical_equity_prices_from_csv_file(PORTFOLIO_CSV_FILENAME,
                                                                             START_DATE,
                                                                             END_DATE)

#portfolio_monthly_prices_dict = get_historical_equity_prices_from_csv_file(PORTFOLIO_CSV_FILENAME)

write_excel_file(portfolio_last_price_df, portfolio_historical_price_df)
