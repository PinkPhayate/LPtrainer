from sqlalchemy import create_engine
from database_setup import Base, Restaurant, MenuItem
engine = create_engine('sqlite:///restaurantMenu.db')
Base.metadata.bind=engine
