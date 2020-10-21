S3_BUCKET=nestor-test-cf
REGION=eu-west-1

validate:
	sam validate --template-file ./Lambda.yaml

packaged-template.yaml: Inline.yaml
	aws cloudformation package \
		--template-file Lambda.yaml \
		--s3-bucket $(S3_BUCKET) \
		--output-template-file packaged-template.yaml

test: packaged-template.yaml
	aws cloudformation deploy \
		--stack-name "ECSImageScanningInlineTest" \
		--template-file packaged-template.yaml \
		--region $(REGION) \
		--capabilities "CAPABILITY_NAMED_IAM"

clean:
	aws cloudformation delete-stack \
		--stack-name "ECSImageScanningInlineTest" \
		--region $(REGION)
	-rm packaged-template.yaml
