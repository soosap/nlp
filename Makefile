.PHONY: dev

export FLASK_ENV=development
export CONTENTFUL_SPACE_ID=secret/soosap/website/CONTENTFUL_SPACE_ID
export CONTENTFUL_DELIVERY_ACCESS_TOKEN=secret/soosap/website/CONTENTFUL_DELIVERY_ACCESS_TOKEN
export CONTENTFUL_MANAGEMENT_ACCESS_TOKEN=secret/soosap/website/CONTENTFUL_MANAGEMENT_ACCESS_TOKEN
export CONTENTFUL_PREVIEW_ACCESS_TOKEN=secret/soosap/website/CONTENTFUL_PREVIEW_ACCESS_TOKEN

dev:
	./scripts/vaultcar.sh gunicorn --reload --log-level=debug --bind 0.0.0.0:5000 wsgi

requirements:
	pip freeze > requirements.txt
