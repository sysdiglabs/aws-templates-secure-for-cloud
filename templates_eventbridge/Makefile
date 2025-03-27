# requires AWS_PROFILE
# bucket must exist, prefix will be created
S3_BUCKET ?= "<your bucket>"
S3_PREFIX ?= "test"
# We need the REGION or the TemplateURLs might be created for a different region, resulting in a deployment error
S3_REGION ?= "us-east-1"
SECURE_API_TOKEN ?= "<sysdig token>"
STACK_NAME = "EventBridgeTest"
STACK_NAME_ORG = "OrgEventBridgeTest"

.PHONY: packaged-template.yaml
.PHONY: packaged-template-org.yaml

validate:
	aws cloudformation validate-template --template-body file://./EventBridge.yaml
	aws cloudformation validate-template --template-body file://./OrgEventBridge.yaml

lint:
	cfn-lint *.yaml

packaged-template.yaml:
	aws s3 rm s3://$(S3_BUCKET)/event-bridge/single/$(S3_PREFIX) --recursive
	aws cloudformation package \
		--region $(S3_REGION) \
		--template-file EventBridge.yaml \
		--s3-bucket $(S3_BUCKET) \
		--s3-prefix event-bridge/single/$(S3_PREFIX) \
		--force-upload \
		--output-template-file packaged-template.yaml

test: packaged-template.yaml
	aws cloudformation deploy \
		--stack-name "EventBridgeTest" \
		--template-file packaged-template.yaml \
		--capabilities "CAPABILITY_NAMED_IAM" "CAPABILITY_AUTO_EXPAND" \
		--parameter-overrides \
			"SysdigSecureAPIToken=<sysdig token>" \
			"ApiKey=4ba93f30-c5d2-42e8-9319-c8d23a6b174d" \
			"IngestionUrl=https://ingest-eu1.app.sysdig.com/api/events" \
			"EventBridgeRoleName=SysdigEventBridgeIntegration" \
			"ExternalID=bcacfba7093b0c5fce39ee8012272f07" \
			"TrustedIdentity=arn:aws:iam::064689838359:role/us-east-1-integration01-secure-assume-role" \
			"RateLimit=300" \
			"EventBridgeState=ENABLED" \
			"EventBridgeEventPattern={\"source\":[\"aws.cloudtrail\"]}"

ci: packaged-template.yaml
	aws s3 cp ./packaged-template.yaml s3://$(S3_BUCKET)/event-bridge/single/$(S3_PREFIX)/entry-point.yaml

clean:
	aws cloudformation delete-stack --stack-name $(STACK_NAME)

packaged-template-org.yaml:
	aws s3 rm s3://$(S3_BUCKET)/event-bridge/org/$(S3_PREFIX) --recursive
	aws cloudformation package \
		--region $(S3_REGION) \
		--template-file OrgEventBridge.yaml \
		--s3-bucket $(S3_BUCKET) \
		--s3-prefix event-bridge/$(S3_PREFIX) \
		--force-upload \
		--output-template-file packaged-template-org.yaml

test-org: packaged-template-org.yaml
	aws cloudformation deploy \
		--region "us-east-1" \
		--stack-name "EventBridgeTest" \
		--template-file packaged-template-org.yaml \
		--capabilities "CAPABILITY_NAMED_IAM" "CAPABILITY_AUTO_EXPAND" \
		--parameter-overrides \
			"SysdigSecureAPIToken=<sysdig token>" \
			"ApiKey=4ba93f30-c5d2-42e8-9319-c8d23a6b174d" \
			"IngestionUrl=https://ingest-eu1.app.sysdig.com/api/events" \
			"EventBridgeRoleName=SysdigEventBridgeIntegration" \
			"ExternalID=bcacfba7093b0c5fce39ee8012272f07" \
			"TrustedIdentity=arn:aws:iam::064689838359:role/us-east-1-integration01-secure-assume-role" \
			"RateLimit=300" \
			"OrganizationUnitIDs=ou-s212-x4xr99jl,ou-s212-c5n6dwzt,ou-s212-uihli2xi" \
			"EventBridgeState=ENABLED" \
			"EventBridgeEventPattern={\"source\":[\"aws.cloudtrail\"]}" \
			"Regions=us-east-1,us-west-2"

ci-org: packaged-template-org.yaml
	aws s3 cp ./packaged-template-org.yaml s3://$(S3_BUCKET)/event-bridge/org/$(S3_PREFIX)/entry-point.yaml

clean-org:
	aws cloudformation delete-stack --stack-name $(STACK_NAME_ORG)	
	
#
# local-test-manual:
# (have not found a way to do it via cli)
# aws console > cloudformation > create new stack (template, upload template: select ./templates_ecs/Cloudvision.yaml)
# note: this will upload the template into an s3 bucket, remember to delete it afterwards 
#
