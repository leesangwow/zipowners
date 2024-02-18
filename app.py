# 1. 모듈가져오기
from flask import Flask, render_template, request, redirect, send_file, session,url_for
from calculation import cal_result, calculate_loan, calculate_monthpay
import dash
import dash_html_components as html
import flask

from dash import Dash, dash_table, html, callback, Output, Input, no_update, State
from dash import dcc
from dash import html
import dash_bootstrap_components as dbc
import search_app
import pandas as pd


# CSS Files
dbc_css = "https://cdn.jsdelivr.net/gh/AnnMarieW/dash-bootstrap-templates/dbc.min.css"


# 2. 앱생성(플라스크 객체 생성)
server = Flask(__name__)
server.secret_key = 'whataglorylife'
app_dash = dash.Dash(__name__, server=server, routes_pathname_prefix='/search_apt/',external_stylesheets=[dbc_css])
#url_base_pathname
df,df_summary = search_app.read_data()
year_aixs = [y for y in range(2006,2024)]
header = search_app.get_header()
search_contents = search_app.create_search_contents(df_summary)
graph_contents = search_app.create_graph()
datatable_contents = search_app.create_datatable()

app_dash.layout = dbc.Container(
    [
        header,
        html.Hr(),
        dbc.Container(
            [
                search_contents,
                datatable_contents,
            ],className="container-fluid px-4"
            ),
    ],
)

# 3. 라우팅(사용자가 요청한 페이지의 주소:url을 누가 처리할것인가 연결)
# URL : http://127.0.0.1:5000/
@server.route("/") #요청
def index():     #응답
    #응답 처리가 결론
    #return -> 요청에 대한 응답을 한다.
    return render_template('index.html')

@server.route("/cal_salary",methods=["POST","GET"])
def cal_salary():
    if request.method == 'GET':
        return render_template('cal_salary.html')

    if request.method == 'POST':
        income_type = request.form.get('income_type')
        salary = int(request.form.get('salary'))
        interests = request.form.get('interests')
        loan_period = request.form.get('loan_period')
        dsr_ratio = request.form.get('dsr_ratio')
        saving_money = request.form.get('saving_money')

        if income_type == 'month_salary':
            salary = salary*12

        montly_payments = int(salary * float(dsr_ratio) / 100 / 12)

        wonli_50, wonli_70, wonli_80, wonkum_50,wonkum_70, wonkum_80,now_price_50,now_price_70,now_price_80 = calculate_loan(salary,interests,loan_period,dsr_ratio,saving_money)
    
        return render_template('cal_salary_result.html', 
                            salary = salary, interests= interests, dsr_ratio=dsr_ratio,
                            loan_period=loan_period,saving_money=saving_money,montly_payments=montly_payments,
                            wonli_50=wonli_50,wonli_70=wonli_70, wonli_80=wonli_80, 
                            wonkum_50=wonkum_50,wonkum_70=wonkum_70, wonkum_80=wonkum_80,
                            now_price_50=now_price_50,now_price_70=now_price_70, now_price_80=now_price_80)
            

@server.route("/cal_monthpay",methods=["POST","GET"])
def cal_monthpay():
    if request.method == 'GET':
        return render_template('cal_monthpay.html')

    if request.method == 'POST':
        monthpay = int(request.form.get('monthpay'))
        interests = request.form.get('interests')
        loan_period = request.form.get('loan_period')
        saving_money = request.form.get('saving_money')

        wonli_50, wonli_70, wonli_80, wonkum_50,wonkum_70, wonkum_80,now_price_50,now_price_70,now_price_80 = calculate_monthpay(monthpay,interests,loan_period,saving_money)

        return render_template('cal_monthpay_result.html', 
                            monthpay = monthpay, interests= interests,
                            loan_period=loan_period,saving_money=saving_money,
                            wonli_50=wonli_50,wonli_70=wonli_70, wonli_80=wonli_80, 
                            #wonkum_50=wonkum_50,wonkum_70=wonkum_70, wonkum_80=wonkum_80,
                            now_price_50=now_price_50,now_price_70=now_price_70, now_price_80=now_price_80)
    
@server.route("/searh_apt")
def render_searchapt():
    return redirect('/search_apt/')

@server.route('/login',methods=["POST","GET"])
def login():
    if request.method =='GET':
        return render_template('login.html')
    else:
        id_ = request.form['id_']
        pw_ = request.form['pw_']
        if id_ == 'munto' and pw_ == 'munto':
            session['id']= id_
            return redirect(url_for('index'))
        else:
            return render_template('login.html')

@server.route('/login_confirm', methods=['GET'])
def login_confirm():
    if "id" in session:
        return redirect('/search_apt/')
    else:
        return redirect(url_for('login'))

@server.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

@server.route('/testpage')
def test():
        
        df_smaple = df_summary.head(10)
        
        #data_json = df_summary.to_json(orient = 'split', indent = 4, force_ascii=False)
        data_column = df_summary.columns.tolist()
        data_sum = df_summary.head(20).values.tolist()

        return render_template('test copy.html', enumerate=enumerate, data_column = data_column, data_sum=data_sum)

################################################
@callback(
    Output("filter-gu",'options'),
    [Input("filter-city",'value')],
)
def update_gu(city):
    if "id" in session:
        return [{"label": gu, "value": gu} for gu in df_summary[df_summary['city']==city].gu.unique()]
    else:
        return {'label':"Need Login","value":'Need Login'}

@callback(
    Output("filter-dong",'options'),
    Input("filter-gu",'value')
)
def update_dong(gu):
    return [{"label": dong, "value": dong} for dong in df_summary[df_summary['gu']==gu].dong.unique()]


@callback(
    [Output('datatable-top10', 'columns'), 
     Output('datatable-top10', 'data'),
     ],
    [Input('filter-dong', 'value'),
     Input('filter-gu', 'value'),
     Input('option-3month','value')
    ],
    [State('filter-city', 'value'),]
)
def update_datatable(dong,gu,option_3month,city):
    
    print(option_3month)
    if 'checked' in option_3month:
        month_option = (df_summary['3mon_avg_price'] > 0)
        print('적용')
    else:
        month_option = (df_summary['3mon_avg_price'] >= 0)
        print('미적용')

    if dong is None:
        mask = ((df_summary.city == city) & (df_summary.gu == gu) & month_option)
    else:
        mask = ((df_summary.city == city) & (df_summary.gu == gu) & (df_summary.dong == dong) & month_option)

    filtered_df = df_summary.loc[mask, :]

    columns_select = ['dong','apt','size',
                      'latest_price','latest_date','3mon_avg_price','3mon_deals',
                      'latest_price_j','latest_date_j','3mon_avg_price_j','3mon_deals_j','jeon_ratio','jeon_diff',
                      'max_price','max_date','min_price','min_date','1year_deals','최고가대비','최저가대비']
    
    columns_kor = ['동','단지명','크기',
                   '최근 매매 실거래','최근 거래 날짜','3개월 평균가','3개월 거래량',
                   '최근 전세 실거래','최근 전세 거래 날짜','전세 3개월 평균가','전세 3개월 거래량','전세가율','매전차이(갭)',
                   '최고가','최고가날짜','최저가','최저가날짜','1년거래량','최고점대비','최저점대비']

    result_df = filtered_df[columns_select]
    result_df.columns = columns_kor

    cols = [
        {"name": i, "id": i} for i in result_df.columns
    ]

    data = result_df.to_dict('records')

    return cols, data


server.run(host='0.0.0.0',port=7000)
