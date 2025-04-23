import json
import redis
from flask import current_app
from flask_htmx.app_factory import app 

class TaskProgress:
    def __init__(self, task_id):
        self.task_id = task_id
        
    def update(self, stage, progress, meta=None):
        # 获取 Redis 管道（用于批量操作）
        pipeline = app.redis_conn.pipeline()
        
        # 更新当前阶段（使用 HSET 存储到 task:{id} 的 hash 中）
        pipeline.hset(f'task:{self.task_id}', 'current_stage', stage)
        
        # 累加进度值（HINCRBYFLOAT 支持浮点数递增）
        pipeline.hincrbyfloat(f'task:{self.task_id}', 'progress', progress)
        
        # 如果有附加元数据（如错误信息等）
        if meta:
            # 将元数据以 JSON 格式存储到 task:{id}:meta 的 hash 中
            pipeline.hset(f'task:{self.task_id}:meta', stage, json.dumps(meta))
        
        # 设置 24 小时过期时间（单位：秒）
        pipeline.expire(f'task:{self.task_id}', 86400)
        
        # 批量执行所有 Redis 命令（原子性操作）
        pipeline.execute()
