import plotly.graph_objs as go
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
from Trading_Functions.SQN import *
from Trading_Functions.NDX import *
from Trading_Functions.ATR_Percent_Of_Close import *
from Data_Import.IEX_Data_Download import *


START_DATE = datetime(2018, 1, 1)
END_DATE = datetime.now()
BASE_DIRECTORY = "D:\\Users\\Shane\\OneDrive\\Programming Projects\\Investing\\Market_Analysis\\"
DATA_DIRECTORY = BASE_DIRECTORY + "data\\"
#INPUT_DATA_FILENAME = "DataInstruments.csv"
INPUT_DATA_FILENAME = "TestData.csv"
OUTPUT_DIRECTORY = BASE_DIRECTORY + "output\\"
OUTPUT_EXCEL_FILENAME = "Market Data.xlsx"
US_INDEX_INSTRUMENTS_FILENAME = DATA_DIRECTORY + "US_Market_Instruments.csv"
US_SECTOR_INSTRUMENTS_FILENAME = DATA_DIRECTORY + "US_Sector_Instruments.csv"

app = dash.Dash(__name__)

app.layout = html.Div(children=[
    html.H1(children='Market Analysis Dashboard'),
    dcc.Tabs(id="tabs", value='overview', children=[
        dcc.Tab(label='Overview', value='overview'),
        dcc.Tab(label='SQN Dashboard', value='sqn_dashboard'),
        dcc.Tab(label='Market Breadth', value='market_breadth'),
        dcc.Tab(label='Harmonic Rotations', value='harmonic_rotations'),
        dcc.Tab(label='Inflation', value='inflation'),
        dcc.Tab(label='Volume Profile', value='volume_profile'),
    ]),
    html.Div(id='tabs-content')
])


def make_dash_table(df):
    # Return a dash definition of an HTML table for a Pandas dataframe
    table = []
    html_row = []

    for i in range(len(df.columns.values)):
        html_row.append(html.Th([df.columns.values[i]]))
    table.append(html.Tr(html_row))

    for index, row in df.iterrows():
        html_row = []
        for i in range(len(row)):
            html_row.append(html.Td([row[i]]))
        table.append(html.Tr(html_row))
    return table


def generate_market_type_table_cell(sqn_value):
    print(sqn_value)
    if isinstance(sqn_value, float):
        if sqn_value > STRONG_BULL_SQN:
            return html.Td(sqn_value, id='strongbull')
        if sqn_value > BULL_SQN:
            return html.Td(sqn_value, id='bull')
        if sqn_value > NEUTRAL_SQN:
            return html.Td(sqn_value, id='neutral')
        if sqn_value > BEAR_SQN:
            return html.Td(sqn_value, id='bear')
        return html.Td(sqn_value)
    return html.Td(sqn_value)


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


def generate_sqn_market_type_data(df):
    df['SQN_200'] = sqn(df.close, 200)
    df['SQN_100'] = sqn(df.close, 100)
    df['SQN_50'] = sqn(df.close, 50)
    df['SQN_25'] = sqn(df.close, 25)
    df['ATR_Percent_Of_Close_20'] = ATR_percent_of_close(df, 20)
    df['SQN_100_Market_Type'] = market_classification(df)
    df['NDX_10'] = ndx(df, 10)
    df['NDX_200'] = ndx(df, 200)
    return df


def generate_sqn_table(spy_df, qqq_df, dia_df):
    spy_df = spy_df.sort_index(ascending=False)
    qqq_df = qqq_df.sort_index(ascending=False)
    dia_df = dia_df.sort_index(ascending=False)

    sqn_df = spy_df[['Instrument', 'SQN_200', 'SQN_100', 'SQN_50', 'SQN_25',
                     'ATR_Percent_Of_Close_20', 'SQN_100_Market_Type']].head(1)
    sqn_df = sqn_df.append(qqq_df[['Instrument', 'SQN_200', 'SQN_100', 'SQN_50', 'SQN_25',
                                   'ATR_Percent_Of_Close_20', 'SQN_100_Market_Type']].head(1),
                           ignore_index=True)
    sqn_df = sqn_df.append(dia_df[['Instrument', 'SQN_200', 'SQN_100', 'SQN_50', 'SQN_25',
                                   'ATR_Percent_Of_Close_20', 'SQN_100_Market_Type']].head(1),
                           ignore_index=True)
    return sqn_df


def generate_ndx_table(spy_df, qqq_df, dia_df):
    spy_df = spy_df.sort_index(ascending=False)
    qqq_df = qqq_df.sort_index(ascending=False)
    dia_df = dia_df.sort_index(ascending=False)

    ndx_df = spy_df[['Instrument', 'NDX_10', 'NDX_200']].head(1)
    ndx_df = ndx_df.append(qqq_df[['Instrument', 'NDX_10', 'NDX_200']].head(1), ignore_index=True)
    ndx_df = ndx_df.append(dia_df[['Instrument', 'NDX_10', 'NDX_200']].head(1), ignore_index=True)

    # TODO: Add Overbought/Oversold/Neutral classifications
    return ndx_df


def generate_price_table(spy_df):
    return 0


def generate_long_term_overview_df():
    df = pd.DataFrame()
    return df


def render_overview_content():
    return html.Div(children=[
        html.H3('S&P 500 Chart'),
        dcc.Graph(
            figure=go.Figure(
                data=[candlestick_trace(spy_df)]),
            id='sp500_graph'),
        html.H3('SQN Market Type'),
        html.Table(make_dash_table(sqn_df)),
        html.H3('NDX Overview'),
        html.Table(make_dash_table(ndx_df)),
        html.H3('Long-term Trend'),
        html.H5('Price')
    ])


def render_sqn_dashboard():
    return html.Div(children=[
        html.H3('S&P 500 SQN Charts'),
        html.H5('S&P 500 SQN(200) Chart'),
        dcc.Graph(
            id='SP500_SQN200_chart',
            figure={
                'data': [
                    go.Scatter(
                        x=spy_df.index.tolist(),
                        y=spy_df['SQN_200'].dropna().values.tolist()
                    )
                ]
            }
        ),
        html.H5('S&P 500 SQN(100) Chart'),
        dcc.Graph(
            id='SP500_SQN100_chart',
            figure={
                'data': [
                    go.Scatter(
                        x=spy_df.index.tolist(),
                        y=spy_df['SQN_100'].dropna().values.tolist()
                    )
                ]
            }
        ),
        html.H5('S&P 500 SQN(50) Chart'),
        dcc.Graph(
            id='SP500_SQN50_chart',
            figure={
                'data': [
                    go.Scatter(
                        x=spy_df.index.tolist(),
                        y=spy_df['SQN_50'].dropna().values.tolist()
                    )
                ]
            }
        ),
        html.H5('S&P 500 SQN(25) Chart'),
        dcc.Graph(
            id='SP500_SQN25_chart',
            figure={
                'data': [
                    go.Scatter(
                        x=spy_df.index.tolist(),
                        y=spy_df['SQN_25'].dropna().values.tolist()
                    )
                ]
            }
        ),
        html.H3('Sector SQN Table'),
        html.H5('US Sectors'),

    ])


@app.callback(Output('tabs-content', 'children'),
              [Input('tabs', 'value')])
def render_content(tab):
    if tab == 'overview':
        return render_overview_content()
    elif tab == 'sqn_dashboard':
        return render_sqn_dashboard()
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


def load_instrument_data(instrument_list_csv_file):
    sector_instruments_df = pd.read_csv(instrument_list_csv_file)

    instruments_price_data_dictionary = {}
    for row in sector_instruments_df.itertuples():
        instrument_price_data_df = get_historical_price_data_from_iex(getattr(row, 'Instrument'))
        instruments_price_data_dictionary[getattr(row, 'Instrument')] = instrument_price_data_df

    return instruments_price_data_dictionary


#qqq_df = get_historical_price_data_from_iex('QQQ')
#dia_df = get_historical_price_data_from_iex('DIA')
#spy_df = get_historical_price_data_from_iex('SPY')
#qqq_df = get_historical_price_data_from_iex('QQQ')
#dia_df = get_historical_price_data_from_iex('DIA')

us_market_price_data_dictionary = load_instrument_data(US_INDEX_INSTRUMENTS_FILENAME)
#us_sector_price_data_dictionary = load_instrument_data(US_SECTOR_INSTRUMENTS_FILENAME)

spy_df = generate_sqn_market_type_data(us_market_price_data_dictionary['SPY'])
qqq_df = generate_sqn_market_type_data(us_market_price_data_dictionary['QQQ'])
dia_df = generate_sqn_market_type_data(us_market_price_data_dictionary['DIA'])

sqn_df = generate_sqn_table(spy_df, qqq_df, dia_df)
ndx_df = generate_ndx_table(spy_df, qqq_df, dia_df)

price_df = generate_price_table(spy_df)

# TODO: Long-Term Trend
# TODO: Prices: Price to SMA(200), SMA(50) to SMA(200), NDX, SMA Slope
# TODO: Momentum: ADX, RSI(20)
# TODO: Volatility: VIX, ATR
# TODO: Market Breadth: Cumulative Tick
# TODO: Interest Rates Chart
# TODO: SQN Charts
# TODO: ETF Money Flow table


if __name__ == '__main__':
    app.run_server(debug=True)
