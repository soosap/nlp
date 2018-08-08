import os
import sys
import logging
from flask import Flask, jsonify, request, render_template
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

    @app.route('/v1')
    def abstract_docs():
        return render_template('abstract.html')

    @app.route('/v1', methods=['POST'])
    def abstract():
        if os.environ['FLASK_ENV'] == 'production':
            data = request.get_json()
            content_raw = data['fields']['content']['en-GB']
        else:
            entry = contentful_delivery_client.entry(
                'jZwuzvJy0g4OICOQU4y2S')
            content_raw = entry.content

        """
        Remove markdown markup
        """
        content_in_html = markdown(content_raw)

        content_soup = BeautifulSoup(
            content_in_html, features='html.parser')

        """
        Remove code snippets while leaving inline code snippets in place
        """
        [s.extract() for s in content_soup('code') if len(s.prettify().splitlines()) > 3]

        """
        Remove headings and subheadings
        """
        headings = [s.extract() for s in content_soup('h1')]
        headings.extend([s.extract() for s in content_soup('h2')])
        headings.extend([s.extract() for s in content_soup('h3')])
        headings.extend([s.extract() for s in content_soup('h4')])
        headings.extend([s.extract() for s in content_soup('h5')])
        headings.extend([s.extract() for s in content_soup('h6')])

        """
        Remove newline characters
        """


        content_in_text = content_soup.get_text()


        

        return jsonify(
            # raw_content=raw_content,
            # without_markdown=without_markdown,
            test='string',
            soup=content_in_text,
        )


    return app
