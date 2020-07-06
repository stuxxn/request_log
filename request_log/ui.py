from flask import Blueprint, render_template
from flask_admin import Admin
from flask_admin.contrib.mongoengine import ModelView, EmbeddedForm
from . import model
from mongoengine import EmbeddedDocument
from markupsafe import Markup
from flask_admin.model import typefmt
import html

ui = Blueprint("UI", __name__)


def list_format(view, values):

    v = [ x if not isinstance(x, model.KeyValue) else kv_format(view, x) for x in values]
    return Markup( "".join( [str(x) for x in v]))


def kv_format(view, value):
    return Markup(f"<div><span class='key'>{html.escape(value.key)}:</span> "
                  f"<span class='value'>{html.escape(value.value)}</span></div>")

view_formatter = dict(typefmt.BASE_FORMATTERS)
view_formatter.update({
    list: list_format,
    model.KeyValue: kv_format
})

class HTTPView(ModelView):
    can_create = False
    can_edit = False
    can_delete = False
    can_view_details = True



    column_filters = ['url']
    column_list = ("datetime", "method", "url",
                   "query_string", "query", "headers", "data")

    column_type_formatters = view_formatter



admin = Admin( name = "Request Log UI")
admin.add_view( HTTPView(model.HTTP))


@ui.route("/overview/<int:cnt>")
@ui.route("/overview", defaults = {"cnt": 25})
def overview(cnt):

    entries = model.HTTP.objects.order_by("datetime")[:cnt]
    return render_template("overview.html", entries = entries)


@ui.route("/details/<string:uid>")
def details(uid):

    entry = model.HTTP.objects.get_or_404(id = uid)
    return render_template("details.html", entry = entry)