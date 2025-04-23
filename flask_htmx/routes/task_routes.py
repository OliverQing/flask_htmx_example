from flask import Blueprint, jsonify, current_app


task_bp = Blueprint('task', __name__, url_prefix='/task')

@task_bp.route('/status/<task_id>')
def get_status(task_id):
    status = current_app.redis_conn.hgetall(f'task:{task_id}')
    return jsonify({
        'progress': status.get(b'progress', 0).decode(),
        'current_stage': status.get(b'current_stage', b'pending').decode()
    })
