"""add market valuation system

Revision ID: b300615a0f8e
Revises: 59fb18904f9a
Create Date: 2026-05-25 15:00:07.429061

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = 'b300615a0f8e'
down_revision = '59fb18904f9a'
branch_labels = None
depends_on = None


def upgrade():

    op.create_table(
        'market_listings',

        sa.Column('id', sa.Integer(), nullable=False),

        sa.Column('source', sa.String(length=50), nullable=True),

        sa.Column('title', sa.String(length=255), nullable=True),

        sa.Column('make', sa.String(length=100), nullable=True),

        sa.Column('model', sa.String(length=100), nullable=True),

        sa.Column('trim', sa.String(length=100), nullable=True),

        sa.Column('year', sa.Integer(), nullable=True),

        sa.Column('mileage', sa.Integer(), nullable=True),

        sa.Column('fuel_type', sa.String(length=50), nullable=True),

        sa.Column('transmission', sa.String(length=50), nullable=True),

        sa.Column('engine_size', sa.Float(), nullable=True),

        sa.Column('location', sa.String(length=100), nullable=True),

        sa.Column('price', sa.Float(), nullable=True),

        sa.Column('image_url', sa.Text(), nullable=True),

        sa.Column('listing_url', sa.Text(), nullable=True),

        sa.Column('scraped_at', sa.DateTime(), nullable=True),

        sa.PrimaryKeyConstraint('id'),

        sa.UniqueConstraint('listing_url')
    )

    op.add_column(
        'vehicle_analysis',
        sa.Column('market_estimate', sa.Float(), nullable=True)
    )

    op.add_column(
        'vehicle_analysis',
        sa.Column('confidence_score', sa.Integer(), nullable=True)
    )

    op.add_column(
        'vehicle_analysis',
        sa.Column('comparable_count', sa.Integer(), nullable=True)
    )


def downgrade():

    op.drop_column(
        'vehicle_analysis',
        'comparable_count'
    )

    op.drop_column(
        'vehicle_analysis',
        'confidence_score'
    )

    op.drop_column(
        'vehicle_analysis',
        'market_estimate'
    )

    op.drop_table('market_listings')