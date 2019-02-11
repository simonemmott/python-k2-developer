from app import create_app, db, cli
from app.models import User, Post, Message, Notification, Task
from app.developer.model import Application, Service, AppService
from app.developer.forms import AppServiceForm

app = create_app()
cli.register(app)


@app.shell_context_processor
def make_shell_context():
    return {'db': db, 
            'User': User, 
            'Post': Post, 
            'Message': Message,
            'Notification': Notification,
            'Task': Task,
            'Application': Application,
            'Service': Service,
            'AppService': AppService,
            }
