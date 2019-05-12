import plotly.graph_objs as go
import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_table as dt
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
COMMODITY_INSTRUMENTS_FILENAME = DATA_DIRECTORY + "Commodity_Instruments.csv"
INTEREST_RATE_INSTRUMENTS_FILENAME = DATA_DIRECTORY + "Interest_Rate_Instruments.csv"
REAL_ESTATE_INSTRUMENTS_FILENAME = DATA_DIRECTORY + "Real_Estate_Instruments.csv"


app = dash.Dash(__name__)

app.layout = html.Div(children=[
    html.H1(children='Market Analysis Dashboard'),
    dcc.Tabs(id="tabs", value='overview', children=[
        dcc.Tab(label='Overview', value='overview'),
        dcc.Tab(label='SQN Dashboard', value='sqn_dashboard'),
        dcc.Tab(label='Market Breadth', value='market_breadth'),
        dcc.Tab(label='Harmonic Rotations', value='harmonic_rotations'),
        dcc.Tab(label='Inflation', value='inflation'),
    ]),
    html.Div(id='tabs-content')
])


def make_dash_table(df, table_id):
    return dt.DataTable(
        id=table_id,
        columns=[{"name": i, "id": i} for i in df.columns],
        data=df.to_dict('records'),
        style_header={
            'backgroundColor': 'grey',
            'fontWeight': 'bold',
            'font-family': 'Helvetica'
        },
        style_cell={
            'font-family': 'Helvetica'
        }
    )


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
    try:
        df['SQN_200'] = sqn(df.close, 200)
        df['SQN_100'] = sqn(df.close, 100)
        df['SQN_50'] = sqn(df.close, 50)
        df['SQN_25'] = sqn(df.close, 25)
        df['ATR_Percent_Of_Close_20'] = ATR_percent_of_close(df, 20)
        df['SQN_100_Market_Type'] = market_classification(df)
        df['NDX_10'] = ndx(df, 10)
        df['NDX_200'] = ndx(df, 200)
    except Exception:
        print("Failed to generate SQN values for " + df['Instrument'])
    return df


def generate_sqn_market_type_from_df_dict(df_dict):
    for key, value in df_dict.items():
        value = generate_sqn_market_type_data(value)
    return df_dict


def generate_sqn_table(df_dict):
    df = pd.DataFrame(columns=['Instrument', 'Name', 'SQN_200', 'SQN_100', 'SQN_50', 'SQN_25',
                     'ATR_Percent_Of_Close_20', 'SQN_100_Market_Type'])
    for key, value in df_dict.items():
        value = value.sort_index(ascending=False)
        df = df.append(value[['Instrument', 'Name', 'SQN_200', 'SQN_100', 'SQN_50', 'SQN_25',
                     'ATR_Percent_Of_Close_20', 'SQN_100_Market_Type']].head(1),
                     ignore_index=True)
    return df


def generate_ndx_table(df_dict):
    df = pd.DataFrame(columns=['Instrument', 'NDX_10', 'NDX_200'])
    for key, value in df_dict.items():
        value = value.sort_index(ascending=False)
        df = df.append(value[['Instrument', 'NDX_10', 'NDX_200']].head(1), ignore_index=True)
    return df


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
        make_dash_table(us_market_sqn_df, 'sqn_market_table'),
        html.H3('NDX Overview'),
        make_dash_table(us_market_ndx_df, 'ndx_market_table'),
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
        make_dash_table(us_sector_sqn_df, 'us_sector_sqn_table'),
        html.H5('Interest Rate Products'),
        make_dash_table(interest_rate_sqn_df, 'interest_rate_sqn_table'),
        html.H5('Commodities'),
        make_dash_table(commodity_sqn_df, "commodity_sqn_table"),
        html.H5('Real Estate'),
        make_dash_table(real_estate_sqn_df, 'real_estate_sqn_table')
    ])


def load_instrument_price_data(instrument_list_csv_file):
    instruments_df = pd.read_csv(instrument_list_csv_file)

    instruments_price_data_dictionary = {}
    for row in instruments_df.itertuples():
        instrument_price_data_df = get_historical_price_data_from_iex(getattr(row, 'Instrument'))
        instrument_company_info_df = get_company_info_from_iex(getattr(row, 'Instrument'))
        instrument_price_data_df['Name'] = instrument_company_info_df['companyName']
        instruments_price_data_dictionary[getattr(row, 'Instrument')] = instrument_price_data_df
    return instruments_price_data_dictionary


def load_instrument_company_data(instrument_list_csv_file):
    instruments_df = pd.read_csv(instrument_list_csv_file)

    instruments_company_data_dictionary = {}
    for row in instruments_df.itertuples():
        instrument_company_data_df = get_company_info_from_iex(getattr(row, 'Instrument'))
        instruments_company_data_dictionary[getattr(row, 'Instrument')] = instrument_company_data_df
    return instruments_company_data_dictionary


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


us_market_price_data_dictionary = load_instrument_price_data(US_INDEX_INSTRUMENTS_FILENAME)
us_sector_price_data_dictionary = load_instrument_price_data(US_SECTOR_INSTRUMENTS_FILENAME)
commoditiy_price_data_dictionary = load_instrument_price_data(COMMODITY_INSTRUMENTS_FILENAME)
interest_rate_price_data_dictionary = load_instrument_price_data(INTEREST_RATE_INSTRUMENTS_FILENAME)
real_estate_price_data_dictionary = load_instrument_price_data(REAL_ESTATE_INSTRUMENTS_FILENAME)

us_market_company_data_dictionary = load_instrument_company_data(US_INDEX_INSTRUMENTS_FILENAME)

us_market_price_sqn_data_dictionary = generate_sqn_market_type_from_df_dict(us_market_price_data_dictionary)
us_sector_price_sqn_data_dictionary = generate_sqn_market_type_from_df_dict(us_sector_price_data_dictionary)
commoditiy_price_sqn_data_dictionary = generate_sqn_market_type_from_df_dict(commoditiy_price_data_dictionary)
interest_rate_price_sqn_data_dictionary = generate_sqn_market_type_from_df_dict(interest_rate_price_data_dictionary)
real_estate_price_sqn_data_dictionary = generate_sqn_market_type_from_df_dict(real_estate_price_data_dictionary)

spy_df = generate_sqn_market_type_data(us_market_price_data_dictionary['SPY'])

us_market_sqn_df = generate_sqn_table(us_market_price_sqn_data_dictionary)
us_market_ndx_df = generate_ndx_table(us_market_price_sqn_data_dictionary)
us_sector_sqn_df = generate_sqn_table(us_sector_price_sqn_data_dictionary)
commodity_sqn_df = generate_sqn_table(commoditiy_price_sqn_data_dictionary)
interest_rate_sqn_df = generate_sqn_table(interest_rate_price_sqn_data_dictionary)
real_estate_sqn_df = generate_sqn_table(real_estate_price_sqn_data_dictionary)

price_df = generate_price_table(spy_df)

if __name__ == '__main__':
    app.run_server(debug=True)
