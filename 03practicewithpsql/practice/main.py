# Import FastAPI framework and dependency injection helper
from fastapi import FastAPI,Depends

# SQLModel is a library combining SQLAlchemy + Pydantic
from sqlmodel import SQLModel, Field, create_engine
# Used for managing async startup/shutdown lifecycles
from contextlib import asynccontextmanager
# Importing database engine and session getter function from your own db lib
# from practice.lib.db import engine,get_session
# Import your route definitions
from practice.mvc.router import userRoute
# Import user model and user creation schema
from practice.mvc.models.userModel import User, UserCreate

# Import SQLModel's sync Session (not async yet)
from sqlmodel import Session


# Define app lifespan — this runs once when the app starts and when it shuts down
@asynccontextmanager
async def lifespan(app: FastAPI):
    yield  # 👈 After this, FastAPI starts handling requests
    # Optionally: add cleanup tasks here (closing connections, etc.)

# Initialize the FastAPI app with the custom lifespan
app = FastAPI(lifespan=lifespan)

# Basic route for testing
@app.get("/")
def root():
    return {"message": "Welcome to FastAPI with uv and SQLModel"}


app.include_router(userRoute.router)

