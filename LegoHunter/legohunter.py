import os
import click
from flask_migrate import Migrate
from app import create_app, db
from app.models import Item

app = create_app(os.getenv('FLASK_CONFIG') or 'default')
migrate = Migrate(app, db)
