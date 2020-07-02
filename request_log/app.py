from flask import Flask, request
from .ui import ui, admin
from .model import db
from . import model

UI_PREFIX = "/ui"
STATIC_PREFIX = "/static"

exclude_prefixes = [
    UI_PREFIX, STATIC_PREFIX, "/admin"
]

app = Flask(__name__)
app.config.from_pyfile("config.cfg")

db.init_app(app)
app.register_blueprint(ui, url_prefix = UI_PREFIX)
admin.init_app(app)


@app.after_request
def log_request(response):

    if any( [request.path.startswith(x) for x in exclude_prefixes]):
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