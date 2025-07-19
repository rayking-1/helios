# helios/security/password.py

"""
密码处理模块，提供密码哈希和验证功能
"""

from passlib.context import CryptContext

# 创建密码上下文，使用bcrypt算法
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_password_hash(password: str) -> str:
    """
    对密码进行哈希处理
    
    参数:
        password: 原始密码
        
    返回:
        哈希后的密码
    """
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    验证密码是否正确
    
    参数:
        plain_password: 原始密码
        hashed_password: 哈希后的密码
        
    返回:
        如果密码匹配则返回True，否则返回False
    """
    return pwd_context.verify(plain_password, hashed_password) 