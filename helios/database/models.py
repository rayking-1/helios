# helios/database/models.py

from datetime import datetime
import uuid
from sqlalchemy import Column, String, Integer, ForeignKey, DateTime, JSON, Text
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID

from helios.database.session import Base

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, index=True)
    email = Column(String(100), unique=True, index=True)
    hashed_password = Column(String(100))
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # 关系
    tasks = relationship("Task", back_populates="user")

class Task(Base):
    __tablename__ = "tasks"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    description = Column(String(500), nullable=False)
    status = Column(String(20), default="PENDING")  # PENDING, IN_PROGRESS, COMPLETED, FAILED
    priority = Column(Integer, default=10)
    result = Column(JSON, nullable=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # 关系
    user = relationship("User", back_populates="tasks")
    messages = relationship("ConversationMessage", back_populates="task")

class ConversationMessage(Base):
    __tablename__ = "conversation_messages"
    
    id = Column(Integer, primary_key=True, index=True)
    task_id = Column(UUID(as_uuid=True), ForeignKey("tasks.id"))
    sequence_order = Column(Integer)  # 消息在对话中的顺序
    speaker = Column(String(50))  # 发言者标识，如 "user", "assistant", "system" 等
    message = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # 关系
    task = relationship("Task", back_populates="messages") 