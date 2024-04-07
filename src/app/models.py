from typing import List, Optional
from sqlalchemy import ForeignKey, MetaData, DateTime
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from datetime import datetime, timezone


metadata = MetaData()

class Base(DeclarativeBase):
    pass

class User(Base):
    __tablename__ = "user_account"
    metadata=metadata
    id: Mapped[int] = mapped_column(primary_key=True)
    telegram_id: Mapped[int] = mapped_column(nullable=False)
    orders: Mapped[List["Order"]|None] = relationship(
        back_populates="user", cascade="all, delete-orphan"
    )
    def __repr__(self) -> str:
        pass

class Order(Base):
    __tablename__ = "order"
    metadata=metadata
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("user_account.id"))
    user: Mapped["User"] = relationship(
        back_populates="orders"
    )
    date: Mapped[DateTime] = mapped_column(DateTime(timezone=True), default=datetime.now(timezone.utc))
    design_id: Mapped[int] = mapped_column(nullable=False)
    tailor_id: Mapped[int] = mapped_column(nullable=False)
    adress: Mapped[str] = mapped_column(nullable=False)

    def __repr__(self) -> str:
        pass