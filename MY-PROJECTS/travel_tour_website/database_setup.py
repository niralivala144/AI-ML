from sqlalchemy import create_engine, Column, Integer, String, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()

# Travel destinations table
class Destination(Base):
    __tablename__ = 'destinations'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    country = Column(String)
    category = Column(String)  # e.g., adventure, beach, cuplture
    cost = Column(Float)
    rating = Column(Float)

# Create SQLite database
engine = create_engine('sqlite:///travel.db')
Base.metadata.create_all(engine)

print("✅ Database created successfully!")