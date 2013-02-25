from flask import Blueprint

from .views import *

bp_events = Blueprint("bp_events", __name__)


bp_events.add_url_rule(
    "/<int:event_id>/swipes",
    view_func=EventInfoView.as_view("single_event_swipes"),
    methods=["GET"])

bp_events.add_url_rule(
    "/<int:event_id>",
    view_func=SingleEventView.as_view("single_events"),
    methods=["GET", "DELETE"])

bp_events.add_url_rule(
    "",
    view_func=EventView.as_view("events"),
    methods=["POST", "GET"])

