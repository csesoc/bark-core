__all__ = [
    "bp_swipes",
]

from flask import Blueprint

from .views import SwipeView

bp_swipes = Blueprint("bp_swipes", __name__)

bp_swipes.add_url_rule(
    "",
    view_func=SwipeView.as_view("swipe"),
    methods=["POST"])
