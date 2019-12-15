from flask import Blueprint, render_template
from . import model



ui = Blueprint("UI", __name__)

@ui.route("/overview/<int:cnt>")
@ui.route("/overview", defaults = {"cnt": 25})
def overview(cnt):

    entries = model.HTTP.objects.order_by("datetime")[:cnt]
    return render_template("overview.html", entries = entries)

@ui.route("/details/<string:uid>")
def details(uid):

    entry = model.HTTP.objects.get_or_404(id = uid)
    return render_template("details.html", entry = entry)