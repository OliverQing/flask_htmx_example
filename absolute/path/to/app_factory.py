def create_app():
    app = Flask(__name__)
    app.secret_key = os.urandom(24)  # 必须设置密钥
    
    # 注册CSRF路由
    from .forms import get_csrf
    app.add_url_rule('/get_csrf', view_func=get_csrf)
    
    return app
