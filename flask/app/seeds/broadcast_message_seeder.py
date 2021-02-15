from __future__ import absolute_import

from app.database import db
from app.database.models import SMSBroadcast
from app.database.models import SMSBroadcastMessage

from random import randrange

import lorem
import datetime


def seed():
    print("seeding broadcast sms messages. please wait...")
    broadcasts = SMSBroadcast.query.all()

    for broadcast in broadcasts:
        broadcast_message_kwargs = {
            'broadcast_id': broadcast.id,
            'subject': lorem.sentence(),
            'message': lorem.paragraph(),
            'send_on_day_relative': randrange(1, 30),
            'send_on_day_absolute': datetime.datetime.now()
        }

        broadcast_message = SMSBroadcastMessage(**broadcast_message_kwargs)
        db.session.add(broadcast_message)
        db.session.commit()
    print("done seeding broadcast sms messages.")