from uuid import uuid4
from sqlalchemy import ForeignKey, String, BigInteger
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Uuid
from uuid import uuid4, UUID as PythonUUID

from database.database import Base


# Модель для таблицы пользователей
class User(Base):
    __tablename__ = 'user'

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    
    username: Mapped[str] = mapped_column(String, nullable=True)
    full_name: Mapped[str] = mapped_column(String, nullable=True)

    requests: Mapped[list["Request"]] = relationship("Request", back_populates="user", cascade="all, delete-orphan")



class Request(Base):
    __tablename__ = 'request'

    
    id: Mapped[PythonUUID] = mapped_column(
        Uuid,
        primary_key=True,
        default=uuid4 
    )

    user: Mapped["User"] = relationship("User", back_populates="requests")
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"))

    region: Mapped["Region"] = relationship("Region", back_populates="requests")
    region_id: Mapped[Uuid] = mapped_column(ForeignKey("region.id"))

    game: Mapped["Game"] = relationship("Game", back_populates="requests")
    game_id: Mapped[Uuid] = mapped_column(ForeignKey("game.id"))

    gameid: Mapped[str] = mapped_column(String, nullable=True)
    top: Mapped[str] = mapped_column(String, nullable=True)
    position: Mapped[str] = mapped_column(String, nullable=True)


class Region(Base):
    __tablename__ = 'region'

    
    id: Mapped[PythonUUID] = mapped_column(
        Uuid,
        primary_key=True,
        default=uuid4 
    )

    requests: Mapped[list["Request"]] = relationship("Request", back_populates="region", cascade="all, delete-orphan")
    name: Mapped[str] = mapped_column(String, nullable=False)


class Game(Base):
    __tablename__ = 'game'

    
    id: Mapped[PythonUUID] = mapped_column(
        Uuid,
        primary_key=True,
        default=uuid4 
    )

    requests: Mapped[list["Request"]] = relationship("Request", back_populates="game", cascade="all, delete-orphan")
    name: Mapped[str] = mapped_column(String, nullable=False)
