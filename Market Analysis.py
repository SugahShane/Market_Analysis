import os
import glob
import pandas as pd
from datetime import datetime

def set_constants():
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
    OUTPUT_EXCEL_FILENAME = OUTPUT_DATA_DIRECTORY + "~priceData.xlsx"


def readAndCombineDataFiles():
    global concatDF
    concatDF = pd.DataFrame()
    global concatLastDF
    concatLastDF = pd.DataFrame()

    os.chdir(marketDataInputDirectory)
    fileList = glob.glob("*.csv")

    for filename in fileList:
        print(filename)
        df = pd.read_csv(filename)
        dfLastDay = df.tail(1)

        if concatDF.empty:
            df.sort_values(by='Date', ascending=False)
            concatDF = df.copy()
            concatLastDF = dfLastDay.copy()
        else:
            concatDF = pd.merge(concatDF, df, on='Date', how='outer')
            concatLastDF = pd.merge(concatLastDF, dfLastDay, on='Date', how='left')

def getInflationData():
    global inflationDF
    inflationDF = concatDF[['Date', 'DBC_Close', 'XLB_Close', 'XAU_Close', 'XLF_Close']]
    #print(inflationDF)


def writeExcelFile():
    writer = pd.ExcelWriter(outputExcelFile)
    concatDF.to_excel(writer, 'All Data')
    concatLastDF.to_excel(writer, 'Last Day')
    inflationDF.to_excel(writer, 'Inflation')
    writer.save()


set_constants()
#readAndCombineDataFiles()
#getInflationData()
#writeExcelFile()
