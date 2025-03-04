from abc import ABC, abstractmethod
from typing import List
from flask import Flask, abort, session, url_for,request
import hashlib
import time
import html

from flask_htmx.validators import validate_email, validate_username
from flask import g

class ValidationError(Exception):
    pass

class FormField(ABC):
    def __init__(self, name, label, validators=callable):
        # 添加输入过滤
        self.name = html.escape(name)
        self.label = html.escape(label)
        self.validators = validators or None
        if validators:
            self.validator_url = f'/form/validate/{validators.__name__}'

    @abstractmethod
    def render(self):
        pass

class TextField(FormField):
    def render(self):
        # 添加CSRF令牌和输出转义
        csrf_token = url_for('get_csrf')
        return f"""
        <div class="mb-3">
            <input type="hidden" name="_csrf" hx-headers='{{"X-CSRFToken": "{csrf_token}"}}'>
            <label class="form-label">{self.label}</label>
            <div class="input-group">
                <input type="text" 
                       class="form-control" 
                       name="{self.name}"
                       hx-post="{html.escape(','.join(self.validator_url))}"
                       hx-headers='{{"X-CSRFToken": "{csrf_token}"}}'
                       hx-trigger="input changed delay:500ms, blur"
                       hx-target="#{self.name}-error">
                <i class="htmx-indicator bx bx-loader-circle"></i>
            </div>
            <span id="{self.name}-error" class="invalid-feedback"></span>
        </div>
        """

class Form(ABC):
    def __init__(self,route_name, fields:List[FormField]):
        self.fields = fields
        self.is_valid = False
        self.route_name = route_name
    
    def render(self):
        # 添加表单防篡改签名
        form_hash = hashlib.sha256(str(time.time()).encode()).hexdigest()
        session['form_hash'] = form_hash
        
        form_html = f'<form hx-post="/submit" hx-swap="none" data-form-hash="{form_hash}">'
        for field in self.fields:
            form_html += field.render()
        form_html += """
        <button type="submit" class="btn btn-primary" 
                hx-indicator=".htmx-indicator" disabled>提交</button>
        </form>
        """
        return form_html
    
    def _validate_form_security(self):
        """安全验证的公共方法"""
        if session.get('form_hash') != request.form.get('form_hash'):
            abort(403)
    
    @abstractmethod
    def handle_submit(self, form_data):
        """子类必须实现的抽象方法"""
        pass
    
    def register_routes(self, app):
        '''注册该表单的路由，并将表单返回到前端'''
        # 添加前置钩子
        @app.before_request
        def verify_form_security():
            if request.method == "POST" and request.endpoint == f'submit_form_{self.route_name}':
                if session.get('form_hash') != request.form.get('form_hash'):
                    abort(403)
                # 将验证结果存入全局对象
                g.form_verified = True

        # 注册路由时添加唯一端点名
        @app.route(f'/{self.route_name}/submit', methods=['POST'], endpoint=f'submit_form_{self.route_name}')
        def submit_form():
            if not getattr(g, 'form_verified', False):
                abort(403)
            form_data = request.form
            self._validate_form_security()  
            return self.handle_submit(form_data)

        @app.route(f'/{self.route_name}', methods=['GET'], endpoint=f'render_form_{self.route_name}')
        def render_form():
            return self.render()
        
        return app


