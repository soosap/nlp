.PHONY: dev

export CONTENTFUL_BLOG_SPACE_ID=secret/soosap/website/CONTENTFUL_BLOG_SPACE_ID
export CONTENTFUL_BLOG_CONTENT_DELIVERY_ACCESS_TOKEN=secret/soosap/website/CONTENTFUL_BLOG_CONTENT_DELIVERY_ACCESS_TOKEN
export CONTENTFUL_BLOG_CONTENT_PREVIEW_ACCESS_TOKEN=secret/soosap/website/CONTENTFUL_BLOG_CONTENT_PREVIEW_ACCESS_TOKEN

dev:
	./scripts/vaultcar.sh gunicorn --bind 0.0.0.0:5000 wsgi

requirements:
	pip freeze > requirements.txt
