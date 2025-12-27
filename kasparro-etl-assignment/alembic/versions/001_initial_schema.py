"""Initial schema

Revision ID: 001_initial
Revises: 
Create Date: 2024-01-01 00:00:00.000000

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '001_initial'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Raw tables
    op.create_table(
        'raw_coinpaprika',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('source_name', sa.String(), nullable=False),
        sa.Column('payload', postgresql.JSON(astext_type=sa.Text()), nullable=False),
        sa.Column('fetched_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index('idx_coinpaprika_fetched', 'raw_coinpaprika', ['fetched_at'])
    
    op.create_table(
        'raw_coingecko',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('source_name', sa.String(), nullable=False),
        sa.Column('payload', postgresql.JSON(astext_type=sa.Text()), nullable=False),
        sa.Column('fetched_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index('idx_coingecko_fetched', 'raw_coingecko', ['fetched_at'])
    
    op.create_table(
        'raw_csv_source',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('source_name', sa.String(), nullable=False),
        sa.Column('payload', postgresql.JSON(astext_type=sa.Text()), nullable=False),
        sa.Column('fetched_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index('idx_csv_fetched', 'raw_csv_source', ['fetched_at'])
    
    # Unified assets table
    op.create_table(
        'assets',
        sa.Column('asset_id', sa.Integer(), nullable=False),
        sa.Column('symbol', sa.String(), nullable=False),
        sa.Column('name', sa.String(), nullable=False),
        sa.Column('price_usd', sa.Float(), nullable=True),
        sa.Column('market_cap', sa.Float(), nullable=True),
        sa.Column('source', sa.String(), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.PrimaryKeyConstraint('asset_id')
    )
    op.create_index('ix_assets_asset_id', 'assets', ['asset_id'])
    op.create_index('ix_assets_symbol', 'assets', ['symbol'])
    op.create_index('ix_assets_source', 'assets', ['source'])
    op.create_index('idx_assets_symbol_source', 'assets', ['symbol', 'source'], unique=True)
    op.create_index('idx_assets_updated', 'assets', ['updated_at'])
    
    # Checkpoint table
    op.create_table(
        'etl_checkpoints',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('source', sa.String(), nullable=False),
        sa.Column('last_processed_id', sa.Integer(), nullable=True),
        sa.Column('last_processed_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('status', sa.String(), nullable=False),
        sa.Column('run_id', sa.String(), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index('ix_etl_checkpoints_id', 'etl_checkpoints', ['id'])
    op.create_index('ix_etl_checkpoints_source', 'etl_checkpoints', ['source'], unique=True)


def downgrade() -> None:
    op.drop_index('ix_etl_checkpoints_source', table_name='etl_checkpoints')
    op.drop_index('ix_etl_checkpoints_id', table_name='etl_checkpoints')
    op.drop_table('etl_checkpoints')
    
    op.drop_index('idx_assets_updated', table_name='assets')
    op.drop_index('idx_assets_symbol_source', table_name='assets')
    op.drop_index('ix_assets_source', table_name='assets')
    op.drop_index('ix_assets_symbol', table_name='assets')
    op.drop_index('ix_assets_asset_id', table_name='assets')
    op.drop_table('assets')
    
    op.drop_index('idx_csv_fetched', table_name='raw_csv_source')
    op.drop_table('raw_csv_source')
    
    op.drop_index('idx_coingecko_fetched', table_name='raw_coingecko')
    op.drop_table('raw_coingecko')
    
    op.drop_index('idx_coinpaprika_fetched', table_name='raw_coinpaprika')
    op.drop_table('raw_coinpaprika')
