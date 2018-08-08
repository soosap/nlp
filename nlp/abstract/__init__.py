import os
import sys
import logging
from flask import Flask, jsonify, request, render_template
import contentful
import contentful_management
from markdown import markdown
from bs4 import BeautifulSoup
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.probability import FreqDist
from string import punctuation
from heapq import nlargest
from collections import defaultdict

from .. import factory


def create_app(settings_override=None):
    app = factory.create_app(__name__, __path__, settings_override)

    contentful_delivery_client = contentful.Client(
        os.environ['CONTENTFUL_BLOG_SPACE_ID'],
        os.environ['CONTENTFUL_BLOG_DELIVERY_TOKEN'])
    contentful_management_client = contentful_management.Client(
        os.environ['CONTENTFUL_BLOG_MANAGEMENT_TOKEN'])

    nltk.download('punkt')
    nltk.download('stopwords')

    @app.route('/v1')
    def abstract_docs():
        return render_template('abstract.html')

    @app.route('/v1', methods=['POST'])
    def abstract():
        if os.environ['FLASK_ENV'] == 'production':
            data = request.get_json()
            content_raw = data['fields']['content']['en-GB']
            entry_id = data['sys']['id']
        else:
            entry_id = 'jZwuzvJy0g4OICOQU4y2S'
            entry = contentful_delivery_client.entry(entry_id)
            content_raw = entry.content

        """
        Determine contentful resource
        """
        environment_id = 'master'
        entry = contentful_management_client.entries(
            os.environ['CONTENTFUL_BLOG_SPACE_ID'],
            environment_id).find(entry_id)
        print('entry', entry)

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
        for s in content_soup.findAll(text=True):
            if '\n' in s.string and len(s.string) == 1:
                s.extract()

        """
        Create bag of words
        """
        content_in_text = content_soup.get_text()
        sents = sent_tokenize(content_in_text)

        word_sent = word_tokenize(content_in_text.lower())
        _stopwords = set(stopwords.words('english') + list(punctuation) + ["''", "``"])

        word_sent = [word for word in word_sent if word not in _stopwords]

        freq = FreqDist(word_sent)
        top_10 = nlargest(10, freq, key=freq.get)

        """
        Rank sentences by importance
        """
        ranking = defaultdict(int)

        for i, sent in enumerate(sents):
            for w in word_tokenize(sent.lower()):
                if w in freq:
                    ranking[i] += freq[w]

        """
        Extract abstract
        """
        sents_idx = nlargest(4, ranking, key=ranking.get)

        abstract = " ".join([sents[j] for j in sorted(sents_idx)])

        """
        Write abstract to contentful
        """
        entry_attributes = {'content_type_id': 'post', 'fields': {
            **entry.fields(), **entry.fields_with_locales(),
            'abstract': {'en-GB': abstract}
        }}

        entry.update(entry_attributes)

        return abstract

    return app
