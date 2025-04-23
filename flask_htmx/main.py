import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from flask import jsonify, render_template, request, session

from flask_htmx.tasks.other_task import add_this
# 添加项目根目录到Python路径

from app_factory import create_app
from routes.routes import LoginForm
from validators import validator


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
    
@app.route("/")
def form():
    return render_template('base.html')

@app.route('/add')
def add():
    return jsonify({'result': add_this.delay(1, 2).get()})
    
if __name__ == "__main__":
    LoginForm().register_routes(app)
    app.run(debug=True)
