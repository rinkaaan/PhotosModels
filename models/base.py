from ksuid import Ksuid
from sqlalchemy import Column, String, DateTime, ColumnElement, Text, Table, ForeignKey, Integer
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import relationship

from nguylinc_python_utils.misc import get_timestamp, get_ksuid
from nguylinc_python_utils.sqlalchemy import BaseExtended

Base = declarative_base()


class AlbumModel(Base, BaseExtended):
    __tablename__ = "albums"
    id = Column(String(length=27), primary_key=True, default=get_ksuid)
    created_at: ColumnElement = Column(DateTime(), default=get_timestamp)
    updated_at: ColumnElement = Column(DateTime(), index=True, default=get_timestamp)
    name = Column(Text(), index=True, unique=True)
    thumbnail_path = Column(String())
    media = relationship("MediaModel", secondary="media_albums", back_populates="albums")


class MediaModel(Base, BaseExtended):
    __tablename__ = "media"
    id = Column(String(length=27), primary_key=True, default=str(Ksuid()))
    created_at: ColumnElement = Column(DateTime(), default=get_timestamp)
    uploaded_at: ColumnElement = Column(String())
    thumbnail_path = Column(String())
    duration = Column(Integer(), index=True)
    webpage_url = Column(String())
    albums = relationship("AlbumModel", secondary="media_albums", back_populates="media")


association_table = Table(
    "media_albums",
    Base.metadata,
    Column("media_id", String(length=36), ForeignKey("media.id"), primary_key=True),
    Column("album_id", String(length=36), ForeignKey("albums.id"), primary_key=True),
)
