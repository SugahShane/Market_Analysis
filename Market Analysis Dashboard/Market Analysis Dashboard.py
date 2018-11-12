from iexfinance import get_historical_data
from datetime import datetime
import pandas as pd
import time
import math
import statistics
import plotly.plotly as py
import plotly.graph_objs as go
import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_table
from dash.dependencies import Input, Output


START_DATE = datetime(2018, 1, 1)
END_DATE = datetime.now()
BASE_DIRECTORY = "D:\\Users\\Shane\\Dropbox\\PyCharm Projects\\Market_Analysis\\"
DATA_DIRECTORY = BASE_DIRECTORY + "data\\"
#INPUT_DATA_FILENAME = "DataInstruments.csv"
INPUT_DATA_FILENAME = "TestData.csv"
OUTPUT_DIRECTORY = BASE_DIRECTORY + "output\\"
OUTPUT_EXCEL_FILENAME = "Market Data.xlsx"
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
colors = {
    'background': '#111111',
    'text': '#7FDBFF'
}


app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div(children=[
    html.H1(children='Market Analysis Dashboard',
            style={
                'textAlign': 'center',
                'color': colors['text']
            }
            ),
    dcc.Tabs(id="tabs", value='tab-1', children=[
        dcc.Tab(label='Overview', value='overview'),
        dcc.Tab(label='SQN Dashboard', value='sqn_dashboard'),
        dcc.Tab(label='Market Breadth', value='market_breadth'),
        dcc.Tab(label='Harmonic Rotations', value='harmonic_rotations'),
        dcc.Tab(label='Inflation', value='inflation'),
        dcc.Tab(label='Volume Profile', value='volume_profile'),
    ]),
    html.Div(id='tabs-content')
])


def read_equity_list_from_csv():
    print("Reading data file: " + DATA_DIRECTORY + INPUT_DATA_FILENAME)
    df = pd.read_csv(DATA_DIRECTORY + INPUT_DATA_FILENAME)
    return df


def get_list_of_equities_price_data_from_iex(instruments_df):
    instruments_price_data_df = pd.DataFrame()
    for row in instruments_df.itertuples():
        print("Processing: " + getattr(row, "Instrument"))
        try:
            instrument_df = get_historical_data(getattr(row, 'Instrument'),
                                                start=START_DATE,
                                                end=END_DATE,
                                                output_format='pandas')
            #instrument_df = instrument_df.assign(Instrument=getattr(row, 'Instrument'))
            instruments_price_data_df = instruments_price_data_df.append(instrument_df, ignore_index=True)
        except Exception:
            print("Could not process " + getattr(row, "Instrument"))
        time.sleep(.5)
    return instruments_price_data_df


def get_equity_price_data_from_iex(ticker):
    print("Fetching from IEX: " + ticker)
    try:
        instrument_df = get_historical_data(ticker,
                                            start=START_DATE,
                                            end=END_DATE,
                                            output_format='pandas')
    except Exception:
        print("Could not process " + ticker)
    return instrument_df


def candlestick_trace(df):
    return go.Candlestick(
        x=df.index,
        open=df.open,
        high=df.high,
        low=df.low,
        close=df.close,
        showlegend=False,
        name="candlestick",
    )


def ATR(df):
    atr_df = pd.DataFrame()
    atr_df['ATR1'] = abs(df['high'] - df['low'])
    atr_df['ATR2'] = abs(df['high'] - df['close'].shift())
    atr_df['ATR3'] = abs(df['low'] - df['close'].shift())
    atr_df['TrueRange'] = atr_df[['ATR1', 'ATR2', 'ATR3']].max(axis=1)
    return atr_df['TrueRange']


def ATR_percent_of_close(df, period):
    df['ATR'] = ATR(df)
    df['ATR_Percent_Of_Close'] = df['ATR'] / df['close']
    return df['ATR_Percent_Of_Close'].rolling(window=period).mean()


def SQN(df, period):
    if len(df.index) < period:
        raise Exception('Not enough data in data frame for period')

    percent_change_df = (df - df.shift()) / df.shift()
    avg_df = percent_change_df.rolling(window=period).mean()
    stdev_df = percent_change_df.rolling(window=period).std()

    multiplier = 0
    if period < 100:
        multiplier = math.sqrt(period)
    else:
        multiplier = 10

    sqn_df = avg_df / stdev_df * multiplier
    return sqn_df


def generate_sqn_market_type_data(df):
    df['SQN_200'] = SQN(df.close, 200)
    df['SQN_100'] = SQN(df.close, 100)
    df['SQN_50'] = SQN(df.close, 50)
    df['SQN_25'] = SQN(df.close, 25)
    df['ATR_Percent_Of_Close_20'] = ATR_percent_of_close(df, 20)
    return df

def generate_sqn_table(spy_df, qqq_df, dia_df):
    spy_df = spy_df.sort_index(ascending=False)
    spy_df['Ticker'] = 'SPY'
    qqq_df = qqq_df.sort_index(ascending=False)
    qqq_df['Ticker'] = 'QQQ'
    dia_df = dia_df.sort_index(ascending=False)
    dia_df['Ticker'] = 'DIA'

    sqn_df = spy_df[['Ticker', 'SQN_200', 'SQN_100', 'SQN_50', 'SQN_25', 'ATR_Percent_Of_Close_20']].head(1)
    sqn_df = sqn_df.append(qqq_df[['Ticker', 'SQN_200', 'SQN_100', 'SQN_50', 'SQN_25', 'ATR_Percent_Of_Close_20']].head(1),
                           ignore_index=True)
    sqn_df = sqn_df.append(dia_df[['Ticker', 'SQN_200', 'SQN_100', 'SQN_50', 'SQN_25', 'ATR_Percent_Of_Close_20']].head(1),
                           ignore_index=True)
    return sqn_df


def render_overview_content():
    return html.Div(children=[
        html.H3('S&P 500 Chart'),
        dcc.Graph(
            figure=go.Figure(
                data=[candlestick_trace(spy_df)]),
            id='sp500_graph'),
        html.H3('SQN Overview'),
        # dcc.Graph(
        #     figure=go.Table(
        #         header=dict(values=list(sqn_df.columns),
        #                     fill=dict(color='#C2D4FF'),
        #                     align=['left'] * 5,
        #                     font=dict(color='black', size=12)),
        #         cells=dict(values=[sqn_df.Ticker,
        #                            sqn_df.SQN_200,
        #                            sqn_df.SQN_100,
        #                            sqn_df.SQN_50,
        #                            sqn_df.SQN_25,
        #                            sqn_df.ATR_Percent_Of_Close_20],
        #                    fill=dict(color='#F5F8FF'),
        #                    align=['left'] * 5)))
        dash_table.DataTable(
            id='sqn_table',
            columns=[{"'name': i, 'id': i"} for i in sqn_df],
            style_cell_conditional=[
                {
                    'if': {'row_index': 'odd'},
                    'backgroundColor': '#eeeeee'
                }
            ],
            data=sqn_df
        )
    ])


@app.callback(Output('tabs-content', 'children'),
              [Input('tabs', 'value')])
def render_content(tab):
    if tab == 'overview':
        return render_overview_content()
    elif tab == 'sqn_dashboard':
        return html.Div([
            html.H3('SQN Dashboard')
        ])
    elif tab == 'market_breadth':
        return html.Div([
            html.H3('Market Breadth')
        ])
    elif tab == 'harmonic_rotations':
        return html.Div([
            html.H3('Harmonic Rotations')
        ])
    elif tab == 'inflation':
        return html.Div([
            html.H3('Inflation')
        ])
    elif tab == 'volume_profile':
        return html.Div([
            html.H3('Volume Profile')
        ])


spy_df = get_equity_price_data_from_iex('SPY')
qqq_df = get_equity_price_data_from_iex('QQQ')
dia_df = get_equity_price_data_from_iex('DIA')
#amzn_df = get_equity_price_data_from_iex('AMZN')

spy_df = generate_sqn_market_type_data(spy_df)
qqq_df = generate_sqn_market_type_data(qqq_df)
dia_df = generate_sqn_market_type_data(dia_df)

sqn_df = generate_sqn_table(spy_df, qqq_df, dia_df)

if __name__ == '__main__':
    app.run_server(debug=True)
