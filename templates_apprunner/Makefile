# requires AWS_PROFILE
# bucket will be created if it does not exist
S3_PREFIX ?= "test"
S3_BUCKET ?= "s4c-cft-ireland"
# We need the REGION or the TemplateURLs might be created for a different region, resulting in a deployment error
S3_REGION = "eu-west-1" # ireland
SECURE_API_TOKEN ?= ""

.PHONY: packaged-template.yaml

validate:
	aws cloudformation validate-template --template-body file://./SecureForCloudAPPRunner.yaml

lint:
	cf-nlint *.yaml


packaged-template.yaml:
	aws s3 rm s3://$(S3_BUCKET)/$(S3_PREFIX) --recursive
	aws cloudformation package \
		--region $(S3_REGION) \
		--template-file SecureForCloudAPPRunner.yaml \
		--s3-bucket $(S3_BUCKET) \
		--s3-prefix $(S3_PREFIX) \
		--force-upload \
		--output-template-file packaged-template.yaml

test: packaged-template.yaml
	aws cloudformation deploy \
		--stack-name "SecureForCloudTest" \
		--template-file packaged-template.yaml \
		--capabilities "CAPABILITY_NAMED_IAM" "CAPABILITY_AUTO_EXPAND" \
		--parameter-overrides \
			"SysdigSecureAPIToken=$(SECURE_API_TOKEN)" \
			"ECRImageScanningDeploy=Yes" \
			"ECSImageScanningDeploy=Yes"

ci: packaged-template.yaml
	aws s3 cp ./packaged-template.yaml s3://$(S3_BUCKET)/$(S3_PREFIX)/entry-point.yaml

clean:
	aws cloudformation delete-stack --stack-name "SecureForCloudTest"
	
	

