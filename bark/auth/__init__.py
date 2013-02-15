from flask import Blueprint

from .views import *

bp_auth = Blueprint("bp_auth", __name__)

bp_auth.add_url_rule(
    "/login",
    view_func=LoginView.as_view("login"),
    methods=["POST"])

bp_auth.add_url_rule(
    "/logout",
    view_func=LogoutView.as_view("logout"),
    methods=["POST"])
