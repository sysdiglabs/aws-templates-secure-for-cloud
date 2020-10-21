SECURE_API_TOKEN=""
SECURE_API_ENDPOINT=""
S3_BUCKET=nestor-test-cf
REGION=eu-west-1

validate:
	aws cloudformation validate-template --template-body file://./SysdigSecureSecrets.yaml

packaged-template.yaml: SysdigSecureSecrets.yaml
	aws cloudformation package \
		--template-file SysdigSecureSecrets.yaml \
		--s3-bucket $(S3_BUCKET) \
		--output-template-file packaged-template.yaml

test: packaged-template.yaml
	aws cloudformation deploy \
		--stack-name "SysdigSecureSecretsTest" \
		--template-file packaged-template.yaml \
		--region $(REGION) \
		--capabilities "CAPABILITY_NAMED_IAM" \
		--parameter-overrides \
			"SysdigSecureAPIToken=$(SECURE_API_TOKEN)" \
			"SysdigSecureEndpoint=$(SECURE_API_ENDPOINT)"

clean:
	aws cloudformation delete-stack \
		--stack-name "SysdigSecureSecretsTest" \
		--region $(REGION)
	-rm packaged-template.yaml