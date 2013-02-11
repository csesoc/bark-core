import sys, traceback

from flask import abort, jsonify, request
from flask.views import View

import bark.lib.logs as logging

logger_ = logging.GetLogger(__name__)

class BarkApiEndpoint(View):
    def bad_request(self, error):
        # Ignoring the error for now.
        logger_.warning("Bad request: %s", error)

        abort(400)
        raise Exception("wtf")  # Never reached.

    def dispatch_request(self):
        # Flask guarantees parsed JSON data in here.
        if request.json is None:
            self.bad_request("Request is not a JSON request")

        method = request.method.lower()

        # Verify that correct fields are present, and of the correct type
        data_types = self.required_fields_.get(method, {})
        parsed_json = self.parse_fields(request.json, data_types)

        try:
            response = getattr(self, method)(parsed_json)
        except:
            logger_.exception("Uncaught exception in API handler %r" % method)

            response = {
                "status": "BACKEND_ERROR",
                "error_detail": "Uncaught exception",
            }

        return jsonify(response)

    def parse_fields(self, json, field_types):
        parsed_json={}

        for data_type in field_types:
            for field in field_types[data_type]:
                if field not in json:
                    self.bad_request("Missing required field '%s'" % field)
                try:
                    parsed_json[field] = data_type(request.json[field])
                except ValueError:
                    self.bad_request("Invalid field '%s'" % field)

        return parsed_json
