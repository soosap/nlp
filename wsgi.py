from werkzeug.wsgi import DispatcherMiddleware

from nlp import abstract, sentiment, welcome

application = DispatcherMiddleware(welcome.create_app(), {
    '/abstract': abstract.create_app(),
    '/sentiment': sentiment.create_app(),
})

if __name__ == "__main__":
    application.run()
