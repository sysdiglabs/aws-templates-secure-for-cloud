VPC=""
PUBLICSUBNETS=""
PRIVATESUBNETS=""
CLUSTER=""

validate:
	aws cloudformation validate-template --template-body file://./CloudBench.yaml

packaged-template.yaml: CloudBench.yaml
	aws cloudformation package \
		--template-file CloudBench.yaml \
		--s3-bucket nestor-test-cf \
		--output-template-file packaged-template.yaml

test: packaged-template.yaml
	aws cloudformation deploy \
		--stack-name "CloudBenchTest" \
		--template-file packaged-template.yaml \
		--capabilities "CAPABILITY_NAMED_IAM"  \
		--parameter-overrides \
			"VPC=$(VPC)" \
			"PublicSubnets=$(PUBLICSUBNETS)" \
			"PrivateSubnets=$(PRIVATESUBNETS)" \
			"ECSCluster=$(CLUSTER)" \
			"SysdigSecureAPIToken=$(SECURE_API_TOKEN)" \
			"SysdigSecureEndpoint=$(SECURE_URL)"
clean:
	aws cloudformation delete-stack --stack-name "CloudBenchTest"
