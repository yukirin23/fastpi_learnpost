from fastapi import FastAPI
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from . import models
from .database import engine
from .routers import post, user, auth


# generate table
models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# to make sure connection is running until get connection
while True:
    # check connection to database postgres
    try:
        conn = psycopg2.connect(host='localhost', database='fastapiDB',
                                user='postgres', password='khalida23', cursor_factory=RealDictCursor)
        cursor = conn.cursor()
        print("Database Connection was successfull")
        break
    except Exception as error:
        print("Connection to database failed")
        print("Error: ", error)
        # break for 2 second before continue check connection
        time.sleep(2)


app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
