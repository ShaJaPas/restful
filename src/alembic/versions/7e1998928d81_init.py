"""Init

Revision ID: 7e1998928d81
Revises: 
Create Date: 2022-12-14 15:50:15.085688

"""
from alembic import op
import sqlalchemy as sa
import sqlmodel


# revision identifiers, used by Alembic.
revision = '7e1998928d81'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('dbperson',
    sa.Column('name', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    sa.Column('sirname', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    sa.Column('birthday', sa.Date(), nullable=False),
    sa.Column('id', sa.Integer(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('dbperson')
    # ### end Alembic commands ###
