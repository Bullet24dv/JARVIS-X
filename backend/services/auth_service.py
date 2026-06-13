from datetime import datetime, timedelta
from jose import jwt
from passlib.context import CryptContext
from backend.config import settings
from backend.models.database import db

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class AuthService:
    @staticmethod
    def verify_password(plain: str, hashed: str) -> bool:
        return pwd_context.verify(plain, hashed)
        
    @staticmethod
    def get_password_hash(password: str) -> str:
        return pwd_context.hash(password)
        
    @staticmethod
    async def authenticate_user(username: str, password: str):
        user = await db.users.find_one({"username": username})
        if user and AuthService.verify_password(password, user["password"]):
            return user
        return None
        
    @staticmethod
    def create_access_token(data: dict, expires_delta: timedelta = None):
        to_encode = data.copy()
        expire = datetime.utcnow() + (expires_delta or timedelta(minutes=15))
        to_encode.update({"exp": expire})
        return jwt.encode(to_encode, settings.secret_key, algorithm="HS256")