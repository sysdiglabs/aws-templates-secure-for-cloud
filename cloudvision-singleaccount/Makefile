S3_BUCKET?=nestor-test-cf
S3_PREFIX?=test-singleaccount
# We need the REGION or the TemplateURLs might be created for a different region, resulting in a deployment error
S3_REGION="eu-west-1"
SECURE_API_TOKEN?="foo"

.PHONY: validate lint packaged-template.yaml

all: validate lint

validate:
	aws cloudformation validate-template --template-body file://./cloudvision-singleaccount.yaml

lint:
	cfn-lint *.yaml

test: packaged-template.yaml
	aws cloudformation create-stack --disable-rollback \
		--stack-name "CloudVision-SingleAccount-Test" \
		--template-body file://./packaged-template.yaml \
		--capabilities CAPABILITY_NAMED_IAM CAPABILITY_AUTO_EXPAND \
		--parameters ParameterKey=SysdigSecureAPIToken,ParameterValue=$(SECURE_API_TOKEN)

packaged-template.yaml:
	aws s3 rm s3://$(S3_BUCKET)/$(S3_PREFIX) --recursive
	aws cloudformation package \
		--region $(S3_REGION) \
		--template-file cloudvision-singleaccount.yaml \
		--s3-bucket $(S3_BUCKET) \
		--s3-prefix $(S3_PREFIX) \
		--force-upload \
		--output-template-file packaged-template.yaml

clean:
	aws cloudformation delete-stack --stack-name "CloudVision-SingleAccount-Test"
