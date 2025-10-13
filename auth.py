
import jwt
from datetime import datetime, timedelta
from typing import Optional, Dict, Any
from config import JWT_SECRET


class AuthManager:
    
    
    @staticmethod
    def create_token(user_id: str, email: str, is_admin: bool = False) -> str:
        
        payload = {
            "user_id": user_id,
            "email": email,
            "is_admin": is_admin,
            "exp": datetime.utcnow() + timedelta(hours=24)
        }
        return jwt.encode(payload, JWT_SECRET, algorithm="HS256")
    
    @staticmethod
    def verify_token(token: str) -> Optional[Dict[str, Any]]:
        
        try:
            payload = jwt.decode(token, JWT_SECRET, algorithms=["HS256"])
            return payload
        except jwt.ExpiredSignatureError:
            print("Token expirado")
            return None
        except jwt.InvalidTokenError:
            print("Token inválido")
            return None
    
    @staticmethod
    def is_admin(token: str) -> bool:
        
        payload = AuthManager.verify_token(token)
        return payload.get("is_admin", False) if payload else False


class SessionManager:
    
    
    def __init__(self):
        self.token: Optional[str] = None
        self.user_data: Optional[Dict[str, Any]] = None
        self.is_admin: bool = False
    
    def login(self, user_data: Dict[str, Any]):
        
        
        self.token = AuthManager.create_token(
            user_id=str(user_data.get("id")),
            email=user_data.get("email"),
            is_admin=user_data.get("is_admin", False)
        )
        self.user_data = user_data
        self.is_admin = user_data.get("is_admin", False)
    
    def logout(self):
        
        self.token = None
        self.user_data = None
        self.is_admin = False
    
    def is_authenticated(self) -> bool:
        
        return self.token is not None
    
    def get_user_email(self) -> str:
        
        if self.user_data:
            return self.user_data.get("email", "")
        return ""
    
    def get_user_id(self) -> str:
        
        if self.user_data:
            return self.user_data.get("id", "")
        return ""



session = SessionManager()

