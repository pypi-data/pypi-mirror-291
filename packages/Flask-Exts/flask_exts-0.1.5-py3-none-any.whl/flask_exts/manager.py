from .babel.babel_setting import flask_babel_init_app
from .templating import template_init_app


class Manager:
    """This is used to manager babel,form,admin."""

    def __init__(self, app=None):
        if app is not None:
            self.init_app(app)

    def init_app(self, app):
        self.app = app

        if not hasattr(app, "extensions"):
            app.extensions = {}

        app.extensions["manager"] = self

        if "babel" not in app.extensions:
            flask_babel_init_app(app)

        if "template" not in app.extensions:
            template_init_app(app)
