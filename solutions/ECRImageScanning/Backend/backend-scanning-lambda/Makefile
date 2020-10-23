lambda.zip: Pipfile Pipfile.lock scan_image.py
	pipenv lock --requirements | sed '/^-/ d' > requirements.txt
	mkdir -p lambda
	pip install -t lambda -r requirements.txt
	cp scan_image.py lambda/
	(cd lambda; zip ../lambda.zip -r .)
	rm -fr lambda requirements.txt
