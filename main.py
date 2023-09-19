from flask import Flask

app = Flask(__name__)

@app.route("/")
def hello_world():
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
 return prefix_google + "Hello World"
