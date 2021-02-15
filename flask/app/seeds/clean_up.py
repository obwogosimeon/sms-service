from __future__ import absolute_import

from app.database import db

from app.database.models import SMSBroadcastMessage
from app.database.models import SMSLog
from app.database.models import SMSMessage
from app.database.models import SMSBroadcast
from app.database.models import SMSBroadcastSubscription


def clean():
    print("truncating data. please wait...")

    broadcast_messages = SMSBroadcastMessage.query.all()
    for message in broadcast_messages:
        db.session.delete(message)
        db.session.commit()

    broadcast_subscriptions = SMSBroadcastSubscription.query.all()
    for broadcast_subscription in broadcast_subscriptions:
        db.session.delete(broadcast_subscription)
        db.session.commit()

    sms_logs = SMSLog.query.all()
    for log in sms_logs:
        db.session.delete(log)
        db.session.commit()

    sms_messages = SMSMessage.query.all()
    for sms in sms_messages:
        db.session.delete(sms)
        db.session.commit()

    sms_broadcasts = SMSBroadcast.query.all()
    for broadcast in sms_broadcasts:
        db.session.delete(broadcast)
        db.session.commit()

    print("done truncating data.")