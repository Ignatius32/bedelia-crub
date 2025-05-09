"""add asignatura_id and asignatura_info to actividades

Revision ID: 001_add_asignatura_fields
Revises: 
Create Date: 2023-05-09 12:00:00.000000

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '001_add_asignatura_fields'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # Agregar columnas nuevas a la tabla actividades
    op.add_column('actividades', sa.Column('asignatura_id', sa.Integer(), nullable=True))
    op.add_column('actividades', sa.Column('asignatura_info', sa.Text(), nullable=True))


def downgrade():
    # Eliminar columnas agregadas en upgrade
    op.drop_column('actividades', 'asignatura_info')
    op.drop_column('actividades', 'asignatura_id')
