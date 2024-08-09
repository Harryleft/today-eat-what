from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()

class CanteenInfo(Base):
    __tablename__ = 'canteen_info'
    id = Column(Integer, primary_key=True)
    canteen_name = Column(String, nullable=False)
    floor_number = Column(Integer, nullable=False)
    stall_name = Column(String, nullable=False)


# Database setup
engine = create_engine('sqlite:///canteens.db')
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)