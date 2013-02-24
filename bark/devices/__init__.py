from flask import Blueprint

from .views import *

bp_devices = Blueprint("bp_devices", __name__)

bp_devices.add_url_rule(
    "",
    view_func=DeviceView.as_view("devices"),
    methods=["POST"])
