"""add age column and check constraint

Revision ID: 71f86b2f8517
Revises: 4bb73bd04e1c
Create Date: 2024-07-28 06:50:49.426915

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '71f86b2f8517'
down_revision = '4bb73bd04e1c'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.add_column(sa.Column('age', sa.Integer(), nullable=True))
        batch_op.create_check_constraint(
            'check_age',
            sa.text('age > 15')
        )

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.drop_constraint('check_age', type_='check')
        batch_op.drop_column('age')

    # ### end Alembic commands ###
