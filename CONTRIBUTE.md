
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

