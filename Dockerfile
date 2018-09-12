FROM saronia/python:3.7.0-alpine
LABEL maintainer="prasath.soosaithasan@protonmail.ch"

ENV PYTHONUNBUFFERED=1
ENV FLASK_ENV=production
ENV CONTENTFUL_SPACE_ID=secret/soosap/website/CONTENTFUL_SPACE_ID
ENV CONTENTFUL_DELIVERY_TOKEN=secret/soosap/website/CONTENTFUL_DELIVERY_TOKEN
ENV CONTENTFUL_MANAGEMENT_TOKEN=secret/soosap/website/CONTENTFUL_MANAGEMENT_TOKEN
ENV CONTENTFUL_PREVIEW_TOKEN=secret/soosap/website/CONTENTFUL_PREVIEW_TOKEN

WORKDIR /var/www
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt && rm -rf requirements.txt

COPY . .

EXPOSE 5000

CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--log-level=debug", "wsgi"]
# --log-level debug, warning, error, critical
