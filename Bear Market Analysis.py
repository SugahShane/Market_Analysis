import pandas as pd
import plotly
import plotly.plotly as py
import plotly.graph_objs as go
import matplotlib
import matplotlib.pyplot as plt
from matplotlib import style
import openpyxl
from openpyxl import Workbook
from openpyxl.utils.dataframe import dataframe_to_rows
import datetime
import math

# Constant Definitions
plotly.tools.set_credentials_file(username='shane.brewer', api_key='Utd2w2H5xUb4MfnMmlNZ')
plotly.tools.set_config_file(world_readable=True, sharing='public')
# baseDirectory = "C:\\Users\\brewshan\\Dropbox\\PycharmProjects\\Bear Market Research\\data\\"
BASE_DIRECTORY = "C:\\Users\\Shane\\Dropbox\\PyCharm Projects\\Market Analysis\\"
DATA_DIRECTORY = BASE_DIRECTORY + "data\\"
INPUT_DATA_FILENAME = "SP500.csv"
OUTPUT_DIRECTORY = BASE_DIRECTORY + "output\\"
OUTPUT_EXCEL_FILENAME = "Bear Market Analysis.xlsx"


def read_data_from_csv():
    print("Reading data file: " + DATA_DIRECTORY + INPUT_DATA_FILENAME)
    df = pd.read_csv(DATA_DIRECTORY + INPUT_DATA_FILENAME, parse_dates=True)
    return df


def plotly_publish_price_table(price_data):
    price_table = go.Table(
        header=dict(values=list(price_data.columns),
                    fill=dict(color='C2D4FF'),
                    align=['left'] * 5),
        cells=dict(values=[price_data.Date,
                           price_data.SP500_Open,
                           price_data.SP500_High,
                           price_data.SP500_Low,
                           price_data.SP500_Close,
                           price_data.SP500_Volume,
                           price_data.SP500_ATRPercentOfClose20,
                           price_data.SP500_SQN25,
                           price_data.SP500_SQN50,
                           price_data.SP500_SQN100,
                           price_data.SP500_SQN200,
                           price_data.SP500_MACD,
                           price_data.SP500_MACD_Avg,
                           price_data.SP500_MACD_Diff,
                           price_data.SP500_LinReg10,
                           price_data.SP500_LinReg30,
                           price_data.SP500_LinReg90,
                           price_data.SP500_LinReg270],
                   fill=dict(color='#F5F8FF'),
                   align=['left'] * 5))

    table_data = [price_table]
    py.plot(table_data, filename='Bear_Market_Research_Table')


def matplotlib_graph_sp500_close_graph(close_data):
    style.use('fivethirtyeight')
    fig = plt.figure()
    fig.set_size_inches(18.5, 9.5)
    ax1 = plt.subplot2grid((1, 1), (0, 0))
    ax1.plot_date(close_data.index, close_data['SP500_Close'], '-', label='S&P 500')
    for label in ax1.xaxis.get_ticklabels():
        label.set_rotation(45)
    ax1.grid(True)

    plt.title('S&P 500 Price')
    plt.xlabel('Date')
    plt.ylabel('Price')
    plt.legend()
    plt.subplots_adjust(left=0.09, bottom=0.20, right=0.94, top=0.90, wspace=0.2, hspace=0)
    plt.savefig(OUTPUT_DIRECTORY + 'SP500_Closes_Chart.png', dpi=100)
    plt.show()


def matplotlib_graph_peak_to_trough_drawdowns(close_data):
    style.use('fivethirtyeight')
    fig = plt.figure()
    fig.set_size_inches(18.5, 9.5)
    ax1 = plt.subplot2grid((1, 1), (0, 0))
    ax1.plot_date(close_data.index, close_data['Peak_To_Trough_Percentage'], '-', label='S&P 500')
    for label in ax1.xaxis.get_ticklabels():
        label.set_rotation(45)
    ax1.grid(True)

    plt.title('S&P 500 Price Peak to Trough Drawdown')
    plt.xlabel('Date')
    plt.ylabel('Percentage Drawdown')
    plt.legend()
    plt.subplots_adjust(left=0.09, bottom=0.20, right=0.94, top=0.90, wspace=0.2, hspace=0)
    plt.savefig(OUTPUT_DIRECTORY + 'SP500_Peak_To_Trough_Drawdown.png', dpi=100)
    plt.show()


def drawdown_analysis(closing_prices, wb):
    print("Analyzing Drawdowns")
    #closing_price_diff = closing_prices['SP500_Close'] - closing_prices['SP500_Close'].shift(1)
    closing_prices = closing_prices.assign(Close_Price_Diff=closing_prices['SP500_Close'] -
                                                              closing_prices['SP500_Close'].shift(1))
    closing_prices = closing_prices.assign(Close_Price_Diff_Percentage=closing_prices['SP500_Close'].pct_change() * 100)
    #closing_prices['Close_Price_Diff_Percentage'] = closing_prices['SP500_Close'].pct_change() * 100

    closing_prices = closing_prices.assign(Cumulative_Price_Diff=closing_prices['Close_Price_Diff'].cumsum())
    #closing_prices['Cumulative_Price_Diff'] = closing_prices['Close_Price_Diff'].cumsum()

    closing_prices = closing_prices.assign(Max_Gain=closing_prices['Cumulative_Price_Diff'].expanding(2).max())
    #closing_prices['Max_Gain'] = closing_prices['Cumulative_Price_Diff'].expanding(2).max()

    closing_prices = closing_prices.assign(Peak_To_Trough=closing_prices['Cumulative_Price_Diff'] - \
                                                          closing_prices['Max_Gain'])
    #closing_prices['Peak_To_Trough'] = closing_prices['Cumulative_Price_Diff'] - \
    #                                   closing_prices['Max_Gain']

    closing_prices = closing_prices.assign(Peak_To_Trough_Percentage=closing_prices['Peak_To_Trough'] / \
                                                                     (closing_prices['SP500_Close'] -
                                                                     closing_prices['Peak_To_Trough']) * 100)
    #closing_prices['Peak_To_Trough_Percentage'] = closing_prices['Peak_To_Trough'] / \
    #                                              (closing_prices['SP500_Close'] -
    #                                              closing_prices['Peak_To_Trough']) * 100
    drawdown_periods = find_drawdowns(closing_prices, 20)
    output_drawdowns_to_workbook(drawdown_periods, wb)
    #matplotlib_chart_drawdowns(closing_prices[['Date', 'Peak_To_Trough_Percentage']])
    #plotly_chart_drawdowns(closing_prices[['Date', 'Peak_To_Trough_Percentage']])


def find_drawdowns(data, drawdown_percentage_threshold):
    drawdown_data = pd.DataFrame()
    max_drawdown_percentage = 0
    for row in data.itertuples():
        if math.isnan(getattr(row, 'Peak_To_Trough')):
            continue
        if math.isclose(getattr(row, 'Peak_To_Trough'), 0, rel_tol=1e-5) and \
                max_drawdown_percentage < (drawdown_percentage_threshold * -1):
            # Now making new highs, and the last drawdown reached the minimum threshold
            start_date = data.at[last_peak_index, 'Date']
            end_date = data.at[max_drawdown_index, 'Date']
            num_days = (datetime.datetime.strptime(data.at[max_drawdown_index, 'Date'], "%m/%d/%Y") -
                        datetime.datetime.strptime(data.at[last_peak_index, 'Date'], "%m/%d/%Y")).days

            df = pd.DataFrame({'Start_Date': start_date,
                               'End_Date': end_date,
                               'Total_Drawdown_Percentage': max_drawdown_percentage,
                               'Num_Days': num_days}, index=[0])
            #df['Start_Date'] = data.at[last_peak_index, 'Date']
            #df['End_Date'] = data.at[max_drawdown_index, 'Date']
            #df['Total_Drawdown_Percentage'] = max_drawdown_percentage
            #df['Num_Days'] = (datetime.datetime.strptime(data.at[last_peak_index, 'Date'], "%m/%d/%Y") -
            #                  datetime.datetime.strptime(data.at[max_drawdown_index, 'Date'], "%m/%d/%Y")).days
            #df['Num_Days'] = (data.at[last_peak_index, 'Date'] - data.at[max_drawdown_index, 'Date']).days

            drawdown_data = drawdown_data.append(df, ignore_index=True)
            last_peak_index = row.Index
            max_drawdown_percentage = 0
            max_drawdown_index = 0
        elif math.isclose(getattr(row, 'Peak_To_Trough'), 0, rel_tol=1e-5):
            # Now making new highs but didn't reach minimum drawdown percentage threshold. Reset variables.
            last_peak_index = row.Index
            max_drawdown_percentage = 0
            max_drawdown_index = 0
        elif max_drawdown_percentage > getattr(row, 'Peak_To_Trough_Percentage'):
            max_drawdown_percentage = getattr(row, 'Peak_To_Trough_Percentage')
            max_drawdown_index = row.Index
    return drawdown_data


def output_drawdowns_to_workbook(df, wb):
    print("Writing Drawdown Worksheet")
    ws = wb.create_sheet("Drawdowns")
    ws.title = "Drawdowns"
    for row in dataframe_to_rows(df, index=True, header=True):
        ws.append(row)

    start_date_col = ws.column_dimensions['D']
    start_date_col.number_format = '0.00%'


def matplotlib_chart_drawdowns(closing_prices):
    print("Generating Matplotlib Drawdown Chart")
    #plt.ion()
    style.use('fivethirtyeight')
    #fig = plt.figure()
    #fig.set_size_inches(18.5, 9.5)
    ax1 = plt.subplot2grid((1, 1), (0, 0))
    ax1.plot_date(closing_prices['Date'].tolist(), closing_prices['Peak_To_Trough_Percentage'].tolist(),
                  linestyle='-', label='S&P 500')
    #for label in ax1.xaxis.get_ticklabels():
    #    label.set_rotation(45)
    ax1.grid(True)

    plt.title('S&P 500 Price Peak to Trough Drawdown')
    plt.xlabel('Date')
    plt.ylabel('Percentage Drawdown')
    plt.legend()
    plt.subplots_adjust(left=0.09, bottom=0.20, right=0.94, top=0.90, wspace=0.2, hspace=0)
    #plt.savefig(OUTPUT_DIRECTORY + 'SP500_Peak_To_Trough_Drawdown.png', dpi=100)
    plt.show()


def plotly_chart_drawdowns(closing_prices):
    print("Generating Plotly Drawdown Chart")
    drawdown_trace = go.Scatter(
        x=closing_prices['Date'].tolist(),
        y=closing_prices['Peak_To_Trough_Percentage'].tolist()
    )
    data = [drawdown_trace]
    py.plot(data, filename='Percentage_Drawdown_Graph')


def sqn_analysis(close_prices):
    print('Performing SQN Analysis')
    matplotlib_graph_sqn_data(close_prices)


def matplotlib_graph_sqn_data(sqn_dataframe):
    print('Generating Matplotlib SQN Chart')
    style.use('fivethirtyeight')
    fig = plt.figure()
    fig.set_size_inches(18.5, 9.5)
    ax1 = plt.subplot2grid((1, 1), (0, 0))
    ax1.plot_date(sqn_dataframe['Date'], sqn_dataframe['SP500_SQN25'], linestyle='-', label='SQN(25)')
    ax1.plot_date(sqn_dataframe['Date'], sqn_dataframe['SP500_SQN50'], linestyle='-', label='SQN(50)')
    ax1.plot_date(sqn_dataframe['Date'], sqn_dataframe['SP500_SQN100'], linestyle='-', label='SQN(100)')
    ax1.plot_date(sqn_dataframe['Date'], sqn_dataframe['SP500_SQN200'], linestyle='-', label='SQN(200)')
    for label in ax1.xaxis.get_ticklabels():
        label.set_rotation(45)
    ax1.grid(True)

    plt.title('S&P 500 SQN Values')
    plt.xlabel('Date')
    plt.ylabel('SQN')
    plt.legend()
    plt.subplots_adjust(left=0.09, bottom=0.20, right=0.94, top=0.90, wspace=0.2, hspace=0)
    plt.savefig(OUTPUT_DIRECTORY + 'SP500_SQN.png', dpi=100)
    plt.show()


price_data = read_data_from_csv()
wb = Workbook()
drawdown_analysis(price_data[['Date', 'SP500_Close']], wb)
sqn_analysis(price_data)
wb.save(OUTPUT_DIRECTORY + OUTPUT_EXCEL_FILENAME)