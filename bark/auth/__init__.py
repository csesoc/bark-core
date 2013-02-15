# This module exports its blueprint and the means to verify an incoming Bark
# API request as having been authenticated.

__all__ = [
    "bp_auth",
    "BarkAuthenticatedApiEndpoint",
]

from flask import Blueprint

from .views import LoginView, LogoutView
from .shared import BarkAuthenticatedApiEndpoint

bp_auth = Blueprint("bp_auth", __name__)

bp_auth.add_url_rule(
    "/login",
    view_func=LoginView.as_view("login"),
    methods=["POST"])

bp_auth.add_url_rule(
    "/logout",
    view_func=LogoutView.as_view("logout"),
    methods=["POST"])
