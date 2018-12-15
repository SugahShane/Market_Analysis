import os
from Data_Import.IEX_Data_Download import *


START_DATE = datetime.now()
END_DATE = datetime.now()
BASE_DIRECTORY = "D:\\Users\\Shane\\Dropbox\\PyCharm Projects\\Market_Analysis\\"
DATA_DIRECTORY = BASE_DIRECTORY + "data\\"
PORTFOLIO_CSV_FILENAME = DATA_DIRECTORY + "PortfolioInstruments.csv"
TODAY_DATE = datetime.now().strftime('%m-%d-%Y')
OUTPUT_DIRECTORY = "D:\\Users\\Shane\\SkyDrive\\Documents\\Trading\\Research\\Data\\Portfolio Data\\"
OUTPUT_EXCEL_FILENAME = OUTPUT_DIRECTORY + "Portfolio Data.xlsx"


def write_excel_file(df):
    print("Writing Excel File: " + OUTPUT_EXCEL_FILENAME)
    writer = pd.ExcelWriter(OUTPUT_EXCEL_FILENAME)
    df.to_excel(writer, 'Last Day Data')
    writer.save()


portfolio_last_price_dict = get_last_prices_from_instruments_in_csv_file(PORTFOLIO_CSV_FILENAME)
portfolio_last_price_df = pd.DataFrame.from_dict([portfolio_last_price_dict])
write_excel_file(portfolio_last_price_df)
