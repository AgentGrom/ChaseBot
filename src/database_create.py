from typing import List, Optional, Annotated

from sqlalchemy import ForeignKey, MetaData, DateTime, Integer, text, select, delete
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship

import enum

from datetime import datetime, timezone

from app.models import RoleNames, PermissionsNames, WorkPostForm, Order
from app.models import Permission, Role, role_permission_associate, User

from database import async_session_maker

import asyncio

user_permissions = {
    "basic": (
        "registered",
        "autorized",
        "can_chat",
        "can_order"
    )
}

async def clear_users(telegram_id):
    async with async_session_maker() as session:
        # if telegram_id is None: query = text(f"""TRUNCATE TABLE {User.__tablename__} RESTART IDENTITY CASCADE""")
        query = delete(User).where(User.telegram_id == telegram_id)
        await session.execute(query)
        await session.commit()

async def clear_forms():
    async with async_session_maker() as session:
        query = text(f"""TRUNCATE TABLE {WorkPostForm.__tablename__} RESTART IDENTITY CASCADE""")
        await session.execute(query)
        await session.commit()

async def clear_orders():
    async with async_session_maker() as session:
        query = text(f'''TRUNCATE TABLE "{Order.__tablename__}" RESTART IDENTITY CASCADE''')
        await session.execute(query)
        await session.commit()


async def create_associates():
    await create_permissions()
    await create_roles()
    async with async_session_maker() as session:
        await session.execute(role_permission_associate.delete())
        await session.commit()
        for user in RoleNames:
            query = select(Permission).where(Permission.name.in_(user_permissions.get(user.value, [])))
            answer = await session.execute(query)
            session.add(Role(name=user.value, permissions=answer.scalars().all()))
        await session.commit()

async def create_roles():
    async with async_session_maker() as session:
        query = text(f"""TRUNCATE TABLE {Role.__tablename__} RESTART IDENTITY CASCADE""")
        await session.execute(query)
        await session.flush()
        # session.add_all([Role(name=role_name.value) for role_name in RoleNames])
        await session.commit()

async def create_permissions():
    async with async_session_maker() as session:
        query = text(f"""TRUNCATE TABLE {Permission.__tablename__} RESTART IDENTITY CASCADE""")
        await session.execute(query)
        await session.flush()
        for permission_name in PermissionsNames:
            session.add(
                Permission(name=permission_name.value)
            )
        await session.commit()

async def main():
    async with async_session_maker() as session:
        res = await session.execute(text("SELECT VERSION()"))
        print(f"{res.all()=}")

if __name__ == "__main__":
    asyncio.run(clear_users())