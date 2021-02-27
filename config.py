class config(object):
    PORT = 5000

class development(config):
    ENV = 'development'
    DEBUG = True
    TESTING = True
    WEEKLY_GOAL = 'Take Trades In the Direction of Larger Term Price Structure'
    BUSINESS_PLAN = {'Trader I am Working to become':['Sized up Swing Trader','I catch big moves with size'],
		'Definition of Success':['Having a Neutral to Small Green Week'],
		'Definition of Failure':['Not taking a small action'],
		'Max Trades Per Week':['10'],
		'Trade Managment':['One Shot Entries','Minimum Profit to lock in 4 points','I never widen my stop only tighten it'],
		'Setups I Trade':['Trend Continuation','S/R holding','S/R breaking'],
		'Symbols I trade and Watch':['ES']}
    CHART_TEMPLATE = """var chart = new CanvasJS.Chart("CHARTCONTAINER", {
	toolTip:{enabled: false},
	animationEnabled: false,zoomEnabled: true,exportEnabled: true,exportFileName: "Verigin_Industries",	title:{
	text: "TITLE"},axisX: {interval:1,intervalType: "hour",labelFontColor: "transparent",
	valueFormatString: "hh mm",crosshair: {enabled: true,snapToDataPoint: false}},
	axisY: {includeZero:false,crosshair: {enabled: true,snapToDataPoint: false}},
	data: [{type: "ohlc",yValueFormatString: "", 
	xValueFormatString: "hh mm",dataPoints: [
	PRICEDATA
	]}]});
    chart.render();
    """
    DAILY_CHART_TEMPLATE = """var chart = new CanvasJS.Chart("CHARTCONTAINER", {
	toolTip:{enabled: false},
	animationEnabled: false,zoomEnabled: true,exportEnabled: true,exportFileName: "Verigin_Industries",	title:{
	text: "TITLE"},axisX: {interval:1,intervalType: "day",labelFontColor: "transparent",
	valueFormatString: "",crosshair: {enabled: true,snapToDataPoint: false}},
	axisY: {includeZero:false,crosshair: {enabled: true,snapToDataPoint: false}},
	data: [{type: "ohlc",yValueFormatString: "", 
	xValueFormatString: "",dataPoints: [
	PRICEDATA
	]}]});
    chart.render();
    """
    CHART_DIV = """
    <div id="CHARTCONTAINER" style="width: 80%; height: 500px;display: inline-block;"></div>
        """