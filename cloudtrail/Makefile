.PHONY: validate lint

all: validate lint

validate:
	aws cloudformation validate-template --template-body file://./cloudtrail.yaml

lint:
	cfn-lint *.yaml

test:
	aws cloudformation deploy \
		--stack-name "CloudVision-CloudTrail-Test" \
		--template-file cloudtrail.yaml \
		--capabilities "CAPABILITY_NAMED_IAM" "CAPABILITY_AUTO_EXPAND"

clean:
	aws cloudformation delete-stack --stack-name "CloudVision-CloudTrail-Test"
