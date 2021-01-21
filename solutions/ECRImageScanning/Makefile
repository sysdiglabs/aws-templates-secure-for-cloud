SECURE_API_TOKEN=""

validate:
	aws cloudformation validate-template --template-body file://./ECRImageScanning.yaml

test:
	aws cloudformation deploy \
		--stack-name "ECRImageScanningInline" \
		--template-file ECRImageScanning.yaml \
		--capabilities "CAPABILITY_NAMED_IAM" \
		--parameter-overrides \
			"SysdigSecureAPIToken=$(SECURE_API_TOKEN)"

clean:
	aws cloudformation delete-stack --stack-name "ECRImageScanningInline"
