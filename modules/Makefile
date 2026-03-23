# requires AWS_PROFILE
# bucket must exist, prefix will be created
S3_BUCKET ?= "s4c-cft"
S3_PREFIX ?= "test"
S3_REGION ?= eu-west-1
RESPONSE_ACTIONS_TEMP_S3_PREFIX = modules/$(S3_PREFIX)/temp
RESPONSE_ACTIONS_TEMP_S3_URI = s3://$(S3_BUCKET)/$(RESPONSE_ACTIONS_TEMP_S3_PREFIX)/response_actions.cft.yaml
STACK_NAME = Sysdig-Secure
PARAM_NAME_SUFFIX ?= test
PARAM_IS_ORGANIZATIONAL ?= false
PARAM_EXTERNAL_ID ?= test
PARAM_TRUSTED_IDENTITY ?= arn:aws:iam:::role/$(PARAM_NAME_SUFFIX)
PARAM_API_KEY ?= <your_api_key>
PARAM_INGESTION_URL ?= https://app-staging.sysdigcloud.com/api/cloudingestion/webhooks/eventbridge/v1/64616366-3130-6163-3665-346636653537
PARAM_RATE_LIMIT ?= 300
PARAM_TARGET_EVENT_BUS_ARN ?= arn:aws:events:us-east-1::event-bus/default
PARAM_BUCKET_ARN ?= arn:aws:s3:::cloudtrail-$(PARAM_NAME_SUFFIX)
PARAM_REGIONS ?= us-east-1
PARAM_LAMBDA_SCANNING_ENABLED ?= true
PARAM_SCANNING_ACCOUNT_ID ?= 878070807337
PARAM_API_BASE_URL ?= https://app-staging.sysdigcloud.com
PARAM_LAMBDA_PACKAGES_BASE_URL ?= https://download.sysdig.com/cloud-response-actions
PARAM_RESPONSE_ACTIONS_VERSION ?= 1.0.0
PARAM_ENABLED_RESPONSE_ACTIONS ?= make_private,fetch_cloud_logs,create_volume_snapshot,quarantine_user
PARAM_RESPONSE_ACTIONS_PARTITION ?= aws

.PHONY: validate lint deploy test clean
validate: export AWS_PAGER=""
validate:
	aws --region us-east-1 cloudformation validate-template --template-body file://./foundational.cft.yaml
	aws --region us-east-1 cloudformation validate-template --template-body file://./log_ingestion.events.cft.yaml
	aws --region us-east-1 cloudformation validate-template --template-body file://./log_ingestion.legacy_events.cft.yaml
	aws --region us-east-1 cloudformation validate-template --template-body file://./log_ingestion.s3.cft.yaml
	aws --region us-east-1 cloudformation validate-template --template-body file://./volume_access.cft.yaml
	aws --region us-east-1 cloudformation validate-template --template-body file://./vm_workload_scanning.cft.yaml
	aws --region us-east-1 cloudformation validate-template --template-body file://./foundational_with_scanning.cft.yaml
	aws --region us-east-1 cloudformation validate-template --template-body file://./foundational_vm_workload_scanning.cft.yaml
	aws --region us-east-1 cloudformation validate-template --template-body file://./foundational_volume_access.cft.yaml
	@trap 'aws s3 rm $(RESPONSE_ACTIONS_TEMP_S3_URI) 2>/dev/null || true' EXIT; \
	aws s3 cp response_actions.cft.yaml $(RESPONSE_ACTIONS_TEMP_S3_URI) && \
	aws --region us-east-1 cloudformation validate-template --template-url `aws s3 presign $(RESPONSE_ACTIONS_TEMP_S3_URI) --region $(S3_REGION) --expires-in 60`

lint:
	cfn-lint *.cft.yaml
	yq '.Resources.OrganizationStackSet.Properties.TemplateBody' foundational.cft.yaml | cfn-lint -
	yq '.Resources.EventBridgeRuleStackSet.Properties.TemplateBody' log_ingestion.events.cft.yaml | cfn-lint -
	yq '.Resources.OrganizationRoleStackSet.Properties.TemplateBody' log_ingestion.events.cft.yaml | cfn-lint -
	yq '.Resources.OrganizationRuleStackSet.Properties.TemplateBody' log_ingestion.events.cft.yaml | cfn-lint -
	yq '.Resources.EventBridgeRuleStackSet.Properties.TemplateBody' log_ingestion.legacy_events.cft.yaml | cfn-lint -
	yq '.Resources.OrganizationRoleStackSet.Properties.TemplateBody' log_ingestion.legacy_events.cft.yaml | cfn-lint -
	yq '.Resources.OrganizationRuleStackSet.Properties.TemplateBody' log_ingestion.legacy_events.cft.yaml | cfn-lint -
	yq '.Resources.AccountStackSet.Properties.TemplateBody' volume_access.cft.yaml | cfn-lint -
	yq '.Resources.OrganizationStackSet.Properties.TemplateBody' volume_access.cft.yaml | cfn-lint -
	yq '.Resources.ScanningOrgStackSet.Properties.TemplateBody' vm_workload_scanning.cft.yaml | cfn-lint -
	yq '.Resources.LambdaFunctionsStackSet.Properties.TemplateBody' response_actions.cft.yaml | cfn-lint -
	yq '.Resources.OrganizationDelegateRolesStackSet.Properties.TemplateBody' response_actions.cft.yaml | cfn-lint -
	yq '.Resources.FoundationalOrganizationStackSet.Properties.TemplateBody' foundational_with_scanning.cft.yaml | cfn-lint -
	yq '.Resources.VMWorkloadScanningOrganizationStackSet.Properties.TemplateBody' foundational_with_scanning.cft.yaml | cfn-lint -
	yq '.Resources.AccountStackSet.Properties.TemplateBody' foundational_with_scanning.cft.yaml | cfn-lint -
	yq '.Resources.VolumeAccessOrganizationStackSet.Properties.TemplateBody' foundational_with_scanning.cft.yaml | cfn-lint -
	yq '.Resources.FoundationalOrganizationStackSet.Properties.TemplateBody' foundational_vm_workload_scanning.cft.yaml | cfn-lint -
	yq '.Resources.VMWorkloadScanningOrganizationStackSet.Properties.TemplateBody' foundational_vm_workload_scanning.cft.yaml | cfn-lint -
	yq '.Resources.FoundationalOrganizationStackSet.Properties.TemplateBody' foundational_volume_access.cft.yaml | cfn-lint -
	yq '.Resources.AccountStackSet.Properties.TemplateBody' foundational_volume_access.cft.yaml | cfn-lint -
	yq '.Resources.VolumeAccessOrganizationStackSet.Properties.TemplateBody' foundational_volume_access.cft.yaml | cfn-lint -

publish:
	aws s3 cp foundational.cft.yaml s3://$(S3_BUCKET)/modules/$(S3_PREFIX)/foundational.cft.yaml
	aws s3 cp log_ingestion.s3.cft.yaml s3://$(S3_BUCKET)/modules/$(S3_PREFIX)/log_ingestion.s3.cft.yaml
	aws s3 cp log_ingestion.events.cft.yaml s3://$(S3_BUCKET)/modules/$(S3_PREFIX)/log_ingestion.events.cft.yaml
	aws s3 cp log_ingestion.legacy_events.cft.yaml s3://$(S3_BUCKET)/modules/$(S3_PREFIX)/log_ingestion.legacy_events.cft.yaml
	aws s3 cp volume_access.cft.yaml s3://$(S3_BUCKET)/modules/$(S3_PREFIX)/volume_access.cft.yaml
	aws s3 cp vm_workload_scanning.cft.yaml s3://$(S3_BUCKET)/modules/$(S3_PREFIX)/vm_workload_scanning.cft.yaml
	aws s3 cp response_actions.cft.yaml s3://$(S3_BUCKET)/modules/$(S3_PREFIX)/response_actions.cft.yaml
	aws s3 cp foundational_with_scanning.cft.yaml s3://$(S3_BUCKET)/modules/$(S3_PREFIX)/foundational_with_scanning.cft.yaml
	aws s3 cp foundational_vm_workload_scanning.cft.yaml s3://$(S3_BUCKET)/modules/$(S3_PREFIX)/foundational_vm_workload_scanning.cft.yaml
	aws s3 cp foundational_volume_access.cft.yaml s3://$(S3_BUCKET)/modules/$(S3_PREFIX)/foundational_volume_access.cft.yaml

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
			"Partition=$(PARAM_PARTITION)" \
			"RootOUID=$(PARAM_ROOT_OU_ID)" \
			"IncludeOUIDs=$(PARAM_INCLUDE_OU_IDS)" \
			"IncludeAccounts=$(PARAM_INCLUDE_ACCOUNTS)" \
			"ExcludeAccounts=$(PARAM_EXCLUDE_ACCOUNTS)"
	aws cloudformation deploy \
		--stack-name $(STACK_NAME)-LogIngestion-EventBridge-$(PARAM_NAME_SUFFIX) \
		--template-file log_ingestion.events.cft.yaml \
		--capabilities "CAPABILITY_NAMED_IAM" "CAPABILITY_AUTO_EXPAND" \
		--parameter-overrides \
			"NameSuffix=$(PARAM_NAME_SUFFIX)" \
			"ExternalID=$(PARAM_EXTERNAL_ID)" \
			"TrustedIdentity=$(PARAM_TRUSTED_IDENTITY)" \
			"Regions=$(PARAM_REGIONS)" \
			"ApiKey=$(PARAM_API_KEY)" \
			"IngestionUrl=$(PARAM_INGESTION_URL)" \
			"RateLimit=$(PARAM_RATE_LIMIT)" \
			"IsOrganizational=$(PARAM_IS_ORGANIZATIONAL)" \
			"Partition=$(PARAM_PARTITION)" \
			"RootOUID=$(PARAM_ROOT_OU_ID)" \
			"IncludeOUIDs=$(PARAM_INCLUDE_OU_IDS)" \
			"IncludeAccounts=$(PARAM_INCLUDE_ACCOUNTS)" \
			"ExcludeAccounts=$(PARAM_EXCLUDE_ACCOUNTS)"
	aws cloudformation deploy \
		--stack-name $(STACK_NAME)-LogIngestion-LegacyEventBridge-$(PARAM_NAME_SUFFIX) \
		--template-file log_ingestion.legacy_events.cft.yaml \
		--capabilities "CAPABILITY_NAMED_IAM" "CAPABILITY_AUTO_EXPAND" \
		--parameter-overrides \
			"NameSuffix=$(PARAM_NAME_SUFFIX)" \
			"ExternalID=$(PARAM_EXTERNAL_ID)" \
			"TrustedIdentity=$(PARAM_TRUSTED_IDENTITY)" \
			"Regions=$(PARAM_REGIONS)" \
			"TargetEventBusARN=$(PARAM_TARGET_EVENT_BUS_ARN)" \
			"IsOrganizational=$(PARAM_IS_ORGANIZATIONAL)" \
			"Partition=$(PARAM_PARTITION)" \
			"RootOUID=$(PARAM_ROOT_OU_ID)" \
			"IncludeOUIDs=$(PARAM_INCLUDE_OU_IDS)" \
			"IncludeAccounts=$(PARAM_INCLUDE_ACCOUNTS)" \
			"ExcludeAccounts=$(PARAM_EXCLUDE_ACCOUNTS)"
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
			"RootOUID=$(PARAM_ROOT_OU_ID)" \
			"IncludeOUIDs=$(PARAM_INCLUDE_OU_IDS)" \
			"IncludeAccounts=$(PARAM_INCLUDE_ACCOUNTS)" \
			"ExcludeAccounts=$(PARAM_EXCLUDE_ACCOUNTS)"
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
			"RootOUID=$(PARAM_ROOT_OU_ID)" \
			"IncludeOUIDs=$(PARAM_INCLUDE_OU_IDS)" \
			"IncludeAccounts=$(PARAM_INCLUDE_ACCOUNTS)" \
			"ExcludeAccounts=$(PARAM_EXCLUDE_ACCOUNTS)"

	aws cloudformation deploy \
		--stack-name $(STACK_NAME)-VMWorkloadScanning-$(PARAM_NAME_SUFFIX) \
		--template-file vm_workload_scanning.cft.yaml \
		--capabilities "CAPABILITY_NAMED_IAM" "CAPABILITY_AUTO_EXPAND" \
		--parameter-overrides \
			"NameSuffix=$(PARAM_NAME_SUFFIX)" \
			"ExternalID=$(PARAM_EXTERNAL_ID)" \
			"TrustedIdentity=$(PARAM_TRUSTED_IDENTITY)" \
			"LambdaScanningEnabled"=$(PARAM_LAMBDA_SCANNING_ENABLED) \
			"IsOrganizational=$(PARAM_IS_ORGANIZATIONAL)" \
			"RootOUID=$(PARAM_ROOT_OU_ID)" \
			"IncludeOUIDs=$(PARAM_INCLUDE_OU_IDS)" \
			"IncludeAccounts=$(PARAM_INCLUDE_ACCOUNTS)" \
			"ExcludeAccounts=$(PARAM_EXCLUDE_ACCOUNTS)"
	
	aws cloudformation deploy \
		--stack-name $(STACK_NAME)-ResponseActions-$(PARAM_NAME_SUFFIX) \
		--template-file response_actions.cft.yaml \
		--s3-bucket $(S3_BUCKET) \
		--s3-prefix $(RESPONSE_ACTIONS_TEMP_S3_PREFIX) \
		--capabilities "CAPABILITY_NAMED_IAM" "CAPABILITY_AUTO_EXPAND" \
		--parameter-overrides \
			"NameSuffix=$(PARAM_NAME_SUFFIX)" \
			"ExternalID=$(PARAM_EXTERNAL_ID)" \
			"TrustedIdentity=$(PARAM_TRUSTED_IDENTITY)" \
			"ApiBaseUrl=$(PARAM_API_BASE_URL)" \
			"LambdaPackagesBaseUrl=$(PARAM_LAMBDA_PACKAGES_BASE_URL)" \
			"ResponseActionsVersion=$(PARAM_RESPONSE_ACTIONS_VERSION)" \
			"EnabledResponseActions=$(PARAM_ENABLED_RESPONSE_ACTIONS)" \
			"Regions=$(PARAM_REGIONS)" \
			"IsOrganizational=$(PARAM_IS_ORGANIZATIONAL)" \
			"Partition=$(PARAM_RESPONSE_ACTIONS_PARTITION)" \
			"RootOUID=$(PARAM_ROOT_OU_ID)" \
			"IncludeOUIDs=$(PARAM_INCLUDE_OU_IDS)" \
			"IncludeAccounts=$(PARAM_INCLUDE_ACCOUNTS)" \
			"ExcludeAccounts=$(PARAM_EXCLUDE_ACCOUNTS)"
	aws cloudformation deploy \
		--stack-name $(STACK_NAME)-FoundationalWithScanning-$(PARAM_NAME_SUFFIX) \
		--template-file foundational_with_scanning.cft.yaml \
		--capabilities "CAPABILITY_NAMED_IAM" "CAPABILITY_AUTO_EXPAND" \
		--parameter-overrides \
			"NameSuffix=$(PARAM_NAME_SUFFIX)" \
			"ExternalID=$(PARAM_EXTERNAL_ID)" \
			"TrustedIdentity=$(PARAM_TRUSTED_IDENTITY)" \
			"LambdaScanningEnabled=$(PARAM_LAMBDA_SCANNING_ENABLED)" \
			"ScanningAccountID=$(PARAM_SCANNING_ACCOUNT_ID)" \
			"Regions=$(PARAM_REGIONS)" \
			"IsOrganizational=$(PARAM_IS_ORGANIZATIONAL)" \
			"Partition=$(PARAM_PARTITION)" \
			"RootOUID=$(PARAM_ROOT_OU_ID)" \
			"IncludeOUIDs=$(PARAM_INCLUDE_OU_IDS)" \
			"IncludeAccounts=$(PARAM_INCLUDE_ACCOUNTS)" \
			"ExcludeAccounts=$(PARAM_EXCLUDE_ACCOUNTS)"
	aws cloudformation deploy \
		--stack-name $(STACK_NAME)-FoundationalVMWorkloadScanning-$(PARAM_NAME_SUFFIX) \
		--template-file foundational_vm_workload_scanning.cft.yaml \
		--capabilities "CAPABILITY_NAMED_IAM" "CAPABILITY_AUTO_EXPAND" \
		--parameter-overrides \
			"NameSuffix=$(PARAM_NAME_SUFFIX)" \
			"ExternalID=$(PARAM_EXTERNAL_ID)" \
			"TrustedIdentity=$(PARAM_TRUSTED_IDENTITY)" \
			"LambdaScanningEnabled=$(PARAM_LAMBDA_SCANNING_ENABLED)" \
			"IsOrganizational=$(PARAM_IS_ORGANIZATIONAL)" \
			"Partition=$(PARAM_PARTITION)" \
			"RootOUID=$(PARAM_ROOT_OU_ID)" \
			"IncludeOUIDs=$(PARAM_INCLUDE_OU_IDS)" \
			"IncludeAccounts=$(PARAM_INCLUDE_ACCOUNTS)" \
			"ExcludeAccounts=$(PARAM_EXCLUDE_ACCOUNTS)"
	aws cloudformation deploy \
		--stack-name $(STACK_NAME)-FoundationalVolumeAccess-$(PARAM_NAME_SUFFIX) \
		--template-file foundational_volume_access.cft.yaml \
		--capabilities "CAPABILITY_NAMED_IAM" "CAPABILITY_AUTO_EXPAND" \
		--parameter-overrides \
			"NameSuffix=$(PARAM_NAME_SUFFIX)" \
			"ExternalID=$(PARAM_EXTERNAL_ID)" \
			"TrustedIdentity=$(PARAM_TRUSTED_IDENTITY)" \
			"ScanningAccountID=$(PARAM_SCANNING_ACCOUNT_ID)" \
			"Regions=$(PARAM_REGIONS)" \
			"IsOrganizational=$(PARAM_IS_ORGANIZATIONAL)" \
			"Partition=$(PARAM_PARTITION)" \
			"RootOUID=$(PARAM_ROOT_OU_ID)" \
			"IncludeOUIDs=$(PARAM_INCLUDE_OU_IDS)" \
			"IncludeAccounts=$(PARAM_INCLUDE_ACCOUNTS)" \
			"ExcludeAccounts=$(PARAM_EXCLUDE_ACCOUNTS)"

clean:
	aws cloudformation delete-stack --stack-name $(STACK_NAME)-Foundational-$(PARAM_NAME_SUFFIX)
	aws cloudformation delete-stack --stack-name $(STACK_NAME)-LogIngestion-EventBridge-$(PARAM_NAME_SUFFIX)
	aws cloudformation delete-stack --stack-name $(STACK_NAME)-LogIngestion-LegacyEventBridge-$(PARAM_NAME_SUFFIX)
	aws cloudformation delete-stack --stack-name $(STACK_NAME)-LogIngestion-S3-$(PARAM_NAME_SUFFIX)
	aws cloudformation delete-stack --stack-name $(STACK_NAME)-VolumeAccess-$(PARAM_NAME_SUFFIX)
	aws cloudformation delete-stack --stack-name $(STACK_NAME)-VMWorkloadScanning-$(PARAM_NAME_SUFFIX)
	aws cloudformation delete-stack --stack-name $(STACK_NAME)-ResponseActions-$(PARAM_NAME_SUFFIX)
	aws cloudformation delete-stack --stack-name $(STACK_NAME)-FoundationalWithScanning-$(PARAM_NAME_SUFFIX)
	aws cloudformation delete-stack --stack-name $(STACK_NAME)-FoundationalVMWorkloadScanning-$(PARAM_NAME_SUFFIX)
	aws cloudformation delete-stack --stack-name $(STACK_NAME)-FoundationalVolumeAccess-$(PARAM_NAME_SUFFIX)
