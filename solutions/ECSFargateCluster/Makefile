validate:
	aws cloudformation validate-template --template-body file://./VPC.yaml
	aws cloudformation validate-template --template-body file://./ECSFargateCluster.yaml

packaged-template.yaml: ECSFargateCluster.yaml VPC.yaml
	aws cloudformation package \
		--template-file ECSFargateCluster.yaml \
		--s3-bucket nestor-test-cf \
		--output-template-file packaged-template.yaml

test: packaged-template.yaml
	aws cloudformation deploy \
		--stack-name "ECSFargateClusterTest" \
		--template-body file://./packaged-template.yaml \
		--capabilities "CAPABILITY_NAMED_IAM"

clean:
	aws cloudformation delete-stack --stack-name "ECSFargateClusterTest"
	rm packaged-template.yaml
