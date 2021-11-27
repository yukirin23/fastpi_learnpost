from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from . import models
from .database import engine
from .routers import post, user, auth, vote
from .config import settings


import sentry_sdk
sentry_sdk.init(
    "https://0102fb0c45b341598e07e7b51d57882d@o1072831.ingest.sentry.io/6072188",

    # Set traces_sample_rate to 1.0 to capture 100%
    # of transactions for performance monitoring.
    # We recommend adjusting this value in production.
    traces_sample_rate=1.0
)


# generate table by sqlalchemy after first loading
# models.Base.metadata.create_all(bind=engine)

app = FastAPI()


# access website CORS (Cross-Origin Resource Sharing) security
origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(vote.router)


@app.get("/")
def root():
    return {"message": "Hello World pushing out to ubuntu"}
