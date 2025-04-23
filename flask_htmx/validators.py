import time


class Validator:
    def __init__(self):
        self.validators = {}

    def register(self):
        def decorator(func):
            self.validators[func.__name__] = func  
            return func
        return decorator

    def validate(self, field_name, value):
        if field_name not in self.validators:
            return {"valid": False, "message": "Validation rule not found"}
        validator_func = self.validators[field_name]
        return validator_func(value)

validator = Validator()

# 验证器注册
# 示例验证规则注册
@validator.register()
def validate_username(value):
    if len(value) < 4:
        return {"valid": False, "message": "Username must be at least 4 characters"}
    return {"valid": True, "message": ""}

@validator.register()
def validate_email(value):
    if "@" not in value:
        return {"valid": False, "message": "Invalid email format"}
    return {"valid": True}

@validator.register()
def validate_password(value):
    if len(value) < 8:
        return {"valid": False, "message": "Password must be at least 8 characters"}
    return {"valid": True}

