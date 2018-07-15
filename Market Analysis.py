import os
import glob
import pandas as pd
from datetime import datetime

def read_and_combine_data_files(etf_df):
    etf_last_day_df = pd.DataFrame()

    os.chdir(INPUT_DATA_DIRECTORY)
    file_list = glob.glob("*.csv")

    for filename in file_list:
        print(filename)
        df = pd.read_csv(filename)
        last_day_df = df.tail(1)

        if etf_df.empty:
            df.sort_values(by='Date', ascending=False)
            etf_df = df.copy()
            etf_last_day_df = last_day_df.copy()
        else:
            etf_df = pd.merge(etf_df, df, on='Date', how='outer')
            etf_last_day_df = pd.merge(etf_last_day_df, last_day_df, on='Date', how='left')

def get_inflation_data():
    inflation_df = etf_df[['Date', 'DBC_Close', 'XLB_Close', 'XAU_Close', 'XLF_Close']]
    #print(inflation_df)


def write_excel_file():
    writer = pd.ExcelWriter(OUTPUT_EXCEL_FILENAME)
    etf_df.to_excel(writer, 'All Data')
    etf_df.head(1).to_excel(writer, 'Last Day')
    #inflation_df.to_excel(writer, 'Inflation')
    writer.save()


if os.environ['COMPUTERNAME'] == 'SEA-1800100736':
    DATE = '07-12-2018'
    BASE_DIRECTORY = "C:\\Users\\brewshan\\PycharmProjects\\Market_Analysis\\"
    INPUT_DATA_DIRECTORY = BASE_DIRECTORY + "data\\" + DATE + "\\"
    OUTPUT_DATA_DIRECTORY = BASE_DIRECTORY + "output\\"
elif os.environ['COMPUTERNAME'] == 'SHANETRADINGD':
    DATE = datetime.now().strftime('%m-%d-%Y')
    BASE_DIRECTORY = "D:\\Users\\Shane\\SkyDrive\\Documents\\Trading\\Research\\Data\\"
    INPUT_DATA_DIRECTORY = BASE_DIRECTORY + "Market Analysis Data\\" + DATE + "\\"
    OUTPUT_DIRECTORY = BASE_DIRECTORY + "Market Analysis Data\\"
else:
    DATE = datetime.now().strftime('%m-%d-%Y')
    BASE_DIRECTORY = "D:\\Users\\Shane\\SkyDrive\\Documents\\Trading\\Research\\Data\\"
    INPUT_DATA_DIRECTORY = BASE_DIRECTORY + "Market Analysis Data\\" + DATE + "\\"
    OUTPUT_DIRECTORY = BASE_DIRECTORY + "Market Analysis Data\\"
OUTPUT_EXCEL_FILENAME = OUTPUT_DATA_DIRECTORY + "~priceData.xlsx"

etf_df = pd.DataFrame()
read_and_combine_data_files(etf_df)
#get_inflation_data()
write_excel_file()
