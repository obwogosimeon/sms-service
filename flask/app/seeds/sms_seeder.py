from __future__ import absolute_import

import lorem
import datetime
from app.database import db
from app.database.models import SMSMessage
from flask_seeder import generator
import uuid


def seed():
    # generate fake sms
    fake_sms_number = 10

    print("seeding sms...")
    for i in range(fake_sms_number):
        africastalking_sms_id = generator.Integer(start=10000, end=99999).generate()
        phone_number = generator.Integer(start=10000000, end=99999999).generate()
        country_code = '+2547'
        message = lorem.paragraph()
        africastalking_sms_cost = generator.Integer(start=20, end=100).generate()

        sms_kwargs = {
            "africastalking_sms_id": africastalking_sms_id,
            "phone": f'{country_code}{phone_number}',
            "message": message,
            "africastalking_sms_cost": f'KES {africastalking_sms_cost}',
            "send_at": datetime.datetime.now(),
            "farmer_id": str(uuid.uuid4()),
            "provider_id": str(uuid.uuid4())
        }

        sms = SMSMessage(**sms_kwargs)
        db.session.add(sms)
        db.session.commit()
    print("done sms")
