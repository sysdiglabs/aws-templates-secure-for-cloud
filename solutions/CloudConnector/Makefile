VPC=""
PUBLICSUBNETS=""
PRIVATESUBNETS=""
CLUSTER=""

validate:
	aws cloudformation validate-template --template-body file://./CloudConnector.yaml
	aws cloudformation validate-template --template-body file://./CloudTrail.yaml

packaged-template.yaml: CloudConnector.yaml CloudTrail.yaml
	aws cloudformation package \
		--template-file CloudConnector.yaml \
		--s3-bucket nestor-test-cf \
		--output-template-file packaged-template.yaml

test: packaged-template.yaml
	aws cloudformation deploy \
		--stack-name "CloudConnectorTest" \
		--template-file packaged-template.yaml \
		--capabilities "CAPABILITY_NAMED_IAM"  \
		--parameter-overrides \
			"VPC=$(VPC)" \
			"PublicSubnets=$(PUBLICSUBNETS)" \
			"PrivateSubnets=$(PRIVATESUBNETS)" \
			"ECSCluster=$(CLUSTER)"
clean:
	aws cloudformation delete-stack --stack-name "CloudConnectorTest"
