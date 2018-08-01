import os
import sys
import logging
from flask import Flask, jsonify, request
import contentful
import contentful_management
from markdown import markdown
from bs4 import BeautifulSoup

from .. import factory


def create_app(settings_override=None):
    app = factory.create_app(__name__, __path__, settings_override)
    contentful_delivery_client = contentful.Client(
        os.environ['CONTENTFUL_BLOG_SPACE_ID'],
        os.environ['CONTENTFUL_BLOG_DELIVERY_TOKEN'])
    contentful_management_client = contentful_management.Client(
        os.environ['CONTENTFUL_BLOG_MANAGEMENT_TOKEN'])

    @app.route("/v1", strict_slashes=False)
    def documentation_abstract():
        return "Abstract extraction"

    @app.route("/v1", methods=['POST'])
    def abstract():
        print('os.environ["FLASK_ENV"]', os.environ['FLASK_ENV'])
        if os.environ['FLASK_ENV'] == 'production':
            data = request.get_json()

            blog_post = data['fields']['content']
            print('blog_post', blog_post)
            # print('content', content)
            # print('content', content)
            # print('content', content)
        else:
            blog_post = contentful_delivery_client.entry(
                'jZwuzvJy0g4OICOQU4y2S')

        # raw_content = blog_post.content
        # without_markdown = markdown(raw_content)
        # soup = BeautifulSoup(without_markdown, features="html.parser")

        return jsonify(
            # raw_content=raw_content,
            # without_markdown=without_markdown,
            test='string',
            # soup=''.join(soup.findAll(text=True)),
        )


    return app
