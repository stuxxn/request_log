from flask import Blueprint, render_template
from flask_admin import Admin
from flask_admin.contrib.mongoengine import ModelView, EmbeddedForm
from . import model

ui = Blueprint("UI", __name__)


class HTTPView(ModelView):
    can_create = False
    can_edit = False
    can_delete = False
    can_view_details = True

    column_exclude_list = ["_cls"]

    column_filters = ['url']

    form_subdocuments = {
        "query": {
            "form_subdocuments": {
                None: EmbeddedForm()
            }
        }
    }


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