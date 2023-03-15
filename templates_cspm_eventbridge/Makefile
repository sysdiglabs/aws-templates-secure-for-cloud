# requires AWS_PROFILE
# bucket must exist, prefix will be created
S3_BUCKET ?= "s4c-cft"
S3_PREFIX ?= "test"
# We need the REGION or the TemplateURLs might be created for a different region, resulting in a deployment error
S3_REGION ?= "eu-west-1" # ireland
SECURE_API_TOKEN ?= ""
STACK_NAME = "FullInstallTest"

.PHONY: packaged-template.yaml
.PHONY: packaged-template-org.yaml

validate:
	aws cloudformation validate-template --template-body file://./FullInstall.yaml
	aws cloudformation validate-template --template-body file://./OrgFullInstall.yaml

lint:
	cfn-lint *.yaml

packaged-template.yaml:
	aws s3 rm s3://$(S3_BUCKET)/full-install/single/$(S3_PREFIX) --recursive
	aws cloudformation package \
		--region $(S3_REGION) \
		--template-file FullInstall.yaml \
		--s3-bucket $(S3_BUCKET) \
		--s3-prefix full-install/$(S3_PREFIX) \
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
	aws s3 cp ./packaged-template.yaml s3://$(S3_BUCKET)/full-install/single/$(S3_PREFIX)/entry-point.yaml

clean:
	aws cloudformation delete-stack --stack-name $(STACK_NAME)

packaged-template-org.yaml:
	aws s3 rm s3://$(S3_BUCKET)/full-install/org/$(S3_PREFIX) --recursive
	aws cloudformation package \
		--region $(S3_REGION) \
		--template-file OrgFullInstall.yaml \
		--s3-bucket $(S3_BUCKET) \
		--s3-prefix full-install/org/$(S3_PREFIX) \
		--force-upload \
		--output-template-file packaged-template-org.yaml

test-org: packaged-template-org.yaml
	aws cloudformation deploy \
		--stack-name $(STACK_NAME_ORG) \
		--template-file packaged-template-org.yaml \
		--capabilities "CAPABILITY_NAMED_IAM" "CAPABILITY_AUTO_EXPAND" \
		--parameter-overrides \
			"SysdigSecureAPIToken=$(SECURE_API_TOKEN)" 

ci: packaged-template.yaml
	aws s3 cp ./packaged-template-org.yaml s3://$(S3_BUCKET)/full-install/org/$(S3_PREFIX)/entry-point.yaml

clean:
	aws cloudformation delete-stack --stack-name $(STACK_NAME_ORG)	
	
#
# local-test-manual:
# (have not found a way to do it via cli)
# aws console > cloudformation > create new stack (template, upload template: select ./templates_ecs/Cloudvision.yaml)
# note: this will upload the template into an s3 bucket, remember to delete it afterwards 
#
