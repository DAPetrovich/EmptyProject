"""empty message

Revision ID: 4e6c03a44767
Revises: 3fc242170c45
Create Date: 2022-06-09 11:30:17.743311

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '4e6c03a44767'
down_revision = '3fc242170c45'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('sostav', sa.Column('ingredients_id', sa.Integer(), nullable=True))
    op.add_column('sostav', sa.Column('menu_id', sa.Integer(), nullable=True))
    op.drop_constraint('sostav_ingredients_fkey', 'sostav', type_='foreignkey')
    op.drop_constraint('sostav_menu_fkey', 'sostav', type_='foreignkey')
    op.create_foreign_key(None, 'sostav', 'ingredient', ['ingredients_id'], ['id'])
    op.create_foreign_key(None, 'sostav', 'menu', ['menu_id'], ['id'])
    op.drop_column('sostav', 'menu')
    op.drop_column('sostav', 'ingredients')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('sostav', sa.Column('ingredients', sa.INTEGER(), autoincrement=False, nullable=True))
    op.add_column('sostav', sa.Column('menu', sa.INTEGER(), autoincrement=False, nullable=True))
    op.drop_constraint(None, 'sostav', type_='foreignkey')
    op.drop_constraint(None, 'sostav', type_='foreignkey')
    op.create_foreign_key('sostav_menu_fkey', 'sostav', 'menu', ['menu'], ['id'])
    op.create_foreign_key('sostav_ingredients_fkey', 'sostav', 'ingredient', ['ingredients'], ['id'])
    op.drop_column('sostav', 'menu_id')
    op.drop_column('sostav', 'ingredients_id')
    # ### end Alembic commands ###