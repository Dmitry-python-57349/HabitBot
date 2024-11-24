from sqlalchemy import select, delete, update
from src.backend.db_engine import Base, async_engine, async_session
from src.backend.models import User, Habit
from src.backend.pydantic_models import UserHabitData, UserData


class AsyncORM:
    @staticmethod
    async def create_tables():
        async with async_engine.begin() as conn:
            await conn.run_sync(Base.metadata.drop_all)
            await conn.run_sync(Base.metadata.create_all)

    @staticmethod
    async def user_ids() -> list[int]:
        async with async_session() as session:
            stmt = select(User.id)
            result = await session.execute(stmt)
            return result.scalars().all()

    @staticmethod
    async def add_user(user: UserData) -> int:
        async with async_session() as session:
            user = User(
                id=user.user_id,
                username=user.username,
                firstname=user.firstname,
                lastname=user.lastname,
            )
            session.add(user)
            await session.flush()
            await session.refresh(user)
            user_id = user.id
            await session.commit()
            return user_id

    @staticmethod
    async def get_habits(user_id: int) -> list[Habit]:
        async with async_session() as session:
            stmt = select(Habit).filter(Habit.user_id == user_id)
            res = await session.execute(stmt)
            return res.scalars().all()

    @staticmethod
    async def edit_habit(habit_id: int, **kwargs) -> None:
        async with async_session() as session:
            stmt = update(Habit).where(Habit.id == habit_id).values(**kwargs)
            await session.execute(stmt)
            await session.commit()

    @staticmethod
    async def delete_habit(habit_id: int) -> None:
        async with async_session() as session:
            stmt = delete(Habit).where(Habit.id == habit_id)
            await session.execute(stmt)
            await session.commit()

    @staticmethod
    async def add_habit(data: UserHabitData) -> int:
        async with async_session() as session:
            habit = Habit(
                name=data.name,
                description=data.description,
                user_id=data.user_id,
            )
            session.add(habit)
            await session.flush()
            await session.refresh(habit)
            habit_id = habit.id
            await session.commit()
            return habit_id

    @staticmethod
    async def update_marks_to_false() -> None:
        async with async_session() as session:
            stmt = update(Habit).values(today_mark=False)
            await session.execute(stmt)
            await session.commit()
