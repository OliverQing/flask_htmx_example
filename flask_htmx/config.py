# class Config:
#     SECRET_KEY = "your_secret_key"
#     DEBUG = True
import sys
from urllib.parse import quote_plus
password = "DGdp@2021"
encoded_password = quote_plus(password)
db_url = f'mysql+pymysql://root:{encoded_password}@127.0.0.1:3306/scheduler_db'

class CeleryConfig:
    result_backend = 'redis://127.0.0.1:6379/3'
    CELERY_BROKER_URL = 'redis://127.0.0.1:6379/1'

class Config:
    # 添加严格解析配置
    JSON_SORT_KEYS = False
    JSONIFY_MIMETYPE = 'application/json; charset=utf-8'
    SQLALCHEMY_DATABASE_URI = db_url
    SECRET_KEY = 'pokemon123'
    # 添加以下配置项解决中文问题
    JSON_AS_ASCII = False  # 禁用ASCII编码
    RESTX_JSON = {'ensure_ascii': False}  # 保持非ASCII字符原样
    SQLALCHEMY_BINDS = {
    'default': SQLALCHEMY_DATABASE_URI,  # 主数据库
    }