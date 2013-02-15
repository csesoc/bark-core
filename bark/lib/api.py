import sys, traceback

from flask import abort, jsonify, request
from flask.views import View

import bark.lib.logs as logging

logger_ = logging.GetLogger(__name__)

class BarkApiException(Exception):
    """
    Abstract exception class for Bark-related errors.

    Override status() in concrete subclasses.
    """

    def status(self):
        raise NotImplemented()

    def error_detail(self):
        return self.args[0] if self.args else ""

    def describe(self):
        return {
            "status": self.status(),
            "error_detail": self.error_detail(),
        }

class VerificationException(BarkApiException):
    def status(self): return "BAD_REQUEST"

class BarkApiEndpoint(View):
    def bad_request(self, error):
        # Ignoring the error for now.
        logger_.warning("Bad request: %s", error)

        abort(400)
        raise Exception("wtf")  # Never reached.

    def dispatch_request(self):
        """
        Dispatches incoming request.
        This method is called by Flask itself.
        """

        try:
            self.method = request.method.lower()
            self.verify_request(request)

            response = getattr(self, self.method)(request.json)

        except BarkApiException, e:
            response = e.describe()

        except:
            logger_.exception("Uncaught exception in API handler %r" % self.method)

            response = {
                "status": "BACKEND_ERROR",
                "error_detail": "Uncaught exception",
            }

        return jsonify(response)

    def verify_request(self, request):
        """
        Verifies request to be similar to what we would expect it to be.
        Raises VerificationException in case of a verification error.

        May modify self.*, e.g. unpacking request data.
        """

        if request.json is None:
            raise VerificationException("Request is not a JSON request")

        self.verify_json(request.json, self.required_fields_[self.method])

    def verify_json(self, json, spec):
        """
        Verify JSON against the spec provided.

        Spec format is a list of tuples:
            (field_name, field_type)
        Each tuple must match the fields in JSON to be conforming to the spec.
        Extra fields in JSON are left unmodified.
        """

        for field, field_type in spec:
            if field not in json:
                raise VerificationException("Missing field %r" % field)

            if type(json[field]) != field_type:
                raise VerificationException("Non-conformant field %r" % field)
