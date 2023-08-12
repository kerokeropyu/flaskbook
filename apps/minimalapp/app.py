from flask import Flask

app = Flask(__name__)

@app.route("/", endpoint="endpoint-name")
def index():
    return "Hello, Flaskbook!"

# @app.get("/hello")
# @app.post("/hello")
@app.route("/hello/<name>",
           methods=["GET", "POST"],
           endpoint="hello-endpoint")
def hello(name):
    return f"Hello, {name}!"