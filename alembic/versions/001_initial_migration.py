"""Initial migration

Revision ID: 001
Revises: 
Create Date: 2024-04-26 12:00:00.000000

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '001'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        'part',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True, server_default=sa.text('gen_random_uuid()')),
        sa.Column('name', sa.String(150), nullable=False),
        sa.Column('sku', sa.String(30), nullable=False, unique=True),
        sa.Column('description', sa.String(1024)),
        sa.Column('weight_ounces', sa.Integer),
        sa.Column('is_active', sa.Boolean, default=True)
    )


def downgrade() -> None:
    op.drop_table('part') 