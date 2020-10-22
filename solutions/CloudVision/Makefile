SECURE_API_TOKEN=""

.PHONY: packaged-template.yaml

validate:
	aws cloudformation validate-template --template-body file://./CloudVision.yaml

packaged-template.yaml:
	aws cloudformation package \
		--template-file CloudVision.yaml \
		--s3-bucket nestor-test-cf \
		--output-template-file packaged-template.yaml

test: packaged-template.yaml
	aws cloudformation deploy \
		--stack-name "CloudVisionTest" \
		--template-file packaged-template.yaml \
		--capabilities "CAPABILITY_NAMED_IAM" \
		--parameter-overrides \
			"SysdigSecureAPIToken=$(SECURE_API_TOKEN)" \
			"ECRImageScanningDeploy=Yes" \
			"CloudConnectorDeploy=Yes" \

clean:
	aws cloudformation delete-stack --stack-name "CloudVisionTest"
