from typing import List, Optional, Annotated

from sqlalchemy import ForeignKey, MetaData, DateTime, Integer, text, Table, Column, select, BigInteger
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship

import enum

from datetime import datetime, timezone

intpk = Annotated[int, mapped_column(primary_key=True, autoincrement=True)]

metadata = MetaData()

class Base(DeclarativeBase):
    pass

class Gender(enum.Enum):
    default_select='default_select'
    man="man"
    woman="woman"

class RoleNames(enum.Enum):
    basic='basic'
    designer='designer'
    dressmaker='dressmaker'
    moderator='moderator'
    administrator='administrator'

class OrderStatuses(enum.Enum):
    new='new'
    canceled='canceled'
    finished='finished'
    in_progress='in_progress'
    on_payment='on_payment'

class PermissionsNames(enum.Enum):
    registered="registered"
    autorized="autorized"
    can_chat="can_chat"
    can_order="can_order"
    can_take_design_order="can_take_design_order"
    can_take_dressmake_order="can_take_dressmake_order"
    can_post_desings="can_post_desings"
    can_post_dressmakes="can_post_dressmakes"
    can_post_in_groupe="can_post_in_group"
    can_accept_payment="can_accept_payment"
    can_join_chats="can_join_chats"
    can_delete_users="can_delete_users"
    can_edit_users="can_edit_users"
    super_user="super_user"

role_permission_associate = Table(
    'rolepermission',
    metadata,
    Column('role_id', ForeignKey("role.id")),
    Column('permission_id', ForeignKey("permission.id"))
)  

class Permission(Base):
    __tablename__='permission'
    metadata=metadata
    id: Mapped[intpk]
    name: Mapped[str]
    roles: Mapped[List["Role"]] = relationship(
        back_populates="permissions", secondary=role_permission_associate
    )

class Role(Base):
    __tablename__='role'
    metadata=metadata
    id: Mapped[intpk]
    name: Mapped["RoleNames"]
    users: Mapped[List["User"]] = relationship(
        back_populates='role'
    )
    permissions: Mapped[List["Permission"]] = relationship(
        back_populates="roles", secondary=role_permission_associate
    )

class Order(Base):
    __tablename__ = "order"
    metadata=metadata
    id: Mapped[intpk]
    status: Mapped["OrderStatuses"] = mapped_column(default=OrderStatuses.new)
    buyer_id: Mapped[int] = mapped_column(ForeignKey("user_account.id"))
    contractor_id: Mapped[int] = mapped_column(ForeignKey("user_account.id"))

    buyer: Mapped["User"] = relationship(
        back_populates="orders_as_buyer", foreign_keys=[buyer_id]
    )
    contractor: Mapped["User"] = relationship(
        back_populates="orders_as_contractor", foreign_keys=[contractor_id]
    )
    cost: Mapped[int|None] = mapped_column(default=None)

class User(Base):
    __tablename__ = "user_account"
    metadata=metadata
    id: Mapped[intpk]
    telegram_id: Mapped[int] = mapped_column(BigInteger, unique=True)
    role_id: Mapped[int] = mapped_column(ForeignKey('role.id'), default=select(Role.id).where(Role.name==RoleNames.basic.value))
    role: Mapped["Role"] = relationship(
        back_populates="users"
    )
    registation_date: Mapped[datetime] = mapped_column( 
        server_default=text("TIMEZONE('utc', now())")
    )
    name: Mapped[str]
    email: Mapped[str|None] = mapped_column(
        server_default=None
    )
    age: Mapped[int|None] = mapped_column(
        server_default=None
    )
    gender: Mapped[Optional["Gender"]]
    # payments: Mapped[List["Payment"]] = relationship(
    #     back_populates='user'
    # )
    orders_as_buyer: Mapped[List["Order"]] = relationship(
        back_populates="buyer", foreign_keys=[Order.buyer_id]
    )
    orders_as_contractor: Mapped[List["Order"]] = relationship(
        back_populates="contractor", foreign_keys=[Order.contractor_id]
    )
    work_forms: Mapped[List["WorkPostForm"]] = relationship(
        back_populates='user'
    )

# class Payment(Base):
#     __tablename__ = 'payment'
#     metadata=metadata
#     id: Mapped[intpk]
#     user: Mapped["User"] = relationship(back_populates="payments")
#     name: Mapped[str]

class WorkPostForm(Base):
    __tablename__ = 'work_post_form'
    metadata=metadata
    id: Mapped[intpk]
    owner_id: Mapped[int] = mapped_column(ForeignKey("user_account.id"))
    user: Mapped["User"] = relationship(
        back_populates='work_forms'
    )
    photo1: Mapped[str]
    photo2: Mapped[str|None]
    photo3: Mapped[str|None]
    name: Mapped[str]
    description: Mapped[str]
    status: Mapped[bool] = mapped_column(default=False)
