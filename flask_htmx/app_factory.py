from flask import Flask, app
from celery import Celery
import redis
from flask_sqlalchemy import SQLAlchemy
from celery.signals import worker_process_init

from flask_htmx.config import CeleryConfig, Config
from flask_htmx.models import Base

celery_config = CeleryConfig()
config = Config()
db = SQLAlchemy(model_class=Base,engine_options={'url':config.SQLALCHEMY_DATABASE_URI})

# celery -A flask_htmx.app_factory.celery worker -pool=solo -l info

# 在模块顶部初始化Celery实例
# 在创建Celery实例时添加配置
from celery import Celery, Task


task_matcher = ([
       ('flask_htmx.tasks.login_tasks.*', {'queue': 'user_tasks'}),
],
)


def make_celery(app):

    celery = Celery(app.import_name
                    , broker=celery_config.CELERY_BROKER_URL
                    , backend=celery_config.result_backend
                    ,include=['flask_htmx.tasks'])
    celery.conf.update(app.config)
    celery.conf.task_routes = task_matcher
    class ContextTask(Task):
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return self.run(*args, **kwargs)
    celery.Task = ContextTask
    return celery



def create_app():
    app = Flask(__name__, static_folder='static', template_folder='templates')
    app.config.from_object(config)

    
    # # 配置Celery
    # celery.conf.update(app.config)
    # celery.main = app.name  # 关键设置
    
    # 初始化数据库
    db.init_app(app)
    with app.app_context():
        db.create_all()
    
    # 初始化Redis连接
    app.redis_conn = redis.StrictRedis(host='localhost', port=6379, db=2)
    
    # 注册蓝图
    from flask_htmx.routes.form_routes import form_bp
    from flask_htmx.routes.task_routes import task_bp  # 新增任务蓝图
    app.register_blueprint(form_bp)
    app.register_blueprint(task_bp)
    


    # # 不再需要单独的celery初始化
    celery_app = make_celery(app)

    return app

app = create_app()
task_app = make_celery(app)


# @worker_process_init.connect
# def init_worker(**kwargs):
#     # 在worker进程中重新创建app上下文
#     local_app = create_app()
#     with local_app.app_context():
#         db.create_all()