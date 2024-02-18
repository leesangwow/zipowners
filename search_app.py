from dash import Dash, dash_table, html, callback, Output, Input, no_update, State
from dash import dcc
from dash import html
import dash_bootstrap_components as dbc
#from dash_bootstrap_templates import ThemeChangerAIO, template_from_url
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd


#Step1. Data Import
def read_data():
    df_all_data = pd.read_csv('static/data/meme_tot_seoul.csv')
    df_summary = pd.read_csv('static/data/summary_test.csv', encoding='cp949')
    df_all_data = df_all_data.astype({'price':'int64'})

    return df_all_data,df_summary

#Step3. Dash Components

def get_header():
    header = html.H1("금액별 아파트 찾기", className='mt-4',style={'textAlign':'center'})
    return header

def create_search_contents(df):

    ## Dropdowns ##
    dropdown_si = dbc.Col(
        dcc.Dropdown(
            id="filter-city",
            options=[
                {"label": city, "value": city}
                for city in df.city.unique()
            ]
        )
    )

    dropdown_gu = dbc.Col(
        dcc.Dropdown(id="filter-gu")
    )

    dropdown_dong = dbc.Col(
        dcc.Dropdown(id="filter-dong")
    )

    check_option = dcc.Checklist(
        id = 'option-3month',
        options =[
            {'label':'3개월 이내 거래된 단지만','value':"checked"}
        ],
        value = []
    )

    ## Contents Wrappers ##
    search_contents = html.Div(
        [
            html.Div(
                html.I(
                    "지역 선택(도시/지역구/동)",
                ),className="card-header",style={"background":"#C4DFD7"}
            ),
            html.Div([
                dbc.Row([
                    dropdown_si,
                    dropdown_gu,
                    dropdown_dong,
                    check_option
                ])
            ],className="card-body",style={"background":'#F3F2DC'})
        ],className='card mb-4'
    )

    return search_contents

def create_graph():

    graph_contents = html.Div(
        [
            html.Div(
                html.I(
                    "트렌드 차트",
                ),className="card-header",style={"background":"#C4DFD7"}),

            html.Div(
                dcc.Graph(
                    id='graph-content',
                    className='card mb-4'
                ),className="card-body",style={"background":'#C4DFD7'}
            )
        ],className='card mb-4'
    )

    return graph_contents

def create_datatable():

    datatable_contents = html.Div(
        [
            dbc.Container(
                html.I(
                     "아파트 순위 차트", 
                ),className='card-header',style={"background":"#C4DFD7"}),

            html.Div(
                [
                    dash_table.DataTable(
                        id = 'datatable-top10',
                        page_size=15,
                        filter_action='native',
                        sort_action='native',
                        style_table={'overflowX': 'auto'}
                    )
                ],className="card-body",style={"background":'#F3F2DC'}
            ),
        ],className='card mb-4'
    )

    return datatable_contents
