from bark import create_app, db

from bark.users.models import User
from bark.groups.models import Group
from bark.persons.models import Person
from bark.events.models import Event
from bark.swipe.models import Swipe
from bark.devices.models import Device

create_app().test_request_context().push()
