from cryptography.fernet import Fernet
from passlib.context import CryptContext
from backend.config import settings

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def encrypt(data: str) -> str:
    f = Fernet(settings.encryption_key.encode())
    return f.encrypt(data.encode()).decode()

def decrypt(encrypted: str) -> str:
    f = Fernet(settings.encryption_key.encode())
    return f.decrypt(encrypted.encode()).decode()

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain: str, hashed: str) -> bool:
    return pwd_context.verify(plain, hashed)