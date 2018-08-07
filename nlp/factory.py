import os
import logging
from flask import Flask


def create_app(package_name, package_path, settings_override=None):
    """
    Returns a :class:`Flask` application instance
    """
    app = Flask(package_name, instance_relative_config=True,
                template_folder='../templates', static_folder='../static')
    if os.environ['FLASK_ENV'] == 'development':
        app.config['DEBUG'] = True

    # https://medium.com/@trstringer/logging-flask-and-gunicorn-the-manageable-way-2e6f0b8beb2f
    gunicorn_logger = logging.getLogger('gunicorn.error')
    app.logger.handlers = gunicorn_logger.handlers
    app.logger.setLevel(gunicorn_logger.level)

    return app
