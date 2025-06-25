from fastapi import Depends
from typing import Annotated, Any, Dict
from practice.lib.db import get_session
from sqlmodel import Session


db_dependency = Annotated[Session, Depends(get_session)]