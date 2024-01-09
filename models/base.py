import uuid

from sqlalchemy import Column, String, DateTime, ColumnElement, Text, Table, ForeignKey
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import relationship

from nguylinc_python_utils.misc import get_timestamp
from nguylinc_python_utils.sqlalchemy import BaseExtended

Base = declarative_base()


class AlbumModel(Base, BaseExtended):
    __tablename__ = "albums"
    id = Column(String(length=36), primary_key=True, default=str(uuid.uuid4()))
    created_at: ColumnElement = Column(DateTime(), index=True, default=get_timestamp())
    updated_at: ColumnElement = Column(DateTime(), index=True, default=get_timestamp())
    name = Column(Text(), index=True)
    thumbnail_path = Column(String())
    serializable_fields = ["id", "created_at", "updated_at", "name", "thumbnail_path"]
    media = relationship("MediaModel", secondary="media_albums", back_populates="albums")


class MediaModel(Base, BaseExtended):
    __tablename__ = "media"
    id = Column(String(length=36), primary_key=True, default=str(uuid.uuid4()))
    created_at: ColumnElement = Column(DateTime(), index=True, default=get_timestamp())
    updated_at: ColumnElement = Column(DateTime(), index=True, default=get_timestamp())
    title = Column(Text(), index=True)
    thumbnail_path = Column(String())
    albums = relationship("AlbumModel", secondary="media_albums", back_populates="media")
    serializable_fields = ["id", "created_at", "updated_at", "title", "thumbnail_path"]


association_table = Table(
    "media_albums",
    Base.metadata,
    Column("media_id", String(length=36), ForeignKey("media.id")),
    Column("album_id", String(length=36), ForeignKey("albums.id")),
)
