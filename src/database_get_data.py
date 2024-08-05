from typing import List, Optional, Annotated

from sqlalchemy import ForeignKey, MetaData, DateTime, Integer, text, select, delete
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship, joinedload

from datetime import datetime, timezone

from app.models import Order, OrderStatuses, RoleNames, PermissionsNames, WorkPostForm
from app.models import User

from database import async_session_maker

import asyncio

async def check_registered_user(telegram_id):
    async with async_session_maker() as session:
        res = select(User.id).where(User.telegram_id==telegram_id)
        ans = await session.execute(res)
        return ans.scalars().all()
    
async def get_check_works():
    async with async_session_maker() as session:
        res = select(WorkPostForm).where(WorkPostForm.status==False).limit(1)
        ans = await session.execute(res)
        first = ans.scalars().first()

        if not first: return None

        first.status = True
        await session.commit()

        return first
    
async def get_user_role_data(telegram_id):
    async with async_session_maker() as session:
        res = select(User).where(User.telegram_id==telegram_id).options(joinedload(User.role)).limit(1)
        ans = await session.execute(res)
        first = ans.scalars().first()

        if first: return first.role.name
        return None

async def get_user_telegram_id_data(id):
    async with async_session_maker() as session:
        res = select(User.telegram_id).where(User.id==id).limit(1)
        ans = await session.execute(res)
        first = ans.scalars().first()

        if first: return first
        return None

async def get_user_id_data(telegram_id):
    async with async_session_maker() as session:
        res = select(User.id).where(User.telegram_id==telegram_id).limit(1)
        ans = await session.execute(res)
        return ans.scalars().one()

async def get_user_account_data(telegram_id):
    async with async_session_maker() as session:
        res = select(User).where(User.telegram_id==telegram_id)
        ans = await session.execute(res)
        return ans.scalars().all()

async def get_order_by_id(id:int, joinned_load:bool=False) -> Order|None:
    async with async_session_maker() as session:
        res = select(Order).where(Order.id == id).limit(1)
        ans = await session.execute(res)
        result = ans.scalars().first()
        if not result: return None
        if joinned_load:
            res = res.options(joinedload(Order.buyer), joinedload(Order.contractor))
            ans = await session.execute(res)
            result = ans.scalars().first()
        return result

async def get_order(buyer:int, contractor:int, statuses:list[OrderStatuses]=['*'], joinned_load:bool=False) -> Order|None:
    async with async_session_maker() as session:
        res = select(Order).where(Order.buyer_id==buyer,
                                     Order.contractor_id==contractor,
                                     Order.status.in_(statuses)
                                     )
        ans = await session.execute(res)
        result = ans.scalars().all()
        if not result: return None
        if joinned_load:
            res = res.options(joinedload(Order.buyer), joinedload(Order.contractor))
            ans = await session.execute(res)
            result = ans.scalars().all()
        return result

if __name__ == "__main__":
    # asyncio.run(add_user(int(input()), input(), input()))
    # asyncio.run(check_add_user())
    pass