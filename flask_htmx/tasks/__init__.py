from .login_tasks import *
from .other_task import *

# 自动发现所有任务模块（新增文件时需在此添加导入）
__all__ = ['login_tasks', 'other_task']