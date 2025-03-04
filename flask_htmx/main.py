import sys
import os

from flask import jsonify, session
# 添加项目根目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app_factory import create_app
from routes.routes import LoginForm

app = create_app()

# 在Form类之后添加CSRF路由
@app.route('/get_csrf', methods=['GET'])
def get_csrf():
    # 生成32位随机CSRF令牌
    csrf_token = os.urandom(16).hex()
    session['_csrf_token'] = csrf_token
    return jsonify({
        'token': csrf_token,
        'expires_in': 3600  # 1小时有效期
    })
    
    
if __name__ == "__main__":
    LoginForm().register_routes(app)
    app.run()
