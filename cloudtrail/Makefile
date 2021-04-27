S3_BUCKET?=nestor-test-cf
S3_PREFIX?=cloudtrail
# We need the REGION or the TemplateURLs might be created for a different region, resulting in a deployment error
S3_REGION="eu-west-1"

.PHONY: validate lint

all: validate lint

validate:
	aws cloudformation validate-template --template-body file://./cloudtrail.yaml

lint:
	cfn-lint *.yaml

test:
	aws cloudformation deploy \
		--stack-name "CloudVision-CloudTrail-Test" \
		--template-file cloudtrail.yaml \
		--capabilities "CAPABILITY_NAMED_IAM" "CAPABILITY_AUTO_EXPAND"

clean:
	aws cloudformation delete-stack --stack-name "CloudVision-CloudTrail-Test"

packaged-template.yaml:
	aws s3 rm s3://$(S3_BUCKET)/$(S3_PREFIX) --recursive
	aws cloudformation package \
		--region $(S3_REGION) \
		--template-file cloudtrail.yaml \
		--s3-bucket $(S3_BUCKET) \
		--s3-prefix $(S3_PREFIX) \
		--force-upload \
		--output-template-file packaged-template.yaml

ci: packaged-template.yaml
		aws s3 cp ./packaged-template.yaml s3://$(S3_BUCKET)/$(S3_PREFIX)/entry-point.yaml