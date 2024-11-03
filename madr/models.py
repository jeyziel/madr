from sqlalchemy.orm import Mapped, mapped_column, registry, relationship 
from sqlalchemy import ForeignKey, func
from datetime import datetime


table_registry = registry()

@table_registry.mapped_as_dataclass
class User:
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(init=False, primary_key=True)
    username: Mapped[str] = mapped_column(unique=True)
    email: Mapped[str] = mapped_column(unique=True)
    password: Mapped[str]
    created_at: Mapped[datetime] = mapped_column(
        init=False, server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        init=False,
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )


@table_registry.mapped_as_dataclass
class Romancist:
    __tablename__ = 'romancistas'

    id: Mapped[int] = mapped_column(unique=True, primary_key=True)
    nome: Mapped[str]
    created_at: Mapped[datetime] = mapped_column(
        init=False, server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        init=False,
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )

    todos: Mapped[list['Book']] = relationship(
        init=False, back_populates='romancista', cascade='all, delete-orphan'
    )




@table_registry.mapped_as_dataclass
class Book:
    __tablename__ = 'livros'

    id: Mapped[int] = mapped_column(unique=True, primary_key=True)
    ano: Mapped[int]
    titulo: Mapped[str]

    romancista_id: Mapped[int] = mapped_column(ForeignKey('romancistas.id'))
    romancistas: Mapped[Romancist] = relationship(init=False, back_populates='romancistas')

    created_at: Mapped[datetime] = mapped_column(
        init=False, server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        init=False,
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )







