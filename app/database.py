from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from .config import settings
import psycopg2
from psycopg2.extras import RealDictCursor
import time

# SQLALCHEMY_DATABASE_URL = 'postgresql://<username>:<password>@<ip-address/hostname>/<database_name>'

SQLALCHEMY_DATABASE_URL = f'postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}'

engine=create_engine(SQLALCHEMY_DATABASE_URL)#this is responsible for estblashing the connection
SessionLocal=sessionmaker(autocommit=False , autoflush=False, bind=engine )

Base = declarative_base()

def get_db():
    db=SessionLocal()
    try:
        yield db
    finally:
        db.close()



# while True:
#     try:
#         conn= psycopg2.connect(host='localhost' , database='fastapi', user='postgres' , password='Yashasvi284*' , cursor_factory=RealDictCursor) #curosr_factiry will help in accessing the column name as well as the values
#         cursor=conn.cursor()
#         print("database connection was successful")
#         break
#     except Exception as error:
#         print("connection to database failed")
#         print("Error: " , error  )
#         time.sleep(2) #in case of network failure it will keep trying in every two seconds to try to connect to the database
#
