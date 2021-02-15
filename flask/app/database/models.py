import datetime
import json
import os

from app.database import db
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.ext.hybrid import hybrid_method
from sqlalchemy.orm import relationship

from . import BaseModel

schema_name = os.getenv('SCHEMA_NAME')


class SMSLog(BaseModel):
    __tablename__ = 'sms_log'
    __table_args__ = {"schema": schema_name}

    sms_id = db.Column(UUID(as_uuid=True), db.ForeignKey(f'{schema_name}.sms_message.id', ondelete='CASCADE'), nullable=False, index=True)
    timestamp = db.Column(db.DateTime, default=datetime.datetime.now)
    at_status_code = db.Column(db.String(), nullable=False)
    at_failure_reason = db.Column(db.String(), nullable=True)

    def __repr__(self):
        return f'<SMSLog {self.id}>'


class SMSMessage(BaseModel):
    __tablename__ = 'sms_message'
    __table_args__ = {"schema": schema_name}

    provider_id = db.Column(UUID(as_uuid=True), nullable=True)
    broadcast_message_id = db.Column(UUID(as_uuid=True), db.ForeignKey(f'{schema_name}.sms_broadcast_message.id', ondelete='CASCADE'), nullable=True, index=True)
    phone = db.Column(db.String(), nullable=False)
    send_at = db.Column(db.DateTime, nullable=True)
    sent = db.Column(db.Boolean, nullable=False, default=False)
    message = db.Column(db.String(), nullable=False)
    at_sms_id = db.Column(db.String(), nullable=True, unique=True, index=True)
    at_sms_cost = db.Column(db.String(), nullable=True)

    logs = relationship("SMSLog", backref='sms', lazy='dynamic')

    def __repr__(self):
        return f'<SMS {self.id}>'

    @hybrid_method
    def contains_status(self, status):
        return self.last_status == status

    @hybrid_property
    def status(self):
        statuses = []

        for log in self.logs:
            statuses.append({
                'at_status_code': log.at_status_code,
                'timestamp': log.timestamp.strftime('%Y-%m-%d %H:%M:%S')
            })

        return statuses

    @hybrid_property
    def last_status(self):
        last_status = SMSLog.query.filter(SMSLog.sms_id == self.id).order_by(SMSLog.date_created.desc()).first()
        return last_status.at_status_code if last_status is not None else "NA"

    @hybrid_property
    def status_date(self):
        if self.logs.count() > 0:
            last_status = self.logs.order_by(SMSLog.date_created.desc()).first()
            return last_status.timestamp.strftime('%Y-%m-%d %H:%M:%S')
        return "NA"


class SMSBroadcast(BaseModel):
    __tablename__ = "sms_broadcast"
    __table_args__ = {"schema": schema_name}

    provider_id = db.Column(UUID(as_uuid=True), nullable=False)
    name = db.Column(db.String(), nullable=False)
    description = db.Column(db.String(), nullable=True)
    is_published = db.Column(db.Boolean, nullable=False, default=False)
    relative_send_dates = db.Column(db.Boolean, nullable=True, default=False)


class SMSBroadcastMessage(BaseModel):
    __tablename__ = "sms_broadcast_message"
    __table_args__ = {"schema": schema_name}

    broadcast_id = db.Column(UUID(as_uuid=True), db.ForeignKey(f'{schema_name}.sms_broadcast.id', ondelete='CASCADE'),
                             nullable=False, index=True)
    subject = db.Column(db.String(), nullable=False)
    message = db.Column(db.String(), nullable=False)
    send_on_day_relative = db.Column(db.Integer, nullable=True)
    send_on_day_absolute = db.Column(db.DateTime, nullable=True)


class SMSBroadcastSubscription(BaseModel):
    __tablename__ = "sms_broadcast_subscription"
    __table_args__ = {"schema": schema_name}

    broadcast_id = db.Column(UUID(as_uuid=True), db.ForeignKey(f'{schema_name}.sms_broadcast.id', ondelete='CASCADE'),
                             nullable=False, index=True)
    farmer_id = db.Column(UUID(as_uuid=True), nullable=False)
    day_zero = db.Column(db.DateTime, nullable=True)
