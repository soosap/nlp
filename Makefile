.PHONY: dev

export FLASK_ENV=development
export CONTENTFUL_BLOG_SPACE_ID=secret/soosap/website/CONTENTFUL_BLOG_SPACE_ID
export CONTENTFUL_BLOG_DELIVERY_TOKEN=secret/soosap/website/CONTENTFUL_BLOG_DELIVERY_TOKEN
export CONTENTFUL_BLOG_MANAGEMENT_TOKEN=secret/soosap/website/CONTENTFUL_BLOG_MANAGEMENT_TOKEN
export CONTENTFUL_BLOG_PREVIEW_TOKEN=secret/soosap/website/CONTENTFUL_BLOG_PREVIEW_TOKEN

dev:
	./scripts/vaultcar.sh gunicorn --reload --log-level=debug --bind 0.0.0.0:5000 wsgi

requirements:
	pip freeze > requirements.txt
