"""Initial migration: create tournaments and players tables

Revision ID: 001
Revises:
Create Date: 2025-06-07 12:00:00.000000

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "001"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Create tournaments table
    op.create_table(
        "tournaments",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(length=255), nullable=False),
        sa.Column("max_players", sa.Integer(), nullable=False),
        sa.Column("start_at", sa.DateTime(timezone=True), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_tournaments_id"), "tournaments", ["id"], unique=False)

    # Create players table
    op.create_table(
        "players",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(length=255), nullable=False),
        sa.Column("email", sa.String(length=255), nullable=False),
        sa.Column("tournament_id", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(
            ["tournament_id"],
            ["tournaments.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("email", "tournament_id", name="uq_email_tournament"),
    )
    op.create_index(op.f("ix_players_id"), "players", ["id"], unique=False)


def downgrade() -> None:
    op.drop_index(op.f("ix_players_id"), table_name="players")
    op.drop_table("players")
    op.drop_index(op.f("ix_tournaments_id"), table_name="tournaments")
    op.drop_table("tournaments")
