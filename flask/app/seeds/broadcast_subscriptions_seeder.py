from __future__ import absolute_import

from app.database import db
from app.database.models import SMSBroadcast
from app.database.models import SMSBroadcastSubscription

import uuid 

import datetime


def seed():
    print("seeding broadcast subscriptions. please wait...")
    broadcasts = SMSBroadcast.query.all()

    for broadcast in broadcasts:
        broadcast_subscription_kwargs = {
            'broadcast_id': broadcast.id,
            'farmer_id': str(uuid.uuid4()),
            'day_zero': datetime.datetime.now()
        }

        broadcast_subscription = SMSBroadcastSubscription(**broadcast_subscription_kwargs)
        db.session.add(broadcast_subscription)
        db.session.commit()
    print("done seeding subscriptions.")