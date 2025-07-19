# helios/repositories/base.py

from typing import TypeVar, Generic, Type, List, Optional, Any, Dict, Union
from sqlalchemy.orm import Session
from sqlalchemy import select, update, delete

ModelType = TypeVar("ModelType")

class BaseRepository(Generic[ModelType]):
    """
    提供通用CRUD操作的基础仓储类
    
    泛型参数:
        ModelType: SQLAlchemy模型类型
    """
    def __init__(self, model: Type[ModelType], db: Session):
        """
        初始化仓储
        
        参数:
            model: SQLAlchemy模型类
            db: SQLAlchemy会话对象
        """
        self.model = model
        self.db = db

    def get(self, item_id: Any) -> Optional[ModelType]:
        """
        通过ID获取单个实体
        
        参数:
            item_id: 实体ID
            
        返回:
            找到的实体对象，如果不存在则返回None
        """
        return self.db.query(self.model).get(item_id)
    
    def get_all(self) -> List[ModelType]:
        """
        获取所有实体
        
        返回:
            实体对象列表
        """
        return self.db.query(self.model).all()
    
    def find(self, **kwargs) -> List[ModelType]:
        """
        根据条件查找实体
        
        参数:
            **kwargs: 过滤条件，字段名和值的键值对
            
        返回:
            符合条件的实体对象列表
        """
        return self.db.query(self.model).filter_by(**kwargs).all()
    
    def find_one(self, **kwargs) -> Optional[ModelType]:
        """
        根据条件查找单个实体
        
        参数:
            **kwargs: 过滤条件，字段名和值的键值对
            
        返回:
            符合条件的第一个实体对象，如果不存在则返回None
        """
        return self.db.query(self.model).filter_by(**kwargs).first()

    def create(self, **kwargs) -> ModelType:
        """
        创建新实体
        
        参数:
            **kwargs: 实体属性的键值对
            
        返回:
            创建的实体对象
        """
        item = self.model(**kwargs)
        self.db.add(item)
        self.db.commit()
        self.db.refresh(item)
        return item
    
    def update(self, item_id: Any, **kwargs) -> Optional[ModelType]:
        """
        更新实体
        
        参数:
            item_id: 实体ID
            **kwargs: 要更新的属性的键值对
            
        返回:
            更新后的实体对象，如果实体不存在则返回None
        """
        item = self.get(item_id)
        if item:
            for key, value in kwargs.items():
                setattr(item, key, value)
            self.db.commit()
            self.db.refresh(item)
        return item
    
    def delete(self, item_id: Any) -> bool:
        """
        删除实体
        
        参数:
            item_id: 实体ID
            
        返回:
            如果删除成功则返回True，否则返回False
        """
        item = self.get(item_id)
        if item:
            self.db.delete(item)
            self.db.commit()
            return True
        return False
    
    def count(self, **kwargs) -> int:
        """
        计算符合条件的实体数量
        
        参数:
            **kwargs: 过滤条件，字段名和值的键值对
            
        返回:
            符合条件的实体数量
        """
        return self.db.query(self.model).filter_by(**kwargs).count() 