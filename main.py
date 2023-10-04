from flask import Flask

app = Flask(__name__)

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

@app.route("/logger")
def logger():
    # print a message in Python
    app.logger.info("Connexion à la page Logger")

    # print a message in the browser console
    browser_log = """
    <script>
        console.log('Connexion à la page Logger');
    </script>
    """

    return prefix_google + "Logger Page" + browser_log

