# requires AWS_PROFILE
# bucket must exist, prefix will be created
S3_BUCKET ?= "s4c-cft"
S3_PREFIX ?= "test"
# We need the REGION or the TemplateURLs might be created for a different region, resulting in a deployment error
S3_REGION ?= "eu-west-1" # ireland
SECURE_API_TOKEN ?= ""
STACK_NAME = "Sysdig-Secure-$(PARAM_NAME_SUFFIX)"
PARAM_NAME_SUFFIX ?= "test"
PARAM_IS_ORGANIZATIONAL ?= "false"

.PHONY: validate lint deploy test clean
validate:
	aws cloudformation validate-template --template-body file://./template.yaml

lint:
	cfn-lint *.yaml
	yq '.Resources.OrganizationRoleStackSet.Properties.TemplateBody' template.yaml | cfn-lint -
	yq '.Resources.ScanningKmsKeyStackSet.Properties.TemplateBody' template.yaml | cfn-lint -
	yq '.Resources.OrganizationKMSKeyStackSet.Properties.TemplateBody' template.yaml | cfn-lint -

publish:
	aws s3 cp ./template.yaml s3://$(S3_BUCKET)/modules/volume_access/$(S3_PREFIX)/template.yaml

deploy:
	aws cloudformation deploy \
		--stack-name $(STACK_NAME) \
		--template-file template.yaml \
		--capabilities "CAPABILITY_NAMED_IAM" "CAPABILITY_AUTO_EXPAND" \
		--parameter-overrides \
			"NameSuffix=$(PARAM_NAME_SUFFIX)" \
			"ExternalID=$(PARAM_EXTERNAL_ID)" \
			"TrustedIdentity=$(PARAM_TRUSTED_IDENTITY)" \
			"IsOrganizational=$(PARAM_IS_ORGANIZATIONAL)" \
			"OrganizationUnitIDs=$(PARAM_ORGANIZATION_UNIT_IDS)"

clean:
	aws cloudformation delete-stack --stack-name $(STACK_NAME)

	