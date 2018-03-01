from sqlalchemy import create_engine, ForeignKey
from sqlalchemy import Column, Date, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, backref

engine = create_engine('mysql+mysqlconnector://root:111111@10.245.39.75:3306/test', echo=True)
Base = declarative_base()


class Artist(Base):
    __tablename__ = "artists"

    id = Column(Integer, primary_key=True)
    name = Column(String(64))

    def __repr__(self):
        return "<Artist: {}>".format(self.name)


class Album(Base):
    """"""
    __tablename__ = "albums"

    id = Column(Integer, primary_key=True)
    title = Column(String(64))
    release_date = Column(String(64))
    publisher = Column(String(64))
    media_type = Column(String(64))

    artist_id = Column(Integer, ForeignKey("artists.id"))
    artist = relationship("Artist", backref=backref(
        "albums", order_by=id))


# create tables
Base.metadata.create_all(engine)
