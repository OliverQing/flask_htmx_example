from flask import Flask


class Config:
    SECRET_KEY = "your_secret_key"
    DEBUG = True

config = Config()


def create_app():
    app = Flask(__name__)
    app.config.from_object(config)
    
    # 注册蓝图
    from routes.form_routes import form_bp
    app.register_blueprint(form_bp)
    
    return app
