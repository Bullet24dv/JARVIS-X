from functools import wraps
from fastapi import HTTPException, Depends
from backend.services.auth_service import AuthService

PERMISSIONS = {
    "admin": ["*"],
    "user": ["chat", "voice", "vision", "computer.read"],
    "guest": ["chat"]
}

def has_permission(user_role: str, action: str) -> bool:
    if user_role == "admin":
        return True
    perms = PERMISSIONS.get(user_role, [])
    return action in perms or "*" in perms

def require_role(role: str):
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            # Obtener usuario del request (simplificado)
            user_role = kwargs.get("user_role", "guest")
            if user_role != role and role != "admin":
                raise HTTPException(status_code=403, detail="Insufficient permissions")
            return await func(*args, **kwargs)
        return wrapper
    return decorator