from datetime import datetime
from sqlalchemy import create_engine, Column, Integer, String, Text, DateTime,Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    username = Column(String(50), unique=True)
    password = Column(String(128))  # 实际生产环境应存储哈希值
    created_at = Column(DateTime, default=datetime.now)

class OperationLog(Base):
    __tablename__ = 'operation_logs'
    id = Column(Integer, primary_key=True)
    task_id = Column(String(64), index=True)
    user_id = Column(Integer)
    operation_type = Column(String(50))
    details = Column(Text)
    created_at = Column(DateTime, default=datetime.now)

class AuditLog(Base):
    __tablename__ = 'audit_logs'
    id = Column(Integer, primary_key=True)
    task_id = Column(String(64), index=True)
    user_id = Column(Integer)
    ip_address = Column(String(45))
    action_type = Column(String(50))
    status = Column(String(20))
    created_at = Column(DateTime, default=datetime.now)

# models.py
class Order(Base):  # 修改继承自 Base 而不是 db.Model
    __tablename__ = 'orders'
    id = Column(Integer, primary_key=True)
    name = Column(String(100))
    total_progress = Column(Float, default=0.0)  # 总进度（0-100）
    stages = relationship("Stage", backref="order")

class Stage(Base):  # 修改继承自 Base
    __tablename__ = 'stages' 
    id = Column(Integer, primary_key=True)
    order_id = Column(Integer, ForeignKey("orders.id"))  # 使用表名 orders.id
    name = Column(String(50))
    weight = Column(Float)  # 固定权重（如30%）
    tasks = relationship("Task", backref="stage")

class Task(Base):  # 修改继承自 Base
    __tablename__ = 'tasks'
    id = Column(Integer, primary_key=True)
    stage_id = Column(Integer, ForeignKey("stages.id"))  # 使用表名 stages.id
    name = Column(String(100))
    weight = Column(Float)  # 动态权重（如60%）
    status = Column(String(20))  # 来自外部系统（pending/done）
    external_id = Column(String(50))  # Jira/SMART系统ID