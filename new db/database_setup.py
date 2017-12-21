import os
import sys
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

Base = declarative_base()


class Catagory(Base):
    __tablename__ = "catagory"

    name = Column(String(80), nullable=False)
    id = Column(Integer, primary_key=True)


class Items(Base):
    __tablename__ = "items"

    name = Column(String(80), nullable=False)
    id = Column(Integer, primary_key=True)
    catagory_id = Column(Integer, ForeignKey('catagory.id'))
    catagory = relationship(Catagory)
    description = Column(String(250))
    user_id = Column(String(80))


engine = create_engine(
    'sqlite:///items.db')

Base.metadata.create_all(engine)


if __name__ == "__main__":
    print ("works great")
