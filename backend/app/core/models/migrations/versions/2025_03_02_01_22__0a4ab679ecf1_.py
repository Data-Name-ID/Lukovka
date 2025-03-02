from collections.abc import Sequence

import sqlalchemy as sa
import sqlmodel.sql.sqltypes
from alembic import op

revision: str = "0a4ab679ecf1"
down_revision: str | None = None
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.create_table(
        "depots",
        sa.Column("name", sqlmodel.sql.sqltypes.AutoString(), nullable=False),
        sa.Column("region", sqlmodel.sql.sqltypes.AutoString(), nullable=False),
        sa.Column("id", sa.BigInteger(), nullable=False),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_depots")),
    )
    op.create_table(
        "fuels",
        sa.Column("name", sqlmodel.sql.sqltypes.AutoString(), nullable=False),
        sa.Column("id", sa.BigInteger(), nullable=False),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_fuels")),
    )
    op.create_table(
        "users",
        sa.Column("activated", sa.Boolean(), nullable=False),
        sa.Column("is_admin", sa.Boolean(), nullable=False),
        sa.Column("email", sa.VARCHAR(length=254), nullable=False),
        sa.Column("password", sa.VARCHAR(length=1024), nullable=False),
        sa.Column("id", sa.BigInteger(), nullable=False),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_users")),
    )
    op.create_index(op.f("ix_users_email"), "users", ["email"], unique=True)
    op.create_table(
        "lots",
        sa.Column("price", sa.Float(), nullable=False),
        sa.Column("current_volume", sa.Float(), nullable=False),
        sa.Column(
            "status",
            sa.Enum("CONFIRMED", "SOLD_OUT", name="lot_status"),
            nullable=True,
        ),
        sa.Column("initial_volume", sa.Float(), nullable=False),
        sa.Column("date", sa.DateTime(), nullable=False),
        sa.Column("depot_id", sa.Integer(), nullable=False),
        sa.Column("fuel_id", sa.Integer(), nullable=False),
        sa.Column("id", sa.BigInteger(), nullable=False),
        sa.ForeignKeyConstraint(
            ["depot_id"],
            ["depots.id"],
            name=op.f("fk_lots_depot_id_depots"),
        ),
        sa.ForeignKeyConstraint(
            ["fuel_id"],
            ["fuels.id"],
            name=op.f("fk_lots_fuel_id_fuels"),
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_lots")),
    )
    op.create_table(
        "orders",
        sa.Column(
            "status",
            sa.Enum("CONFIRMED", "IN_PROGRESS", "COMPLETED", "CANCELED", name="status"),
            nullable=True,
        ),
        sa.Column(
            "created_datetime",
            sa.TIMESTAMP(timezone=True),
            server_default=sa.text("CURRENT_TIMESTAMP"),
            nullable=False,
        ),
        sa.Column(
            "updated_datetime",
            sa.TIMESTAMP(timezone=True),
            server_default=sa.text("CURRENT_TIMESTAMP"),
            nullable=False,
        ),
        sa.Column("volume", sa.Float(), nullable=False),
        sa.Column(
            "delivery_type",
            sa.Enum("DELIVERY", "SELF_PICKUP", name="delivery_type"),
            nullable=True,
        ),
        sa.Column("lot_id", sa.Integer(), nullable=True),
        sa.Column("id", sa.BigInteger(), nullable=False),
        sa.Column("user_id", sa.Integer(), nullable=True),
        sa.ForeignKeyConstraint(
            ["lot_id"],
            ["lots.id"],
            name=op.f("fk_orders_lot_id_lots"),
        ),
        sa.ForeignKeyConstraint(
            ["user_id"],
            ["users.id"],
            name=op.f("fk_orders_user_id_users"),
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_orders")),
    )


def downgrade() -> None:
    op.drop_table("orders")
    op.drop_table("lots")
    op.drop_index(op.f("ix_users_email"), table_name="users")
    op.drop_table("users")
    op.drop_table("fuels")
    op.drop_table("depots")
