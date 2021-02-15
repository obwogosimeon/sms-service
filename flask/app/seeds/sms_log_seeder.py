from __future__ import absolute_import

from app.database import db
from app.database.models import SMSMessage
from app.database.models import SMSLog


def seed():
    print("seeding sms log. please wait...")
    sms_messages = SMSMessage.query.all()

    for sms in sms_messages:
        sms_log_kwargs = {
            'sms_id': sms.id,
            'status': 'Success',
            'network_code': '63902'
        }

        sms_log = SMSLog(**sms_log_kwargs)
        db.session.add(sms_log)
        db.session.commit()
    print("done seeding sms log.")
