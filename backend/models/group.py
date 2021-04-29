from core.db import Base
from sqlalchemy import Column, Integer, ForeignKey, SmallInteger
from sqlalchemy.orm import relationship


class Group(Base):
    id = Column(Integer, primary_key=True)
    program_id = Column(Integer, ForeignKey("program.id"))
    program = relationship("Program", backref="groups")
    sem = Column(SmallInteger)
    # join_year = Column(SmallInteger)
    __tablename__ = "group"
