import sys, traceback

from flask import abort, jsonify, request
from flask.views import View

class BarkApiEndpoint(View):
    def bad_request(self, error):
        # Ignoring the error for now.
        abort(400)
        raise Exception("wtf")  # Never reached.

    def dispatch_request(self):
        # Flask guarantees parsed JSON data in here.
        if request.json is None:
            self.bad_request("Request is not a JSON request")

        method = request.method.lower()

        # Verify that correct fields are present.
        for field in self.required_fields_.get(method, []):
            if field not in request.json:
                self.bad_request("Missing required field '%s'" % field)

        try:
            response = getattr(self, method)(request.json)
        except:
            traceback.print_exc(file=sys.stdout)
            response = {
                "status": "BACKEND_ERROR",
                "error_detail": "Uncaught exception",
            }

        return jsonify(response)
