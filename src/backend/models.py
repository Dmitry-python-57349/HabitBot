from datetime import datetime, timedelta, timezone
from typing import Annotated

from sqlalchemy import text, BIGINT, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
from db_engine import Base


bigint = Annotated[int, mapped_column(BIGINT)]
created_at = Annotated[
    datetime,
    mapped_column(
        server_default=text("TIMEZONE('Europe/Moscow', now())"),
    ),
]


class User(Base):
    __tablename__ = "users"

    id: Mapped[bigint] = mapped_column(primary_key=True)
    username: Mapped[str]
    firstname: Mapped[str]
    lastname: Mapped[str]
    join_at: Mapped[created_at]

    def __repr__(self):
        return f"<{self.__class__.__name__}: {self.id}> {self.username} | {self.fullname} | {self.join_at}"

    @property
    def fullname(self):
        return f"{self.firstname} {self.lastname}"


class Habit(Base):
    __tablename__ = "users_habits"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    description: Mapped[str]
    created_at: Mapped[created_at]
    user_id: Mapped[bigint] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"))

    def __repr__(self):
        return f"<{self.__class__.__name__}: {self.id}> {self.name}"
