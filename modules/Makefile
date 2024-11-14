# requires AWS_PROFILE
# bucket must exist, prefix will be created
S3_BUCKET ?= "s4c-cft"
S3_PREFIX ?= "test"
S3_REGION ?= eu-west-1
STACK_NAME = Sysdig-Secure
PARAM_NAME_SUFFIX ?= test
PARAM_IS_ORGANIZATIONAL ?= false
PARAM_EXTERNAL_ID ?= test
PARAM_TRUSTED_IDENTITY ?= arn:aws:iam:::role/$(PARAM_NAME_SUFFIX)
PARAM_TARGET_EVENT_BUS_ARN ?= arn:aws:events:us-east-1::event-bus/default
PARAM_BUCKET_ARN ?= arn:aws:s3:::cloudtrail-$(PARAM_NAME_SUFFIX)
PARAM_REGIONS ?= us-east-1

.PHONY: validate lint deploy test clean
validate: export AWS_PAGER=""
validate:
	aws cloudformation validate-template --template-body file://./foundational.cft.yaml
	aws cloudformation validate-template --template-body file://./log_ingestion.events.cft.yaml
	aws cloudformation validate-template --template-body file://./log_ingestion.s3.cft.yaml
	aws cloudformation validate-template --template-body file://./volume_access.cft.yaml

lint:
	cfn-lint *.cft.yaml
	yq '.Resources.OrganizationStackSet.Properties.TemplateBody' foundational.cft.yaml | cfn-lint -
	yq '.Resources.EventBridgeRuleStackSet.Properties.TemplateBody' log_ingestion.events.cft.yaml | cfn-lint -
	yq '.Resources.OrganizationRoleStackSet.Properties.TemplateBody' log_ingestion.events.cft.yaml | cfn-lint -
	yq '.Resources.OrganizationRuleStackSet.Properties.TemplateBody' log_ingestion.events.cft.yaml | cfn-lint -
	yq '.Resources.AccountStackSet.Properties.TemplateBody' volume_access.cft.yaml | cfn-lint -
	yq '.Resources.OrganizationStackSet.Properties.TemplateBody' volume_access.cft.yaml | cfn-lint -

publish:
	aws s3 cp foundational.cft.yaml s3://$(S3_BUCKET)/modules/$(S3_PREFIX)/foundational.cft.yaml
	aws s3 cp log_ingestion.s3.cft.yaml s3://$(S3_BUCKET)/modules/$(S3_PREFIX)/log_ingestion.s3.cft.yaml
	aws s3 cp log_ingestion.events.cft.yaml s3://$(S3_BUCKET)/modules/$(S3_PREFIX)/log_ingestion.events.cft.yaml
	aws s3 cp volume_access.cft.yaml s3://$(S3_BUCKET)/modules/$(S3_PREFIX)/volume_access.cft.yaml

deploy:
	aws cloudformation deploy \
		--stack-name $(STACK_NAME)-Foundational-$(PARAM_NAME_SUFFIX) \
		--template-file foundational.cft.yaml \
		--capabilities "CAPABILITY_NAMED_IAM" "CAPABILITY_AUTO_EXPAND" \
		--parameter-overrides \
			"NameSuffix=$(PARAM_NAME_SUFFIX)" \
			"ExternalID=$(PARAM_EXTERNAL_ID)" \
			"TrustedIdentity=$(PARAM_TRUSTED_IDENTITY)" \
			"IsOrganizational=$(PARAM_IS_ORGANIZATIONAL)" \
			"OrganizationalUnitIDs=$(PARAM_ORGANIZATIONAL_UNIT_IDS)"
	aws cloudformation deploy \
		--stack-name $(STACK_NAME)-LogIngestion-EventBridge-$(PARAM_NAME_SUFFIX) \
		--template-file log_ingestion.events.cft.yaml \
		--capabilities "CAPABILITY_NAMED_IAM" "CAPABILITY_AUTO_EXPAND" \
		--parameter-overrides \
			"NameSuffix=$(PARAM_NAME_SUFFIX)" \
			"ExternalID=$(PARAM_EXTERNAL_ID)" \
			"TrustedIdentity=$(PARAM_TRUSTED_IDENTITY)" \
			"Regions=$(PARAM_REGIONS)" \
			"TargetEventBusARN=$(PARAM_TARGET_EVENT_BUS_ARN)" \
			"IsOrganizational=$(PARAM_IS_ORGANIZATIONAL)" \
			"OrganizationalUnitIDs=$(PARAM_ORGANIZATIONAL_UNIT_IDS)"
	aws cloudformation deploy \
		--stack-name $(STACK_NAME)-LogIngestion-S3-$(PARAM_NAME_SUFFIX) \
		--template-file log_ingestion.s3.cft.yaml \
		--capabilities "CAPABILITY_NAMED_IAM" "CAPABILITY_AUTO_EXPAND" \
		--parameter-overrides \
			"NameSuffix=$(PARAM_NAME_SUFFIX)" \
			"ExternalID=$(PARAM_EXTERNAL_ID)" \
			"TrustedIdentity=$(PARAM_TRUSTED_IDENTITY)" \
			"BucketARN=$(PARAM_BUCKET_ARN)" \
			"IsOrganizational=$(PARAM_IS_ORGANIZATIONAL)" \
			"OrganizationalUnitIDs=$(PARAM_ORGANIZATIONAL_UNIT_IDS)"
	aws cloudformation deploy \
		--stack-name $(STACK_NAME)-VolumeAccess-$(PARAM_NAME_SUFFIX) \
		--template-file volume_access.cft.yaml \
		--capabilities "CAPABILITY_NAMED_IAM" "CAPABILITY_AUTO_EXPAND" \
		--parameter-overrides \
			"NameSuffix=$(PARAM_NAME_SUFFIX)" \
			"ExternalID=$(PARAM_EXTERNAL_ID)" \
			"TrustedIdentity=$(PARAM_TRUSTED_IDENTITY)" \
			"Regions=$(PARAM_REGIONS)" \
			"IsOrganizational=$(PARAM_IS_ORGANIZATIONAL)" \
			"OrganizationalUnitIDs=$(PARAM_ORGANIZATIONAL_UNIT_IDS)"

clean:
	aws cloudformation delete-stack --stack-name $(STACK_NAME)-Foundational-$(PARAM_NAME_SUFFIX)
	aws cloudformation delete-stack --stack-name $(STACK_NAME)-LogIngestion-EventBridge-$(PARAM_NAME_SUFFIX)
	aws cloudformation delete-stack --stack-name $(STACK_NAME)-LogIngestion-S3-$(PARAM_NAME_SUFFIX)
	aws cloudformation delete-stack --stack-name $(STACK_NAME)-VolumeAccess-$(PARAM_NAME_SUFFIX)


