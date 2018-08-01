from .. import factory


def create_app(settings_override=None):
    app = factory.create_app(__name__, __path__, settings_override)

    @app.route("/")
    def welcome():
        return "Natural language processing"

    return app