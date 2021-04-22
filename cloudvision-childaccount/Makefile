.PHONY: validate lint

all: validate lint

validate:
	aws cloudformation validate-template --template-body file://./cloudvision-childaccount.yaml

lint:
	cfn-lint *.yaml

test:
	aws cloudformation deploy \
		--stack-name "CloudVision-ChildAccount-Test" \
		--template-file cloudvision-childaccount.yaml \
		--capabilities "CAPABILITY_NAMED_IAM" "CAPABILITY_AUTO_EXPAND"

clean:
	aws cloudformation delete-stack --stack-name "CloudVision-ChildAccount-Test"
