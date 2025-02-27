from flask import Flask, request, jsonify,render_template
from markupsafe import Markup
import htmx

app = Flask(__name__)
app.secret_key = "your_secret_key"

class Validator:
    def __init__(self):
        self.validators = {}

    def register(self, field_name):
        def decorator(func):
            self.validators[field_name] = func
            return func
        return decorator

    def validate(self, field_name, value):
        if field_name not in self.validators:
            return {"valid": False, "message": "Validation rule not found"}
        
        validator_func = self.validators[field_name]
        return validator_func(value)

# 初始化验证器
validator = Validator()

# 注册验证路由
@app.route("/form/validate/<field_name>", methods=["POST"])
def validate_field(field_name):
    value = request.form.get(field_name, "")
    result = validator.validate(field_name, value)
    
    # HTMX需要的HTML响应
    if result["valid"]:
        return Markup("<span class='text-success'>✓ Valid</span>")
    else:
        return Markup(f"<span class='text-danger'>{result['message']}</span>")

# 示例验证规则注册
@validator.register("username")
def validate_username(value):
    if len(value) < 4:
        return {"valid": False, "message": "Username must be at least 4 characters"}
    return {"valid": True}

@validator.register("email")
def validate_email(value):
    if "@" not in value:
        return {"valid": False, "message": "Invalid email format"}
    return {"valid": True}

@validator.register("password")
def validate_password(value):
    if len(value) < 8:
        return {"valid": False, "message": "Password must be at least 8 characters"}
    return {"valid": True}

# HTML模板示例
@app.route("/")
def form():
    return """
    <script src="https://unpkg.com/htmx.org@1.9.10"></script>

    <form hx-boost="true">
        <div class="form-group">
            <label>Username</label>
            <input type="text" 
                   name="username"
                   hx-post="/form/validate/username"
                    hx-trigger="input changed delay:500ms, keyup[key=='Enter']"
                   hx-target="#username-error">
            <span id="username-error"></span>
        </div>

        <div class="form-group">
            <label>Email</label>
            <input type="email" 
                   name="email"
                   hx-post="/form/validate/email"
                   hx-trigger="blur"
                   hx-target="#email-error">
            <span id="email-error"></span>
        </div>

        <div class="form-group">
            <label>Password</label>
            <input type="password" 
                   name="password"
                   hx-post="/form/validate/password"
                   hx-trigger="blur"
                   hx-target="#password-error">
            <span id="password-error"></span>
        </div>

        <button type="submit">Submit</button>
    </form>
    """

if __name__ == "__main__":
    app.run(debug=True)