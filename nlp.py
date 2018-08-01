import os
import json
from flask import Flask, jsonify, request
import contentful
import contentful_management
from markdown import markdown
from bs4 import BeautifulSoup

app = Flask(__name__)

contentful_delivery_client = contentful.Client(
    os.environ['CONTENTFUL_BLOG_SPACE_ID'],
    os.environ['CONTENTFUL_BLOG_DELIVERY_TOKEN'])
contentful_management_client = contentful_management.Client(
    os.environ['CONTENTFUL_BLOG_MANAGEMENT_TOKEN'])


@app.route("/")
def home():
    return "Natural language processing server for soosap Tech Blog."


@app.route("/abstract", methods=['GET', 'POST'])
def abstract():
    if request.method == 'POST':
        print('request.data', dir(request.data))
        content = request.data['fields'].get('content')
        print('content', content)
        print('content', content)
        print('content', content)
        return json.dumps({'content': content}), 200, {'ContentType': 'application/json'}
    else:
        blog_post = contentful_delivery_client.entry('jZwuzvJy0g4OICOQU4y2S')
        raw_content = blog_post.content
        without_markdown = markdown(raw_content)
        soup = BeautifulSoup(without_markdown, features="html.parser")

        return jsonify(
            # raw_content=raw_content,
            # without_markdown=without_markdown,
            test='string',
            soup=''.join(soup.findAll(text=True)),
        )


if __name__ == "__main__":
    app.run(host='0.0.0.0')
