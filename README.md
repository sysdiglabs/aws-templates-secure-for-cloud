# Sysdig Secure for Cloud in AWS - Cloudformation Template

This repository contains the CloudFormation templates to deploy the Sysdig
CloudVision suite in an AWS Account using ECS or AppRunner.

Deploy latest versions of Sysdig Secure for Cloud using one of the worklfows that most suit you:

- **[Op1) Template for ECS workload](https://console.aws.amazon.com/cloudformation/home#/stacks/quickCreate?stackName=Sysdig-CloudVision&templateURL=https://cf-templates-cloudvision-ci.s3-eu-west-1.amazonaws.com/ecs/latest/entry-point.yaml)**
- **[Op2) Tempalte for AppRunner workload](https://console.aws.amazon.com/cloudformation/home#/stacks/quickCreate?stackName=Sysdig-CloudVision&templateURL=https://cf-templates-cloudvision-ci.s3-eu-west-1.amazonaws.com/apprunner/latest/entry-point.yaml)**


If needed, we also have an <a href="https://github.com/sysdiglabs/terraform-aws-secure-for-cloud">Sysdig Secure for Cloud Terraform version</a>

--- 

## Contribute


### Release

Templates are [uploaded on the CI release cycle](https://github.com/sysdiglabs/aws-cloudvision-templates/blob/main/.github/workflows/release.yaml#L63) to `cf-templates-cloudvision-ci` on Sysdig `draios-demo` account.

Leading to the latest entry-point, which will be used on the Sysdig Secure > Getting Started > AWS Cloudformation
<br/>`https://cf-templates-cloudvision-ci.s3-eu-west-1.amazonaws.com/master/entry-point.yaml`


### Pull Request

When the PR is drafted, a new template will be available for testing:  
- For AppRunner
<br/>`https://cf-templates-cloudvision-ci.s3-eu-west-1.amazonaws.com/apprunner/pr/<PR_NAME>/entry-point.yaml`
- For ECS
<br/>`https://cf-templates-cloudvision-ci.s3-eu-west-1.amazonaws.com/ecs/pr/<PR_NAME>/entry-point.yaml`


### Testing

see [Makefile](templates_ecs/Makefile)

- **Validation**

  ```bash
  $ aws cloudformation validate-template --template-body file://./templates/CloudVision.yaml
  ```

- **Launch** Template

  full cycle
  
  ```
  -- test
  $ aws cloudformation delete-stack --stack-name test ; \
  sleep 10 ; \
  aws cloudformation deploy --template-file templates/CloudVision.yaml --stack-name test ; \
  aws cloudformation describe-stack-events --stack-name test
  ```

- Test **Template wizard** (UI)
  ```
  Aws console > cloudformation > create new stack (template, upload template: select ./templates/Cloudvision.yaml)
  ```
  - note: this will upload the template into an s3 bucket, remember to delete it afterwards 


- **Cleanup** <br/>Delete stack to clean test environment. [CFT limitation does not allow to automatically delete non-empty S3 bucket](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-bucket.html), so Stack deletion will fail when you request it. Delete S3 bucket manually and relaunch deletion for a full cleanup.

