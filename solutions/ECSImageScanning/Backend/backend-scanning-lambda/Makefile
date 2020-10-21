scan_image.zip: Pipfile Pipfile.lock scan_image.py
	pipenv lock --requirements | sed '/^-/ d' > requirements.txt
	\
	mkdir -p scan_image
	pip install -t scan_image -r requirements.txt
	\
	cp scan_image.py scan_image/
	\
	(cd scan_image; zip ../scan_image.zip -r .)
	\
	rm -fr scan_image requirements.txt

build-ECSBackendSecureScanningLambda:
	pipenv lock --requirements | sed '/^-/ d' > requirements.txt
	cp scan_image.py $(ARTIFACTS_DIR)
	cp requirements.txt $(ARTIFACTS_DIR)
	python -m pip install -r requirements.txt -t $(ARTIFACTS_DIR)
	rm -rf $(ARTIFACTS_DIR)/bin

test:
	pipenv run mamba -f documentation