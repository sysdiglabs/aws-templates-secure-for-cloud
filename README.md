# Sysdig Secure for Cloud in AWS - Cloudformation Templates

This repository contains the CloudFormation templates to deploy [Sysdig Secure for Cloud](https://docs.sysdig.com/en/docs/sysdig-secure/sysdig-secure-for-cloud/)
suite.

## UseCases

If you're unsure about what/how to use this module, please fill the [questionnaire](https://github.com/sysdiglabs/terraform-aws-secure-for-cloud/blob/master/use-cases/_questionnaire.md) report as an issue and let us know your context, we will be happy to help and improve our module.

### Single-Account

Deploy the latest versions using one of the workloads that most suit you:

#### ECS-based workload

[Template for ECS workload](https://console.aws.amazon.com/cloudformation/home#/stacks/quickCreate?stackName=Sysdig-CloudVision&templateURL=https://cf-templates-cloudvision-ci.s3-eu-west-1.amazonaws.com/ecs/latest/entry-point.yaml)
 
![single-account diagram](https://raw.githubusercontent.com/sysdiglabs/terraform-aws-secure-for-cloud/master/examples/single-account-ecs/diagram-single.png)


#### AppRunner-based workload

Less resource-demanding and economic deployment (ECS requires VPCs and Gateways), but Apprunner is not available on all regions yet

[Template for AppRunner workload](https://console.aws.amazon.com/cloudformation/home#/stacks/quickCreate?stackName=Sysdig-CloudVision&templateURL=https://cf-templates-cloudvision-ci.s3-eu-west-1.amazonaws.com/apprunner/latest/entry-point.yaml)

![single-account diagram on apprunner](https://raw.githubusercontent.com/sysdiglabs/terraform-aws-secure-for-cloud/master/examples/single-account-apprunner/diagram-single.png)


If needed, we also have an <a href="https://github.com/sysdiglabs/terraform-aws-secure-for-cloud">Sysdig Secure for Cloud Terraform version</a>


## Organizational

WIP.

--- 

## Contribute

### Release

Templates are [uploaded on the CI release cycle](https://github.com/sysdiglabs/aws-cloudvision-templates/blob/main/.github/workflows/release.yaml#L63) to `cf-templates-cloudvision-ci` on Sysdig `draios-demo` account.

Leading to the latest entry-point, which will be used on the Sysdig Secure > Getting Started > AWS Cloudformation
<br/>`https://cf-templates-cloudvision-ci.s3-eu-west-1.amazonaws.com/master/entry-point.yaml`


### Pull Request

When the PR is drafted, a new template will be available for testing:  
- For ECS
  <br/>`https://cf-templates-cloudvision-ci.s3-eu-west-1.amazonaws.com/ecs/pr/<PR_NAME>/entry-point.yaml`
- For AppRunner
  <br/>`https://cf-templates-cloudvision-ci.s3-eu-west-1.amazonaws.com/apprunner/pr/<PR_NAME>/entry-point.yaml`


### Testing

see [Makefile](templates_ecs/Makefile)

#### Validation

ECS:

```bash
$ aws cloudformation validate-template --template-body file://./templates_ecs/CloudVision.yaml
```

AppRunner:

```bash
$ aws cloudformation validate-template --template-body file://./templates_apprunner/SecureForCloudAppRunner.yaml
```

#### Launch Template

ECS full cycle:

```
-- test
$ aws cloudformation delete-stack --stack-name test ; \
sleep 10 ; \
aws cloudformation deploy --template-file templates_ecs/CloudVision.yaml --stack-name test ; \
aws cloudformation describe-stack-events --stack-name test
```

AppRunner full cycle:

```
-- test
$ aws cloudformation delete-stack --stack-name test ; \
sleep 10 ; \
aws cloudformation deploy --template-file templates_apprunner/SecureForCloudAppRunner.yaml --stack-name test ; \
aws cloudformation describe-stack-events --stack-name test
```

#### Test Template wizard (UI)
  ```
  Aws console > cloudformation > create new stack (template, upload template: select ./templates/Cloudvision.yaml)
  ```
  - note: this will upload the template into an s3 bucket, remember to delete it afterwards 


#### Cleanup

Delete stack to clean test environment. [CFT limitation does not allow to automatically delete non-empty S3 bucket](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-bucket.html), so Stack deletion will fail when you request it. Delete S3 bucket manually and relaunch deletion for a full cleanup.

