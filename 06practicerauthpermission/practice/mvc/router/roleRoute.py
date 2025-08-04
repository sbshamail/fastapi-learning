from datetime import datetime, timezone
from fastapi import APIRouter, Depends
from sqlmodel import select

from practice.lib import GetSession, api_response
from practice.mvc.core.security import require_admin, require_signin
from practice.mvc.models.roleModel import Role, RoleCreate, RoleUpdate, RoleRead


router = APIRouter(prefix="/role", tags=["role"])

requireSignin = Depends(require_signin)
requireAdmin = Depends(require_admin)


@router.post("/create")
def create_role(request: RoleCreate, session: GetSession, user=requireAdmin):
    role = Role(**request.model_dump())
    session.add(role)
    session.commit()
    session.refresh(role)
    return api_response(200, "Role created", role)


@router.put("/{id}")
def update_role(id: int, request: RoleUpdate, session: GetSession, user=requireAdmin):
    role = session.get(Role, id)
    if not role:
        api_response(404, "Role not found")

    role_data = request.model_dump(exclude_unset=True)
    for key, value in role_data.items():
        setattr(role, key, value)
    role.updated_at = datetime.now(timezone.utc)
    session.add(role)
    session.commit()
    session.refresh(role)

    return api_response(200, "Role updated", role)


@router.get("/list")
def list_roles(session: GetSession, user=requireAdmin):
    roles = session.exec(select(Role)).all()
    return api_response(200, "Role list", roles)


@router.get("/{id}")
def read_role(id: int, session: GetSession, user=requireAdmin):
    statement = select(Role).where(Role.id == id)
    result = session.exec(statement).first()
    return api_response(200, "Role list", result)


@router.delete("/{id}", response_model=dict)
def delete_role(id: int, session: GetSession, user=requireAdmin):
    role = session.get(Role, id)
    if not role:
        return api_response(404, "Role not found")

    session.delete(role)
    session.commit()
    return api_response(200, f"Role {id} deleted")
