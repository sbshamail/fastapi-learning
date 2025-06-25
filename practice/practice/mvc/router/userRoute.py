from fastapi import APIRouter, Depends,HTTPException
from fastapi.responses import JSONResponse
from sqlmodel import Session,select
from practice.mvc.models.userModel import User, UserCreate
from practice.lib.db import get_session
from practice.lib.response import api_response
router = APIRouter(prefix="/user", tags=["user"])

@router.post("/create", response_model=User)  # ✅ Added "@"
def create_user(request: UserCreate, session: Session = Depends(get_session)):
    user = User(**request.model_dump())
    session.add(user)
    session.commit()
    session.refresh(user)
    return api_response(200, "User created", user)

# ✅ READ ALL
@router.get("/all")  # no response_model
def get_users(session: Session = Depends(get_session)):
    users = session.exec(select(User)).all()
    if not users or len(users) == 0:
      return api_response(404, "User not found")
   
    return api_response(200, "Users fetched", users, len(users))  


# ✅ READ ONE
@router.get("/{user_id}", response_model=User)
def get_user(user_id: int, session: Session = Depends(get_session)):
    user = session.get(User, user_id)
    if not user:
        # raise HTTPException(status_code=404, detail="User not found")
        return api_response(404, "User not found")
    return api_response(200, "User Found", user)


# ✅ DELETE
@router.delete("/{user_id}", response_model=dict)
def delete_user(user_id: int, session: Session = Depends(get_session)):
    user = session.get(User, user_id)
    if not user:
        return api_response(404, "User not found")
    
    session.delete(user)
    session.commit()
    return api_response(404, f"User {user_id} deleted")