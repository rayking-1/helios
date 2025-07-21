# helios/database/migrations.py

from sqlalchemy import inspect
from sqlalchemy.exc import SQLAlchemyError
import logging

from helios.database.models import Base
from helios.database.session import engine
from helios.services import logger

def create_tables():
    """
    创建所有数据库表
    
    如果表已存在，则不会重新创建
    """
    try:
        # 获取数据库检查器
        inspector = inspect(engine)
        
        # 获取所有表名
        existing_tables = inspector.get_table_names()
        
        # 获取所有模型的表名
        model_tables = [table.__tablename__ for table in Base.__subclasses__()]
        
        # 记录现有表和要创建的表
        logger.info(f"现有表: {existing_tables}")
        logger.info(f"模型表: {model_tables}")
        
        # 创建表
        Base.metadata.create_all(bind=engine)
        logger.info("数据库表创建完成")
        
        # 记录新创建的表
        new_tables = set(inspector.get_table_names()) - set(existing_tables)
        if new_tables:
            logger.info(f"新创建的表: {new_tables}")
        else:
            logger.info("没有新表被创建")
            
    except SQLAlchemyError as e:
        logger.error(f"创建数据库表时出错: {str(e)}")
        raise

def drop_tables():
    """
    删除所有数据库表
    
    警告: 这将删除所有数据，仅用于开发和测试环境
    """
    try:
        Base.metadata.drop_all(bind=engine)
        logger.info("所有数据库表已删除")
    except SQLAlchemyError as e:
        logger.error(f"删除数据库表时出错: {str(e)}")
        raise

def reset_database():
    """
    重置数据库，删除所有表并重新创建
    
    警告: 这将删除所有数据，仅用于开发和测试环境
    """
    try:
        drop_tables()
        create_tables()
        logger.info("数据库已重置")
    except Exception as e:
        logger.error(f"重置数据库时出错: {str(e)}")
        raise

if __name__ == "__main__":
    # 当直接运行此脚本时，创建所有表
    create_tables() 