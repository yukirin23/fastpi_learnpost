from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from .config import settings
import time
import psycopg2
from psycopg2.extras import RealDictCursor

# connect database via sqlalchemy
#SQLALCHEMY_DATABASE_URL = 'postgresql://<username>:<password>@<ip-address/hostname>/<database_name>'
SQLALCHEMY_DATABASE_URL = f'postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}'

engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# Dependency


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# to make sure connection is running until get connection
# while True:
    # check connection to database postgres
   # try:
   #     conn = psycopg2.connect(host='localhost', database='fastapiDB',
   #                             user='postgres', password='khalida23', cursor_factory=RealDictCursor)
   #     cursor = conn.cursor()
   #     print("Database Connection was successfull")
   #     break
   # except Exception as error:
   #     print("Connection to database failed")
   #     print("Error: ", error)
   #     # break for 2 second before continue check connection
   #     time.sleep(2)
