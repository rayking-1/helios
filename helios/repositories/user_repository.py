# helios/repositories/user_repository.py

from sqlalchemy.orm import Session
from helios.database.models import User
from helios.repositories.base import BaseRepository

class UserRepository(BaseRepository[User]):
    """
    User实体的仓储类，提供用户相关的数据访问方法
    """
    def __init__(self, db: Session):
        super().__init__(User, db)
    
    def find_by_email(self, email: str):
        """
        通过电子邮件查找用户
        
        参数:
            email: 用户电子邮件
            
        返回:
            找到的用户对象，如果不存在则返回None
        """
        return self.find_one(email=email)
    
    def find_by_username(self, username: str):
        """
        通过用户名查找用户
        
        参数:
            username: 用户名
            
        返回:
            找到的用户对象，如果不存在则返回None
        """
        return self.find_one(username=username) 