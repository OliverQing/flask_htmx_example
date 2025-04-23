from flask import Blueprint, render_template, request
from flask_htmx.validators import validator
from markupsafe import Markup 

form_bp = Blueprint('form', __name__, url_prefix='/form')

@form_bp.route("/validate/<func_name>", methods=["POST"])
def validate_field(func_name):
    k,v = list(request.form.items())[0]
    validation_result = validator.validate(func_name, v)
    if validation_result["valid"]:
        # 验证通过，返回成功提示
        # response_html = f'<div class="text-green-500">√ Valid</div>'
        response_html = f'<div id="{k}-error" aria-valid="true"><div class="text-green-500">√ Valid</div></div>'

    else:
        # 验证失败，返回错误提示
        response_html = f'<div id="{k}-error" aria-valid="false"><div class="text-red-500">{validation_result["message"]}</div></div>'

    return response_html

@form_bp.route("/")
def form():
    return render_template('base.html')

