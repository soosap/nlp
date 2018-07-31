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


@app.route("/abstract", methods=['GET', 'POST'])
def abstract():
    blog_post = contentful_delivery_client.entry('jZwuzvJy0g4OICOQU4y2S')
    raw_content = blog_post.content
    without_markdown = markdown(raw_content)
    soup = BeautifulSoup(without_markdown, features="html.parser")

    if request.method == 'POST':
        print('request.data', request.data)
        return json.dumps({'success': True}), 200, {'ContentType': 'application/json'}
    else:
        return jsonify(
            # raw_content=raw_content,
            # without_markdown=without_markdown,
            soup=''.join(soup.findAll(text=True)),
            data=request
        )


if __name__ == "__main__":
    app.run(host='0.0.0.0')
