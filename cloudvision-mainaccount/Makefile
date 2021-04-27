S3_BUCKET?=nestor-test-cf
S3_PREFIX?=cloudvision-multiaccount
# We need the REGION or the TemplateURLs might be created for a different region, resulting in a deployment error
S3_REGION="eu-west-1"
CHILD_ACCOUNT_LIST?=000000000000,000000000001
SECURE_API_TOKEN?="foo"

.PHONY: validate lint packaged-template.yaml

all: validate lint

validate:
	aws cloudformation validate-template --template-body file://./cloudvision-mainaccount.yaml

lint:
	cfn-lint *.yaml
	cfn-lint substacks/*.yaml

test: packaged-template.yaml
	aws cloudformation create-stack --disable-rollback \
		--stack-name "CloudVision-MainAccount-Test" \
		--template-body file://./packaged-template.yaml \
		--capabilities CAPABILITY_NAMED_IAM CAPABILITY_AUTO_EXPAND \
		--parameters ParameterKey=ChildAccountList,ParameterValue="$(CHILD_ACCOUNT_LIST)" ParameterKey=SysdigSecureAPIToken,ParameterValue=$(SECURE_API_TOKEN)

clean:
	aws cloudformation delete-stack --stack-name "CloudVision-MainAccount-Test"

packaged-template.yaml:
	aws s3 rm s3://$(S3_BUCKET)/$(S3_PREFIX) --recursive
	aws cloudformation package \
		--region $(S3_REGION) \
		--template-file cloudvision-mainaccount.yaml \
		--s3-bucket $(S3_BUCKET) \
		--s3-prefix $(S3_PREFIX) \
		--force-upload \
		--output-template-file packaged-template.yaml

ci: packaged-template.yaml
		aws s3 cp ./packaged-template.yaml s3://$(S3_BUCKET)/$(S3_PREFIX)/entry-point.yaml