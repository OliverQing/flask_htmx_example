from celery import chain
import secrets
from flask import Blueprint, jsonify, url_for
from flask_htmx.tasks.login_tasks import log_errors,write_db_log,audit_log
from  forms import TextField, Form
from validators import validate_username
from .task_handlers import TaskProgress  # 新增导入

class LoginError(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)


def validate_login(username, password):
    if username == 'admin' and password == '123':
        # user = User.query.filter_by(username='admin').first()
        return 12345
    raise LoginError("Invalid credentials")
 


class LoginForm(Form):
    def __init__(self):
        
        
        super().__init__(
        'login',
        [
            TextField('username', 'Username', validators=validate_username),
            TextField('password', 'Password')
        ],
        )
    
    def handle_submit(self, form_data):
        # 同步处理核心登录验证
        login_flag = False
        user_id = form_data.get('username')
        task_id = secrets.token_urlsafe(24)
        tracker = TaskProgress(task_id)
        tracker.update('login_validation', 20, {'status': 'started'})
        try:
            user_id = validate_login(form_data.get('username'), form_data.get('password'))
            login_flag = True
        except LoginError as e:
            login_flag = False
             
        # 生成安全任务ID（保持原有逻辑）

        tracker.update('login_validation', 30, {'user_id': user_id})

        # 构建异步日志任务链
        log_chain = chain(
            write_db_log.si(user_id, task_id),
            audit_log.si(user_id, task_id)
        )
        
        # 异步执行日志任务
        log_chain.apply_async(
            task_id=task_id,
            link_error=log_errors.s(task_id)
        )

        if not login_flag:
            return jsonify({
                'status':'failed',
                'task_id': task_id,
               'status_url': url_for('task.get_status', task_id=task_id)
            })
        else:
            return jsonify({
                'user_id': user_id,
                'status': 'success',
                'task_id': task_id,
                'status_url': url_for('task.get_status', task_id=task_id)
            })    
