from flask import Flask, request
from .ui import ui
from .model import db
from . import model

UI_PREFIX = "/ui"
STATIC_PREFIX = "/static"

app = Flask(__name__)
app.config.from_pyfile("config.cfg")

db.init_app(app)
app.register_blueprint(ui, url_prefix = UI_PREFIX)


@app.after_request
def set_cors_headers(response):
    response.headers["Access-Control-Allow-Origin"] = request.headers.get("Origin", "*")
    response.headers["Access-Control-Allow-Credentials"] = "true"

    if request.method == "OPTIONS":
        # Both of these headers are only used for the "preflight request"
        # http://www.w3.org/TR/cors/#access-control-allow-methods-response-header
        response.headers[
            "Access-Control-Allow-Methods"
        ] = "GET, POST, PUT, DELETE, PATCH, OPTIONS"
        response.headers["Access-Control-Max-Age"] = "3600"  # 1 hour cache
        if request.headers.get("Access-Control-Request-Headers") is not None:
            response.headers["Access-Control-Allow-Headers"] = request.headers[
                "Access-Control-Request-Headers"
            ]
    return response

@app.after_request
def log_request(response):

    if request.path.startswith(UI_PREFIX) or request.path.startswith(STATIC_PREFIX):
        return response
    entry = model.HTTP()

    entry.ip = request.remote_addr

    entry.method = request.method
    entry.url = request.base_url
    entry.query_string = request.query_string.decode()
    entry.query = [ model.KeyValue(key = k, value = v) for k,v in request.args.items() ]
    entry.headers = [model.KeyValue(key=k, value=v) for k, v in request.headers.items()]
    entry.data = request.get_data()

    entry.save()

    return response

@app.route("/")
def index():
    return "Request logger"

@app.route("/post", methods = ["GET", "POST"])
def post_data():
    return "Request logger"
