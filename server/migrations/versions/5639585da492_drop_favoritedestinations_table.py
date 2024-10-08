"""drop favoriteDestinations table

Revision ID: 5639585da492
Revises: d94914684480
Create Date: 2024-07-28 09:30:21.389640

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '5639585da492'
down_revision = 'd94914684480'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('favoriteDestinations')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('favoriteDestinations',
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.Column('user_id', sa.INTEGER(), nullable=False),
    sa.Column('destination_id', sa.INTEGER(), nullable=False),
    sa.Column('is_favorite', sa.BOOLEAN(), nullable=True),
    sa.ForeignKeyConstraint(['destination_id'], ['destinations.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###
