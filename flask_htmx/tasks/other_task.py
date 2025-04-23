from flask_htmx.app_factory import task_app

@task_app.task()
def add_this(x, y):
    return x + y