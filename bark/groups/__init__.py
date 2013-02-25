from flask import Blueprint

from .views import GroupView, SingleGroupView

bp_groups = Blueprint("bp_groups", __name__)

bp_groups.add_url_rule(
    "",
    view_func=GroupView.as_view("groups"),
    methods=["POST", "GET"])

bp_groups.add_url_rule(
    "/<int: group_id>",
    view_func=SingleGroupView.as_view("groups"),
    methods=["GET"])
