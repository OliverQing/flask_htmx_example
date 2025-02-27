class Validator:
    def __init__(self):
        self.validators = {}
        
    def register(self, field_name):
        def decorator(func):
            self.validators[field_name] = func
            return func
        return decorator
    
    def validate_route(self, field_name):
        def wrapper():
            if field_name not in self.validators:
                return "Invalid field", 400
                
            # 从请求中获取表单值
            value = request.args.get('value') or request.form.get('value')
            return self.validators[field_name](value)
            
        return wrapper

# 初始化验证器实例
validator = Validator()
