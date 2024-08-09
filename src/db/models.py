from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()

class CanteenInfo(Base):
    __tablename__ = 'canteen_info'
    id = Column(Integer, primary_key=True)
    canteen_name = Column(String, nullable=False)
    floor_number = Column(Integer, nullable=False)
    stall_name = Column(String, nullable=False)
