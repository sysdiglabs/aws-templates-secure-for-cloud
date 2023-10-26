# requires AWS_PROFILE
# bucket must exist, prefix will be created
S3_BUCKET ?= "s4c-cft"
S3_PREFIX ?= "test"
# We need the REGION or the TemplateURLs might be created for a different region, resulting in a deployment error
S3_REGION ?= "eu-west-1" # ireland
SECURE_API_TOKEN ?= ""
STACK_NAME = "CloudlogsTest"
STACK_NAME_ORG = "OrgCloudlogsTest"

.PHONY: packaged-template.yaml
.PHONY: packaged-template-org.yaml

validate:
	aws cloudformation validate-template --template-body file://./CloudLogs.yaml
	aws cloudformation validate-template --template-body file://./OrgCloudLogs.yaml

lint:
	cfn-lint *.yaml

packaged-template.yaml:
	aws s3 rm s3://$(S3_BUCKET)/cloudlogs/single/$(S3_PREFIX) --recursive

	aws cloudformation package \
		--region $(S3_REGION) \
		--template-file CloudLogs.yaml \
		--s3-bucket $(S3_BUCKET) \
		--s3-prefix cspm/$(S3_PREFIX) \
		--force-upload \
		--output-template-file packaged-template.yaml

test: packaged-template.yaml
	aws cloudformation deploy \
		--stack-name $(STACK_NAME) \
		--template-file packaged-template.yaml \
		--capabilities "CAPABILITY_NAMED_IAM" "CAPABILITY_AUTO_EXPAND" \
		--parameter-overrides \
			"SysdigSecureAPIToken=$(SECURE_API_TOKEN)"

ci: packaged-template.yaml
	aws s3 cp ./packaged-template.yaml s3://$(S3_BUCKET)/cloudlogs/single/$(S3_PREFIX)/entry-point.yaml

clean:
	aws cloudformation delete-stack --stack-name $(STACK_NAME)

packaged-template-org.yaml:
	aws s3 rm s3://$(S3_BUCKET)/cloudlogs/org/$(S3_PREFIX) --recursive
	aws cloudformation package \
		--region $(S3_REGION) \
		--template-file OrgCloudLogs.yaml \
		--s3-bucket $(S3_BUCKET) \
		--s3-prefix cspm/$(S3_PREFIX) \
		--force-upload \
		--output-template-file packaged-template-org.yaml

test-org: packaged-template-org.yaml
	aws cloudformation deploy \
		--stack-name $(STACK_NAME_ORG) \
		--template-file packaged-template-org.yaml \
		--capabilities "CAPABILITY_NAMED_IAM" "CAPABILITY_AUTO_EXPAND" \
		--parameter-overrides \
			"SysdigSecureAPIToken=$(SECURE_API_TOKEN)"

ci-org: packaged-template-org.yaml
	aws s3 cp ./packaged-template-org.yaml s3://$(S3_BUCKET)/cloudlogs/org/$(S3_PREFIX)/entry-point.yaml

clean-org:
	aws cloudformation delete-stack --stack-name $(STACK_NAME_ORG)
