from abc import ABC, abstractmethod
from typing import Callable, List
from flask import Flask, abort, session, url_for,request
import hashlib
import time
import html

from flask_htmx.validators import validate_email, validate_username
from flask import g

class ValidationError(Exception):
    pass

class FormField(ABC):
    def __init__(self, name, label, validators=None):
        # 添加输入过滤
        self.name = html.escape(name)
        self.label = html.escape(label)
        self.validators = validators
        print(validators)
        if validators:
            self.validator_url = f'/form/validate/{validators.__name__}'
            self.validate_block = f'''hx-post="{html.escape(self.validator_url)}" hx-params="{self.name}"  '''
        else:
            self.validator_url = None
            self.validate_block = ''
    @abstractmethod
    def render(self):
        pass

class TextField(FormField):
    def render(self):
        csrf_token = url_for('get_csrf')
        required_attr = 'required aria-required="true"' if self.validators else ''
        aria_invalid = 'true' if self.validators else 'false'
        
        return f"""
        <div class="mb-3">
            <input type="hidden" name="_csrf" hx-headers='{{"X-CSRFToken": "{csrf_token}"}}'>
            <label class="form-label">{self.label}</label>
            <div class="input-group">
                <input type="text" 
                       class="form-control" 
                       name="{self.name}"
                       {required_attr}
                       {self.validate_block}
                       hx-headers='{{"X-CSRFToken": "{csrf_token}"}}'
                       hx-trigger="keyup changed delay:500ms"
                       hx-target="#{self.name}-error"
                       hx-swap="outterHTML"
                       > 
                <i class="htmx-indicator bx bx-loader-circle"></i>
            </div>
            <div id="{self.name}-error" aria-invalid="{aria_invalid} class=""></div>
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

        # 引入 unpkg 的 htmx 包
        htmx_script = '<script src="https://unpkg.com/htmx.org@1.9.9"></script>'
        # 引入 style.css 文件
        css_link = '<link rel="stylesheet" href="static/style.css">'

        form_html = f'<form hx-post="/{self.route_name}/submit" hx-swap="none" data-form-hash="{form_hash}">'
        for field in self.fields:
            form_html += field.render()
        form_html += """
        <button type="submit" id='submit_button' class="btn btn-primary" 
                hx-indicator=".htmx-indicator" disabled>提交</button>
        </form>
        """
        # 将 htmx 脚本和 CSS 链接添加到表单 HTML 前面
        form_html = css_link + htmx_script + form_html
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

        @app.route(f'/{self.route_name}/submit', methods=['POST'], endpoint=f'submit_form_{self.route_name}')
        def submit_form():
            # if not getattr(g, 'form_verified', False):
            #     abort(403)
            form_data = request.form
            # self._validate_form_security()  
            return self.handle_submit(form_data)

        @app.route(f'/{self.route_name}', methods=['GET'], endpoint=f'render_form_{self.route_name}')
        def render_form():
            return self.render()
        
        return app


