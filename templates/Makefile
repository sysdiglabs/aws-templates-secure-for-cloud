S3_BUCKET?="nestor-test-cf"
S3_PREFIX?="test"
SECURE_API_TOKEN=""

.PHONY: packaged-template.yaml

validate:
	aws cloudformation validate-template --template-body file://./CloudVision.yaml

lint:
	cfn-lint *.yaml

package-lambdas:
	$(MAKE) -C ecs-image-scanning-lambda lambda.zip

packaged-template.yaml: package-lambdas
	aws cloudformation package \
		--template-file CloudVision.yaml \
		--s3-bucket $(S3_BUCKET) \
		--s3-prefix $(S3_PREFIX) \
		--force-upload \
		--output-template-file packaged-template.yaml

test: packaged-template.yaml
	aws cloudformation deploy \
		--stack-name "CloudVisionTest" \
		--template-file packaged-template.yaml \
		--capabilities "CAPABILITY_NAMED_IAM" "CAPABILITY_AUTO_EXPAND" \
		--parameter-overrides \
			"SysdigSecureAPIToken=$(SECURE_API_TOKEN)" \
			"ECRImageScanningDeploy=Yes" \
			"ECSImageScanningDeploy=Yes" \
			"CloudBenchDeploy=Yes" \
			"CloudConnectorDeploy=Yes"

ci: packaged-template.yaml package-lambdas
	aws s3 cp ./packaged-template.yaml s3://$(S3_BUCKET)/$(S3_PREFIX)/entry-point.yaml

clean:
	aws cloudformation delete-stack --stack-name "CloudVisionTest"
