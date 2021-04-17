"""table

Revision ID: 04244b935b00
Revises: 0650daca7648
Create Date: 2021-04-14 14:39:49.215548

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '04244b935b00'
down_revision = '0650daca7648'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('class_session',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('datetime', sa.DateTime(), nullable=True),
    sa.Column('is_active', sa.Boolean(), nullable=True),
    sa.Column('course_id', sa.Integer(), nullable=True),
    sa.Column('description', sa.String(length=128), nullable=True),
    sa.ForeignKeyConstraint(['course_id'], ['course.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('user_class_session_association',
    sa.Column('class_session_id', sa.Integer(), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['class_session_id'], ['class_session.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], )
    )
    op.create_table('user_course_association',
    sa.Column('course_id', sa.Integer(), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['course_id'], ['course.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], )
    )
    op.drop_table('association')
    op.drop_table('classsession')
    op.add_column('user', sa.Column('department_id', sa.Integer(), nullable=True))
    op.create_foreign_key(None, 'user', 'department', ['department_id'], ['id'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'user', type_='foreignkey')
    op.drop_column('user', 'department_id')
    op.create_table('classsession',
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('datetime', postgresql.TIMESTAMP(), autoincrement=False, nullable=True),
    sa.Column('course_id', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('description', sa.VARCHAR(length=128), autoincrement=False, nullable=True),
    sa.ForeignKeyConstraint(['course_id'], ['course.id'], name='classsession_course_id_fkey'),
    sa.PrimaryKeyConstraint('id', name='classsession_pkey')
    )
    op.create_table('association',
    sa.Column('course_id', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('user_id', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.ForeignKeyConstraint(['course_id'], ['course.id'], name='association_course_id_fkey'),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], name='association_user_id_fkey')
    )
    op.drop_table('user_course_association')
    op.drop_table('user_class_session_association')
    op.drop_table('class_session')
    # ### end Alembic commands ###