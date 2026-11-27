"""
Authentication utilities - JWT and encryption
"""
import logging
import os
import jwt # type: ignore
import hashlib
from datetime import datetime, timedelta
from typing import Optional, Dict, Any, Mapping
from cryptography.fernet import Fernet # type: ignore
import base64

logger = logging.getLogger(__name__)

DEFAULT_DEV_JWT_SECRET = "dev-secret-please-change-in-production"
MIN_PRODUCTION_SECRET_LENGTH = 32
_PRODUCTION_ENV_VALUES = {"production", "prod"}


def _is_production(env: Mapping[str, str]) -> bool:
    if env.get("RAILWAY_ENVIRONMENT"):
        return True
    return any(env.get(key, "").strip().lower() in _PRODUCTION_ENV_VALUES for key in ("ENVIRONMENT", "APP_ENV", "ENV"))


def resolve_jwt_secret(env: Mapping[str, str]) -> str:
    """取得 JWT 簽章金鑰。

    正式環境若沒設定、等於公開的預設值或長度不足，直接拒絕啟動，避免任何人都能偽造 token
    （使用者設定的加密金鑰也由它衍生）。開發環境保留預設值，但會印出警告。
    """
    secret = env.get("JWT_SECRET", "")
    is_default = not secret or secret == DEFAULT_DEV_JWT_SECRET

    if _is_production(env):
        if is_default or len(secret) < MIN_PRODUCTION_SECRET_LENGTH:
            raise RuntimeError(
                f"正式環境必須設定至少 {MIN_PRODUCTION_SECRET_LENGTH} 字元、且不同於預設值的 JWT_SECRET"
            )
        return secret

    if is_default:
        logger.warning("JWT_SECRET 未設定，使用公開的開發用預設值；請勿用於正式環境")
        return DEFAULT_DEV_JWT_SECRET
    return secret


# JWT Configuration
JWT_SECRET = resolve_jwt_secret(os.environ)
JWT_ALGORITHM = "HS256"
JWT_EXPIRATION_HOURS = 24 * 7  # 7 days

# Encryption key derived from JWT_SECRET (for settings encryption)
def _get_fernet_key() -> bytes:
    """Generate a Fernet-compatible key from JWT_SECRET"""
    # Use SHA256 to get a consistent 32-byte key, then base64 encode
    key_hash = hashlib.sha256(JWT_SECRET.encode()).digest()
    return base64.urlsafe_b64encode(key_hash)

_fernet = Fernet(_get_fernet_key())


def create_access_token(user_data: Dict[str, Any]) -> str:
    """
    Create a JWT access token for a user
    
    Args:
        user_data: Dict containing user info (id, email, name, avatar_url)
    
    Returns:
        JWT token string
    """
    payload = {
        "sub": str(user_data["id"]),  # Subject (user ID)
        "email": user_data["email"],
        "name": user_data.get("name"),
        "avatar_url": user_data.get("avatar_url"),
        "exp": datetime.utcnow() + timedelta(hours=JWT_EXPIRATION_HOURS),
        "iat": datetime.utcnow(),
    }
    
    return jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)


def verify_access_token(token: str) -> Optional[Dict[str, Any]]:
    """
    Verify and decode a JWT access token
    
    Args:
        token: JWT token string
    
    Returns:
        Decoded payload if valid, None if invalid/expired
    """
    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        return payload
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None


def encrypt_settings(settings_json: str) -> str:
    """
    Encrypt user settings JSON string
    
    Args:
        settings_json: JSON string of user settings
    
    Returns:
        Encrypted string (base64 encoded)
    """
    encrypted = _fernet.encrypt(settings_json.encode())
    return encrypted.decode()


def decrypt_settings(encrypted_settings: str) -> str:
    """
    Decrypt user settings
    
    Args:
        encrypted_settings: Encrypted settings string
    
    Returns:
        Decrypted JSON string
    """
    decrypted = _fernet.decrypt(encrypted_settings.encode())
    return decrypted.decode()


def get_user_id_from_token(token: str) -> Optional[str]:
    """Extract user ID from a valid token"""
    payload = verify_access_token(token)
    if payload:
        return payload.get("sub")
    return None
