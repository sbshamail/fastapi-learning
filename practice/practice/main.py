from fastapi import FastAPI,Depends
from sqlmodel import SQLModel, Field, create_engine
from contextlib import asynccontextmanager

from practice.lib.db import engine,get_session
from practice.mvc.router import userRoute
from practice.mvc.models.userModel import User, UserCreate
from sqlmodel import Session


@asynccontextmanager
async def lifespan(app: FastAPI):
    SQLModel.metadata.create_all(engine)  # 👈 create tables on startup
    yield  # 👈 run the app
    # cleanup logic (if needed) goes here

app = FastAPI(lifespan=lifespan)

@app.get("/")
def root():
    return {"message": "Welcome to FastAPI with uv and SQLModel"}


app.include_router(userRoute.router)

# @app.post("/users", response_model=User)
# def create_user(user_create: UserCreate, session: Session = Depends(get_session)):
#     user = User(**user_create.dict())
#     session.add(user)
#     session.commit()
#     session.refresh(user)
#     return user