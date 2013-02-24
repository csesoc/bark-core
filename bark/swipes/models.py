from datetime import datetime

from bark import db
from bark.devices.models import Device

class Swipe(db.Model):
    __tablename__ = 'swipes'

    id = db.Column(db.Integer, primary_key=True)

    device_id = db.Column(db.ForeignKey("devices.id"))
    device = db.relationship("Device")

    card_id = db.Column(db.ForeignKey("cards.card_uid"))
    card = db.relationship("Card")

    timestamp = db.Column(db.DateTime)

    def __init__(self, device, card, timestamp=datetime.now()):
        self.device_id = device.id
        self.card_id = card.card_uid
        self.timestamp = timestamp
