from flask import jsonify
from bark import db
from bark.auth.shared import BarkAuthenticatedApiEndpoint
from bark.devices.models import Device

class DeviceView(BarkAuthenticatedApiEndpoint):

    def post(self, json):
        return 'should add a new one'