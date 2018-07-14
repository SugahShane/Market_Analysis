import os
import glob
import pandas as pd
from datetime import datetime

date = datetime.now().strftime('%m-%d-%Y')
baseDirectory = "D:\\Users\\Shane\\SkyDrive\\Documents\\Trading\\Research\\Data\\"
marketDataInputDirectory = baseDirectory + "Market Analysis Data\\" + date + "\\"
marketDataOutputDirectory = baseDirectory + "Market Analysis Data\\"
#outputCSVFile = outputDirectory + "~priceData.csv"
outputExcelFile = marketDataOutputDirectory + "~priceData.xlsx"

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


readAndCombineDataFiles()
getInflationData()
writeExcelFile()
