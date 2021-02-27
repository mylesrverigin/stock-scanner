from ui import app
from flask import render_template,request,url_for,redirect
import pandas as pd
from modules.mongo import DataManager
from modules.time_handling import TimeManagement
from ui.lib.create_datatable import CreateDatatable
from ui.lib.call_price import CallPrice
from ui.lib.playbook import PlayBooks
from ui.lib.tradeplans import TradePlans
from ui.lib.journals import Journals
from ui.lib.format_views import FormatWeeklyReview
from ui.lib.report_card import ReportCard
from ui.lib.charts import Charts
from ui.lib.inplay import Inplay
from ui.lib.goal import Goals

@app.route('/')
def home():
    goals = Goals()
    dates = TimeManagement().weekly_review_times()
    trades = Journals('1993/12/20').weekly_trades(dates)
    tickers = Inplay().run() 
    weekly_goal = goals.return_weekly_goal()
    business_plan = goals.return_business_plan()
    return render_template('home.html',goal=weekly_goal,plan=business_plan,trades=trades,inplay=tickers)

@app.route('/createplaybook/',methods=['GET','POST'])
def create_playbook():
    if request.method == 'GET':
        return render_template('create_playbook.html')
    if request.method == 'POST':
        dict_ = request.form
        if dict_['ticker'] != '':
            #add in a check for ticker and for date and defaults 
            date = TimeManagement().date_now()
            playbook = PlayBooks(date,dict_['ticker'])
            playbook.log_playbook(playbook_dict=dict_)
            return render_template('success.html')
        else:
            return redirect(url_for('create_playbook'))

@app.route('/viewplaybook/')
def view_playbook():
    date = TimeManagement().date_now()
    playbooks = PlayBooks(date,'playbook')
    plays= playbooks.return_views()
    return render_template('view_playbook.html',plays=plays)

@app.route('/createjournal/',methods=['GET','POST'])
def create_journal():
    if request.method == 'GET':
        goals = Goals()
        weekly_goal = goals.return_weekly_goal()
        return render_template('create_journal.html',goal=weekly_goal)
    if request.method == 'POST':
        dict_ = request.form
        date = TimeManagement().date_now()
        journal = Journals(date)
        journal.log_journal(dict_)
        return render_template('success.html')

@app.route('/viewjournal/')
def view_journal():
    date = TimeManagement().date_now()
    journals = Journals(date)
    journal = journals.return_views() 
    return render_template('view_journal.html',journal=journal)

@app.route('/createtradeplan/',methods=['GET','POST'])
def create_tradeplan():
    if request.method == 'GET':
        return render_template('create_tradeplan.html')
    if request.method == 'POST':
        dict_ = request.form
        if dict_['ticker'] != '':
            #add in a check for ticker and for date and defaults 
            date = TimeManagement().date_now()
            ##
            tradeplan = TradePlans(date,dict_['ticker'])
            tradeplan.log_tradeplan(tradeplan_dict=dict_)
            ##
            return render_template('success.html')
        else:
            return redirect(url_for('create_tradeplan'))

@app.route('/viewtradeplan/')
def view_tradeplan():
    date = TimeManagement().date_now()
    yesterday = TimeManagement().date_days_ago(1)
    date_list = [date,yesterday]
    tradeplan = TradePlans(date,'tradeplan')
    plans = tradeplan.weekly_view(date_list)
    return render_template('view_tradeplan.html',plans=plans)

@app.route('/reportcard/',methods=['GET','POST'])
def create_report_card():
    if request.method == 'GET':
        goals = Goals()
        weekly_goal = goals.return_weekly_goal()
        return render_template('create_report_card.html',goal=weekly_goal)
    if request.method == 'POST':
        dict_ = request.form
        date = TimeManagement().date_now()
        reportcard = ReportCard(date)
        reportcard.log_report_card(dict_)
        return render_template('success.html')

@app.route('/viewreportcard/')
def view_report_card():
    date = TimeManagement().date_now()
    reportcard = ReportCard(date)
    cards = reportcard.return_views()
    return render_template('view_reportcard.html',cards=cards)

@app.route('/weekreview/')
def weekly_review():
    # this is really innefficent and uses multiple loops
    dates = TimeManagement().weekly_review_times()
    journals = Journals('1993/12/20').weekly_view(dates)
    playbooks = PlayBooks('1993/12/20','playbooks').weekly_view(dates)
    tradeplans = TradePlans('1993/12/20','tradeplans').weekly_view(dates)
    reportcards = ReportCard('1993/12/20').weekly_view(dates)
    final_result = FormatWeeklyReview(dates,tradeplans,journals,playbooks,reportcards).format_review()
    return render_template('weekly_review.html',result=final_result)

@app.route('/charts/')
def view_charts():
    date = TimeManagement().date_now()
    # date = TimeManagement().date_days_ago(2)
    charts = Charts(date)
    charts,divs = charts.run()
    #return render_template('test.html')
    return render_template('charts.html',charts=charts,divs=divs)