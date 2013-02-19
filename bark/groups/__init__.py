from flask import Blueprint

from .views import CreateGroupView, GroupView

bp_groups = Blueprint("bp_groups", __name__)

bp_groups.add_url_rule(
    "/groups",
    view_func=CreateGroupView.as_view("groups"),
    methods=["POST"])

bp_groups.add_url_rule(
    "/groups/<int: group_id>",
    view_func=GroupView.as_view("groups"),
    methods=["GET, DELETE"])
