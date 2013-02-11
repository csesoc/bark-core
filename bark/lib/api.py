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

        self.verify_json(request.json, self.required_fields_[method])

        try:
            response = getattr(self, method)(request.json)
        except:
            logger_.exception("Uncaught exception in API handler %r" % method)

            response = {
                "status": "BACKEND_ERROR",
                "error_detail": "Uncaught exception",
            }

        return jsonify(response)

    def verify_json(self, json, spec):
        """
        Verify JSON against the spec provided.

        Spec format is a list of tuples:
            (field_name, field_type)
        Each tuple must match the fields in JSON to be conforming to the spec.
        Extra fields in JSON are left unmodified.

        Calls out to self.bad_request() if JSON is non-conforming.
        """

        for field, field_type in spec:
            if field not in json:
                self.bad_request("Missing field %r" % field)

            if type(json[field]) != field_type:
                self.bad_request("Non-conformant field %r" % field)
