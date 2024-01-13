from sqlalchemy import (
    String,
    BigInteger,
    SmallInteger,
    ForeignKey,
    Boolean
)
from sqlalchemy.orm import (
    relationship,
    declarative_base,
    mapped_column,
    Mapped
)

Base = declarative_base()


class DatabaseUser(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(BigInteger, autoincrement=True, primary_key=True, index=True)
    username: Mapped[str] = mapped_column(String(16), nullable=False)
    full_name: Mapped[str] = mapped_column(String(150), nullable=False)
    email: Mapped[str] = mapped_column(String(150), nullable=False)
    lang_id: Mapped[int] = mapped_column(ForeignKey("langs.id"), nullable=False)
    lang = relationship("DatabaseLang", back_populates="user", lazy="selectin")


class DatabaseLang(Base):
    __tablename__ = "langs"

    id: Mapped[int] = mapped_column(SmallInteger, autoincrement=True, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(32), nullable=False)
    cyrillic: Mapped[bool] = mapped_column(Boolean, default=False)
    user = relationship("DatabaseUser", back_populates="lang", lazy="selectin")
