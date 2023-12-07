"""callableuser, admin, password model

Revision ID: eb9cc94cb57d
Revises: 
Create Date: 2023-12-05 20:06:27.430250

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'eb9cc94cb57d'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('callable_users',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('is_superuser', sa.Boolean(), nullable=True),
    sa.Column('email', sa.String(), nullable=False),
    sa.Column('phone_number', sa.String(length=10), nullable=True),
    sa.Column('is_staff', sa.Boolean(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('phone_number')
    )
    op.create_index(op.f('ix_callable_users_email'), 'callable_users', ['email'], unique=True)
    op.create_index(op.f('ix_callable_users_id'), 'callable_users', ['id'], unique=False)
    op.create_table('password_table',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('password', sa.LargeBinary(length=255), nullable=True),
    sa.Column('hashed_special_key', sa.LargeBinary(length=255), nullable=True),
    sa.Column('is_enabled', sa.Boolean(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_password_table_hashed_special_key'), 'password_table', ['hashed_special_key'], unique=False)
    op.create_table('admins',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('callable_user_id', sa.Integer(), nullable=True),
    sa.Column('is_active', sa.Boolean(), nullable=True),
    sa.Column('salt', sa.LargeBinary(), nullable=True),
    sa.Column('special_key', sa.LargeBinary(), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.Column('is_auto_password', sa.Boolean(), nullable=True),
    sa.ForeignKeyConstraint(['callable_user_id'], ['callable_users.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('special_key')
    )
    op.create_index(op.f('ix_admins_id'), 'admins', ['id'], unique=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_admins_id'), table_name='admins')
    op.drop_table('admins')
    op.drop_index(op.f('ix_password_table_hashed_special_key'), table_name='password_table')
    op.drop_table('password_table')
    op.drop_index(op.f('ix_callable_users_id'), table_name='callable_users')
    op.drop_index(op.f('ix_callable_users_email'), table_name='callable_users')
    op.drop_table('callable_users')
    # ### end Alembic commands ###
