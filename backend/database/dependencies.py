# helios/database/dependencies.py

from typing import Generator
from sqlalchemy.orm import Session
from fastapi import Depends

from helios.database.session import get_db
from helios.repositories.user_repository import UserRepository
from helios.repositories.task_repository import TaskRepository
from helios.repositories.conversation_repository import ConversationRepository

def get_user_repository(db: Session = Depends(get_db)) -> UserRepository:
    """
    获取User实体的仓储实例
    
    参数:
        db: SQLAlchemy会话对象
        
    返回:
        UserRepository实例
    """
    return UserRepository(db)

def get_task_repository(db: Session = Depends(get_db)) -> TaskRepository:
    """
    获取Task实体的仓储实例
    
    参数:
        db: SQLAlchemy会话对象
        
    返回:
        TaskRepository实例
    """
    return TaskRepository(db)

def get_conversation_repository(db: Session = Depends(get_db)) -> ConversationRepository:
    """
    获取ConversationMessage实体的仓储实例
    
    参数:
        db: SQLAlchemy会话对象
        
    返回:
        ConversationRepository实例
    """
    return ConversationRepository(db) 