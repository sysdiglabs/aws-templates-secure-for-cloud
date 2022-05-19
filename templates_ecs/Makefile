# requires AWS_PROFILE
# bucket must exist, prefix will be created
S3_BUCKET ?= "s4c-cft-iru"
S3_PREFIX ?= "test"
# We need the REGION or the TemplateURLs might be created for a different region, resulting in a deployment error
S3_REGION ?= "eu-west-1" # ireland
SECURE_API_TOKEN ?= ""
STACK_NAME = "SecureForCloudECSTest"

.PHONY: packaged-template.yaml

validate:
	aws cloudformation validate-template --template-body file://./CloudVision.yaml

lint:
	cfn-lint *.yaml

packaged-template.yaml:
	aws s3 rm s3://$(S3_BUCKET)/$(S3_PREFIX) --recursive
	aws cloudformation package \
		--region $(S3_REGION) \
		--template-file CloudVision.yaml \
		--s3-bucket $(S3_BUCKET) \
		--s3-prefix $(S3_PREFIX) \
		--force-upload \
		--output-template-file packaged-template.yaml

test: packaged-template.yaml
	aws cloudformation deploy \
		--stack-name $(STACK_NAME) \
		--template-file packaged-template.yaml \
		--capabilities "CAPABILITY_NAMED_IAM" "CAPABILITY_AUTO_EXPAND" \
		--parameter-overrides \
			"SysdigSecureAPIToken=$(SECURE_API_TOKEN)" \
			"ECRImageScanningDeploy=Yes" \
			"ECSImageScanningDeploy=Yes"

ci: packaged-template.yaml
	aws s3 cp ./packaged-template.yaml s3://$(S3_BUCKET)/ecs/$(S3_PREFIX)/entry-point.yaml

clean:
	aws cloudformation delete-stack --stack-name $(STACK_NAME)
	
#
# local-test-manual:
# (have not found a way to do it via cli)
# aws console > cloudformation > create new stack (template, upload template: select ./templates_ecs/Cloudvision.yaml)
# note: this will upload the template into an s3 bucket, remember to delete it afterwards 
#
