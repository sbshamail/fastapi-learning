# Import FastAPI framework and dependency injection helper
from fastapi import FastAPI,Depends
# Used for managing async startup/shutdown lifecycles
from contextlib import asynccontextmanager
# Import your route definitions
from practice.mvc.router import userRoute,productRoute

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
app.include_router(productRoute.router)

