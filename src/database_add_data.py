from typing import List, Optional, Annotated

from sqlalchemy import ForeignKey, MetaData, DateTime, Integer, text, select, delete, update
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship, joinedload

from datetime import datetime, timezone

from app.models import Order, OrderStatuses, RoleNames, PermissionsNames, WorkPostForm
from app.models import User

from database import async_session_maker

import asyncio

async def all_forms_to_false(*_):
    async with async_session_maker() as session:
        res = select(WorkPostForm)
        ans = await session.execute(res)
        forms = ans.scalars().all()

        for form in forms:
            form.status = False
        
        await session.commit()

async def add_form_status_return(id: int):
    async with async_session_maker() as session:
        res = select(WorkPostForm).where(WorkPostForm.id==id).limit(1)
        ans = await session.execute(res)
        form = ans.scalars().first()
        form.status = False
        await session.commit()

async def add_check_works(telegram_id, name, description, photo1, photo2=None, photo3=None, status=False):
    async with async_session_maker() as session:
        res = select(User.id).where(User.telegram_id==telegram_id).limit(1)
        ans = await session.execute(res)
        owner_id = ans.scalars().first()

        work = WorkPostForm(owner_id=owner_id, 
                            name=name, 
                            description=description, 
                            photo1=photo1, 
                            photo2=photo2, 
                            photo3=photo3,
                            status=status)
        session.add(work)
        await session.commit()

async def add_user(telegram_id, name, email=None, age=None, gender=None):
    async with async_session_maker() as session:
        
        user = User(telegram_id=telegram_id, name=name)
        if not(email is None): user.email=email  
        if not(age is None): user.age=age  
        if not(gender is None): user.gender=gender
        session.add(user)
        await session.commit()

async def add_new_user_role(telegram_id, new_role):
    async with async_session_maker() as session:
        res = update(User).where(User.telegram_id==telegram_id).values(role_id=new_role)
        await session.execute(res)
        await session.commit()

async def check_add_user():
    async with async_session_maker() as session:
        res = select(User).options(joinedload(User.role))
        ans = await session.execute(res)
        print(ans.scalars().first().role.name)

async def add_create_order(buyer:int, contractor:int):
    async with async_session_maker() as session:
        order = Order(buyer_id=buyer,contractor_id=contractor)
        session.add(order)
        await session.commit()

async def order_set_status(id:int, status:OrderStatuses):
    async with async_session_maker() as session:
        res = select(Order).where(Order.id == id).limit(1)
        ans = await session.execute(res)
        forms = ans.scalars().first()
        forms.status = status
        await session.commit()

async def order_set_cost(id:int, cost:int):
    async with async_session_maker() as session:
        res = select(Order).where(Order.id == id).limit(1)
        ans = await session.execute(res)
        forms = ans.scalars().first()
        forms.cost = cost
        await session.commit()


if __name__ == "__main__":
    # asyncio.run(add_user(int(input()), input(), input()))
    # asyncio.run(check_add_user())
    pass