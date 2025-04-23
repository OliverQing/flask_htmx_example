from celery import shared_task
from flask_htmx.app_factory import task_app

from flask_htmx.routes.task_handlers import TaskProgress
from ..models import User, OperationLog, AuditLog
from sqlalchemy.orm import scoped_session, sessionmaker
from flask_htmx.app_factory import db
from celery import shared_task




# @task_app.task(bind=True, autoretry_for=(Exception,), max_retries=3)
# def validate_login(self, form_data, task_id):
#     tracker = TaskProgress(task_id)
    
#     # 更新进度
#     tracker.update('login_validation', 20, {'status': 'started'})
    
#     # 固定账号验证
#     if form_data.get('username') == 'admin' and form_data.get('password') == '123':
#         user = User.query.filter_by(username='admin').first()
#         tracker.update('login_validation', 30, {'user_id': user.id})
#         return user.id
#     else:
#         tracker.update('error', 0, {'error': 'Invalid credentials'})
#         raise ValueError("Authentication failed")

@task_app.task(bind=True)
def write_db_log(self, user_id, task_id):
    tracker = TaskProgress(task_id)
    session = db.session
    
    try:
        tracker.update('db_logging', 15)
        log = OperationLog(
            task_id=task_id,
            user_id=user_id,
            operation_type='login',
            details='用户登录操作'
        )
        session.add(log)
        session.commit()
        tracker.update('db_logging', 15)
    finally:
        session.remove()

@task_app.task(bind=True)
def audit_log(self, prev_result, task_id):
    tracker = TaskProgress(task_id)
    session = db.session    
    try:
        tracker.update('audit_logging', 0)
        # 模拟调用外部审计系统
        audit_record = AuditLog(
            task_id=task_id,
            user_id=prev_result,
            ip_address='127.0.0.1',
            action_type='login',
            status='success'
        )
        session.add(audit_record)
        session.commit()
        
        # 模拟外部API调用
        if not mock_external_audit_api():
            raise Exception("Audit API failed")
        
        tracker.update('Completed', 20)
        
    except Exception as e:
        tracker.update('error', 0, {'error': str(e)})
        raise self.retry(exc=e, countdown=5)
    finally:
        session.remove()

def mock_external_audit_api():
    # 模拟API调用成功率90%
    import random
    return random.random() < 0.9


@task_app.task(bind=True)
def log_errors(self, task_id, failed_task_id):
    # 获取失败任务信息
    failed_task = self.app.AsyncResult(failed_task_id)
    error_msg = str(failed_task.result)
    
    # 更新任务进度为失败状态
    TaskProgress(task_id).update('error', 100, {
        'error': f'Task {failed_task_id} failed: {error_msg}'
    }) 