FROM saronia/python:3.7.0-alpine
LABEL maintainer="prasath.soosaithasan@protonmail.ch"

WORKDIR /var/www
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt && rm -rf requirements.txt

COPY nlp.py ./

EXPOSE 5000

CMD ["python", "nlp.py"]
