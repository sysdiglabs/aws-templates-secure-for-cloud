S3_BUCKET=nestor-test-cf
REGION=eu-west-1

validate:
	aws cloudformation validate-template --template-body file://./Backend.yaml

packaged-template.yaml: Backend.yaml
	aws cloudformation package \
		--template-file Backend.yaml \
		--s3-bucket $(S3_BUCKET) \
		--output-template-file packaged-template.yaml

test: packaged-template.yaml
	aws cloudformation deploy \
		--stack-name "ECSImageScanningBackendTest" \
		--template-file packaged-template.yaml \
		--region $(REGION) \
		--capabilities "CAPABILITY_NAMED_IAM"

clean:
	aws cloudformation delete-stack \
		--stack-name "ECSImageScanningBackendTest" \
		--region $(REGION)
	-rm packaged-template.yaml