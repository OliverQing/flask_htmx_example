from flask import Blueprint, render_template, request
from validators import validator
from markupsafe import Markup 

form_bp = Blueprint('form', __name__, template_folder='../templates')

@form_bp.route("/form/validate/<field_name>", methods=["POST"])
def validate_field(field_name):
    value = request.form.get(field_name, "")
    result = validator.validate(field_name, value)
    
    if result["valid"]:
        return Markup("<span class='text-success' data-valid='true'>✓ 有效</span>")
    else:
        return Markup(f"<span class='text-danger' data-valid='false'>{result['message']}</span>")

@form_bp.route("/")
def form():
    return render_template('form_page.html')

@form_bp.route("/submit", methods=["POST"])
def handle_submit():
    return render_template("success.html")
