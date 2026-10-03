from datetime import date, datetime
from decimal import Decimal

from sqlalchemy import (
    BigInteger,
    CheckConstraint,
    Date,
    ForeignKey,
    Identity,
    Numeric,
    Text,
    func,
    text,
    true,
)
from sqlalchemy.dialects.postgresql import ExcludeConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from backend.db import Base


class Medicine(Base):
    __tablename__ = "medicines"

    __table_args__ = (
        CheckConstraint("code <> ''", name="code_not_empty"),
        CheckConstraint("name <> ''", name="name_not_empty"),
        CheckConstraint("form <> ''", name="form_not_empty"),
        CheckConstraint("strength_unit <> ''", name="strength_unit_not_empty"),
        CheckConstraint("strength_value > 0", name="strength_value_positive"),
    )

    id: Mapped[int] = mapped_column(BigInteger, Identity(), primary_key=True)
    code: Mapped[str] = mapped_column(Text, unique=True)
    name: Mapped[str] = mapped_column(Text)
    form: Mapped[str] = mapped_column(Text)
    strength_value: Mapped[Decimal] = mapped_column(Numeric)
    strength_unit: Mapped[str] = mapped_column(Text)
    is_active: Mapped[bool] = mapped_column(server_default=true())

    # Relationships
    rules: Mapped[list["FormularyRule"]] = relationship(
        back_populates="medicine", lazy="raise"
    )


class FormularyRule(Base):
    __tablename__ = "formulary_rules"

    __table_args__ = (
        CheckConstraint("effective_to >= effective_from", name="period_valid"),
        CheckConstraint(
            "max_quantity_per_dispense > 0",
            name="max_quantity_per_dispense_positive",
        ),
        CheckConstraint(
            "max_quantity_per_30_days > 0",
            name="max_quantity_per_30_days_positive",
        ),
        CheckConstraint(
            "max_quantity_per_dispense <= max_quantity_per_30_days",
            name="max_qty_lte_max_per_30_days",
        ),
        ExcludeConstraint(
            ("medicine_id", "="),
            (text("daterange(effective_from, effective_to, '[]')"), "&&"),
            using="gist",
            name="ex_formulary_rules_no_overlap",
        ),
    )

    id: Mapped[int] = mapped_column(BigInteger, Identity(), primary_key=True)
    medicine_id: Mapped[int] = mapped_column(ForeignKey("medicines.id"))
    effective_from: Mapped[date] = mapped_column(Date)
    effective_to: Mapped[date | None] = mapped_column(Date)
    max_quantity_per_dispense: Mapped[Decimal] = mapped_column(Numeric(10, 2))
    max_quantity_per_30_days: Mapped[Decimal] = mapped_column(Numeric(10, 2))
    requires_authorisation: Mapped[bool] = mapped_column()
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())

    # Relationships
    medicine: Mapped["Medicine"] = relationship(back_populates="rules", lazy="raise")


__all__ = ["Base", "FormularyRule", "Medicine"]
