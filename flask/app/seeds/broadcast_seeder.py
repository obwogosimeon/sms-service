from __future__ import absolute_import

import uuid

import lorem
from flask_seeder import generator

from app.database import db
from app.database.models import SMSBroadcast


def seed():
    # generate fake broadcast sms
    fake_broadcasts_number = 10

    print("seeding broadcast sms...")
    for i in range(fake_broadcasts_number):
        provider_id = str(uuid.uuid4())
        name = generator.Name().generate()
        description = lorem.paragraph()
        is_published = True

        broadcast_kwargs = {
            "provider_id": provider_id,
            "name": name,
            "description": description,
            "is_published": is_published
        }

        broadcast = SMSBroadcast(**broadcast_kwargs)
        db.session.add(broadcast)
        db.session.commit()
    print("done broadcast sms")
