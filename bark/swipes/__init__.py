__all__ = [
    "bp_swipe",
]

from flask import Blueprint

from .views import SwipeView

bp_swipe = Blueprint("bp_swipe", __name__)

bp_swipe.add_url_rule(
    "/",
    view_func=SwipeView.as_view("swipe"),
    methods=["POST"])
