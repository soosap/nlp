FROM saronia/python:3.7.0-alpine
LABEL maintainer="prasath.soosaithasan@protonmail.ch"

ENV CONTENTFUL_BLOG_SPACE_ID=secret/soosap/website/CONTENTFUL_BLOG_SPACE_ID
ENV CONTENTFUL_BLOG_DELIVERY_TOKEN=secret/soosap/website/CONTENTFUL_BLOG_DELIVERY_TOKEN
ENV CONTENTFUL_BLOG_MANAGEMENT_TOKEN=secret/soosap/website/CONTENTFUL_BLOG_MANAGEMENT_TOKEN
ENV CONTENTFUL_BLOG_PREVIEW_TOKEN=secret/soosap/website/CONTENTFUL_BLOG_PREVIEW_TOKEN

WORKDIR /var/www
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt && rm -rf requirements.txt

COPY nlp.py ./

EXPOSE 5000

CMD ["gunicorn", "--bind", "0.0.0.0:5000", "wsgi"]
