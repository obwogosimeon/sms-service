from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.dialects.postgresql import UUID

import datetime
import uuid

db = SQLAlchemy()


class BaseModel(db.Model):
    __abstract__ = True

    id = db.Column(UUID(as_uuid=True), default=uuid.uuid4, primary_key=True)
    date_created = db.Column(db.DateTime(timezone = True), default = datetime.datetime.now)
    last_modified = db.Column(db.DateTime(timezone = True), default = datetime.datetime.now, onupdate=datetime.datetime.now)