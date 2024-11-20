from sqlalchemy import select
from db_engine import Base, async_engine, async_session
from models import User, Habit
from pydantic_models import UserHabitData


class AsyncORM:
    @staticmethod
    async def create_tables():
        async with async_engine.begin() as conn:
            await conn.run_sync(Base.metadata.drop_all)
            await conn.run_sync(Base.metadata.create_all)

    @staticmethod
    async def add_user(
        user_id: int,
        username: str,
        firstname: str,
        lastname: str,
    ) -> None:
        async with async_session() as session:
            user = User(
                id=user_id,
                username=username,
                firstname=firstname,
                lastname=lastname,
            )
            session.add(user)
            await session.commit()

    @staticmethod
    async def get_habits(user_id: int) -> list[Habit]:
        async with async_session() as session:
            query = select(Habit).filter(Habit.user_id == user_id)
            res = await session.execute(query)
            return res.scalars().all()

    @staticmethod
    async def edit_habit(user_tg_id: int, habit_id: int):
        async with async_session() as session:
            ...

    @staticmethod
    async def delete_habit(user_tg_id: int, habit_id: int):
        async with async_session() as session:
            ...

    @staticmethod
    async def add_habit(
            data: UserHabitData,
    ) -> None:
        async with async_session() as session:
            habit = Habit(
                name=data.name,
                description=data.description,
                user_id=data.user_id,
            )
            session.add(habit)
            await session.commit()
