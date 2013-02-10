from flask import Blueprint

from .events import *

bp_events = Blueprint("bp_events", __name__)

bp_events.add_url_rule(
    "/events",
    view_func=EventCreateView.as_view("events"),
    methods=["POST"])

bp_events.add_url_rule(
    "/events/<int: event_id>",
    view_func=EventView.as_view("events"),
    methods=["GET", "DELETE"])
