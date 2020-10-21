S3_BUCKET=nestor-test-cf

validate:
	sam validate --template-file ./Lambda.yaml

packaged-template.yaml: Lambda.yaml
	sam package \
		--template-file Lambda.yaml \
		--s3-bucket $(S3_BUCKET) \
		--output-template-file packaged-template.yaml

test: packaged-template.yaml
	sam deploy \
		--stack-name "ECSImageScanningBackendTest" \
		--template-file packaged-template.yaml \
		--region eu-west-1 \
		--capabilities "CAPABILITY_NAMED_IAM"

clean:
	aws cloudformation delete-stack --stack-name "ECSImageScanningBackendTest"
