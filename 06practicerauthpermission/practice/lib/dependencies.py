from typing import Annotated, Any, Dict

from fastapi import Depends
from sqlmodel import Session

from practice.lib.db import get_session


GetSession = Annotated[Session, Depends(get_session)]
