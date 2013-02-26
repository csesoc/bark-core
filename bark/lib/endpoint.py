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

    def status(self):  # pragma: no cover
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
    def dispatch_request(self, **kwargs):
        """
        Dispatches incoming request.
        This method is called by Flask itself.
        """

        try:
            self.method = request.method.lower()
            self.verify_request(request)

            if self.method == 'post' or self.method == 'put':
                response = getattr(self, self.method)(request.json, **kwargs)
            else:
                response = getattr(self, self.method)(**kwargs)

        except BarkApiException, e:
            response = e.describe()

        except:
            logger_.exception("Uncaught exception in API handler %r" % self.method)

            response = {
                "status": "BACKEND_ERROR",
                "error_detail": "Uncaught exception",
            }

        response = jsonify(response)

        # Check if we need JSONP.
        try:
            callback = request.args.get('callback', None)
            if callback is not None:
                response = '%s(%s)' % (unicode(callback), response.data)
        except:
            # Something has gone wrong. Probably request.json is None.
            # Ignore it, return response, which should remain unmodified.
            pass

        return response

    def verify_request(self, request):
        """
        Verifies request to be similar to what we would expect it to be.
        Raises VerificationException in case of a verification error.

        May modify self.*, e.g. unpacking request data.
        """

        if (request.method == 'POST' or request.method == 'PUT'):
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
