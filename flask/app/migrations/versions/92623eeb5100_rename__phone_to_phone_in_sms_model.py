"""rename _phone to phone in sms model

Revision ID: 92623eeb5100
Revises: 6dc3b9a53f26
Create Date: 2020-08-14 09:11:43.802877

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '92623eeb5100'
down_revision = '6dc3b9a53f26'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('sms_message', sa.Column('phone', sa.String(), nullable=False), schema='sms')
    op.drop_column('sms_message', '_phone', schema='sms')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('sms_message', sa.Column('_phone', sa.VARCHAR(), server_default=sa.text("'[]'::character varying"), autoincrement=False, nullable=False), schema='sms')
    op.drop_column('sms_message', 'phone', schema='sms')
    # ### end Alembic commands ###
