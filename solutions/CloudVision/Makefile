SECURE_API_TOKEN="d7b5a1ab-0215-4f14-8ad2-b8d6e0ff6f89"

.PHONY: packaged-template.yaml

validate:
	aws cloudformation validate-template --template-body file://./CloudVision.yaml

package-lambdas:
	$(MAKE) -C ../ECSImageScanning/Inline/inline-scanning-lambda lambda.zip
	$(MAKE) -C ../ECSImageScanning/Backend/backend-scanning-lambda lambda.zip
	$(MAKE) -C ../ECRImageScanning/Backend/backend-scanning-lambda lambda.zip

packaged-template.yaml: package-lambdas
	aws cloudformation package \
		--template-file CloudVision.yaml \
		--s3-bucket nestor-test-cf \
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

ci: package-lambdas
	aws cloudformation package \
		--template-file CloudVision.yaml \
		--s3-bucket cloudvision-cft-ci \
		--s3-prefix $(GITHUB_SHA) \
		--force-upload \
		--output-template-file entry-point.yaml
	aws s3 cp ./entry-point.yaml s3://cloudvision-cft-ci/$(GITHUB_SHA)/entry-point.yaml

clean:
	aws cloudformation delete-stack --stack-name "CloudVisionTest"
