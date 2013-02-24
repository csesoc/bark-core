from flask import Blueprint

from .views import *

bp_persons = Blueprint("bp_persons", __name__)

bp_persons.add_url_rule(
    "",
    view_func=PersonsView.as_view('persons'),
    methods=['POST']
)
