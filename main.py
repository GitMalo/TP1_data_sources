from flask import Flask, request, render_template, jsonify
import logging
import requests
import os
from google.analytics.data_v1beta import BetaAnalyticsDataClient
from google.analytics.data_v1beta.types import RunReportRequest
from pytrends.request import TrendReq

app = Flask(__name__)

logging.basicConfig(level=logging.DEBUG)

prefix_google = """
 <!-- Google tag (gtag.js) -->
<script async
src="https://www.googletagmanager.com/gtag/js?id=G-GV4KJPM75M"></script>
<script>
 window.dataLayer = window.dataLayer || [];
 function gtag(){dataLayer.push(arguments);}
 gtag('js', new Date());
 gtag('config', 'G-GV4KJPM75M');
</script>
 """

@app.route("/")
def hello_world():
 return prefix_google + "Hello World"

@app.route("/logger", methods=["GET", "POST"])
def logger():
    # print a message in Python
    app.logger.info("Connexion à la page Logger")

    if request.method == 'POST':
        # take the text in the text box
        text_from_textbox = request.form['textbox']

        # print a message in the browser console with the text from the text box
        browser_log = f"""
        <script>
            console.log('Connexion à la page Logger');
            console.log('Texte de la boîte de texte : {text_from_textbox}');
        </script>
        """

    else:
    # print a message in the browser console
        browser_log = """
        <script>
            console.log('Connexion à la page Logger');
        </script>
        """
    
    return "logger page" + browser_log + render_template('template_logger.html')

@app.route("/perform_google_request", methods=["GET", "POST"])
def perform_google_request():
    # obtient la réponse de Google
    response = requests.get("https://www.google.com")
    # si la réponse est 200, on obtient les cookies
    if response.status_code == 200:
        response_message = response.cookies.get_dict()
    else:
        response_message = "Request to Google failed."

    return str(response_message)

@app.route("/perform_google_analytics_request", methods=["GET", "POST"])
def perform_google_analytics_request():
    # obtient la réponse de Google Analytics
    response = requests.get("https://analytics.google.com/analytics/web/#/p407503730/reports/intelligenthome")
    # si la réponse est 200, on obtient les cookies
    if response.status_code == 200:
        response_message = response.cookies.get_dict()
    else:
        response_message = "Request to Google analytics failed."

    return str(response_message)

@app.route('/fetch-google-analytics-data', methods=['GET'])
def fetch_google_analytics_data():

    os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'serious-form-402014-78076268a00b.json'
    PROPERTY_GA4_ID = '407503730'
    starting_date = "28daysAgo"
    ending_date = "yesterday"

    client = BetaAnalyticsDataClient()

    # function qui retourne la requête de l'API Google Analytics
    def get_visitor_count(client, property_id):
        request = RunReportRequest(
            property=f"properties/{property_id}",
            date_ranges=[{"start_date": starting_date, "end_date": ending_date}],
            metrics=[{"name": "activeUsers"}]
        )
        response = client.run_report(request)
        return response

    # récupère le nombre de visiteurs actifs
    response = get_visitor_count(client, PROPERTY_GA4_ID)

    # affiche le nombre de visiteurs actifs
    if response and response.row_count > 0:
        metric_value = response.rows[0].metric_values[0].value
    else:
        metric_value = "N/A"

    return f'Number of active visitors : {metric_value}'

@app.route('/fetch-google-trend')
def chart_data():
    pytrends = TrendReq(hl='en-US', tz=360)
    keywords = ["football", "basketball"]
    pytrends.build_payload(keywords, timeframe='today 12-m', geo='US')
    interest_over_time_df = pytrends.interest_over_time()

    data = {
        'dates': interest_over_time_df.index.strftime('%Y-%m-%d').tolist(),
        'football': interest_over_time_df['football'].tolist(),
        'basketball': interest_over_time_df['basketball'].tolist()
    }

    return jsonify(data)

if __name__ == '_main_':
    app.run(debug=True)


