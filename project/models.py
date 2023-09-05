from flask_login import UserMixin
from . import db
from sqlalchemy.orm import Mapped, mapped_column, relationship, DeclarativeBase, sessionmaker
from sqlalchemy import String, DateTime, ForeignKey, Integer

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True) # primary key
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    name = db.Column(db.String(100))
    lname = db.Column(db.String(100))

from sqlalchemy import create_engine
import pandas as pd

db_name = 'instance/db.sqlite'
engine = create_engine(f'sqlite:///{db_name}')

Airlines_file = 'project/IATA Codes/Airlines.csv'  
df_airlines_file = pd.read_csv(Airlines_file)

AirportCity_file = 'project/IATA Codes/AirportCity.csv'  
df_AirportCity_file = pd.read_csv(AirportCity_file)

Cities_file = 'project/IATA Codes/Cities.csv'  
df_Cities_file = pd.read_csv(Cities_file)


# Airlines = 'airlines'  
# Cities = 'airportCity' 
# df_airlines_file.to_sql(Airlines, engine, index=False, if_exists='replace')  
# df_AirportCity_file.to_sql(Cities, engine, index=False, if_exists='replace')  

class Base(DeclarativeBase):
    pass

class Airlines(Base):
    __tablename__ = 'airlines'
    id: Mapped[int] = mapped_column(primary_key=True)
    airline: Mapped[str] = mapped_column(String(20), unique=True,nullable=False)
    codes: Mapped[str] = mapped_column(String(20), unique=True,nullable=False)
   
    def __str__(self):
        return self.airline

class Cities(Base):
    __tablename__ = 'cities'
    id: Mapped[int] = mapped_column(primary_key=True)
    codes: Mapped[str] = mapped_column(String(20), unique=True,nullable=False)
    city: Mapped[str] = mapped_column(String(20), unique=False,nullable=False)
    country: Mapped[str] = mapped_column(String(20), unique=False,nullable=False)

    # def __str__(self):
    #     return self.city

    def __str__(self):
        return f"<Cities codes={self.codes}, city = {self.city}"

class Airports(Base):
    __tablename__ = 'airports'
    id: Mapped[int] = mapped_column(primary_key=True)
    codes: Mapped[str] = mapped_column(String(20), unique=True,nullable=False)
    airport: Mapped[str] = mapped_column(String(20), unique=False,nullable=False)

    def __str__(self):
        return self.airport
    

Session = sessionmaker(bind=engine)
session = Session()

# Create tables
Base.metadata.create_all(engine)

# # Insert data into the Airlines table
# for index, row in df_airlines_file.iterrows():
#     airline = Airlines(airline=row['airline'], codes=row['codes'])
#     session.add(airline)

# # Insert data into the Cities table
# for index, row in df_Cities_file.iterrows():
#     city = Cities(codes=row['Codes'], city=row['City'], country=row['Country'])
#     session.add(city)

# # Insert data into the Airports table
# for index, row in df_AirportCity_file.iterrows():
#     airport = Airports(airport=row['airport'], codes=row['codes'])
#     session.add(airport)

# Commit the changes and close the session
session.commit()
session.close()