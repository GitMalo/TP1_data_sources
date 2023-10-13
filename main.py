from flask import Flask, request
import logging
import requests

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

    # Formulaire HTML avec une boîte de texte
    textbox_form = """
    <form method="POST">
        <label for="textbox">Text Box :</label><br>
        <input type="text" id="textbox" name="textbox"><br><br>
        <input type="submit" value="Soumettre">
    </form>
    """
    # Bouton pour effectuer une requête Google
    google_button = """
    <form method="GET" action="/perform_google_request">
        <input type="submit" value="Effectuer la requête Google">
    </form>
    """
    # Bouton pour effectuer une requête Google Analytics
    google_analytics_button = """
    <form method="GET" action="/perform_google_analytics_request">
        <input type="submit" value="Effectuer la requête Google analytics">
    </form>
    """
    
    return "logger page" + browser_log + textbox_form + google_button + google_analytics_button

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


