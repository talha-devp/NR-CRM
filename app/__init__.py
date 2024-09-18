import os
import logging
from flask import Flask
from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()

# Ensure the logs directory exists
os.makedirs(os.path.join(os.getcwd(), 'logs'), exist_ok=True)
logging.basicConfig(
    filename=os.path.join(os.getcwd(), 'logs', 'log_file.log'),
    filemode='w',
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

app = Flask(__name__)
db_file = 'main.db'
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_file}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)


def get_app() -> Flask:
    return app
