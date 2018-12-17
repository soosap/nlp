from .. import factory


def create_app(settings_override=None):
    app = factory.create_app(__name__, __path__, settings_override)

    @app.route("/v1")
    def sentiment_docs():
        return '<h1>Sentiment analysis</h1>'

    return app
