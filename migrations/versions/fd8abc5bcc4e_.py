"""empty message

Revision ID: fd8abc5bcc4e
Revises: 9e72b65b4d69
Create Date: 2020-08-15 23:43:19.466971

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'fd8abc5bcc4e'
down_revision = '9e72b65b4d69'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user_account', sa.Column('is_active', sa.Boolean(), server_default='1', nullable=False))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('user_account', 'is_active')
    # ### end Alembic commands ###
