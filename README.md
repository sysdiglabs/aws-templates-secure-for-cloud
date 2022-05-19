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

No official templates available yet.

Find some [organizational use-case](./use_cases/org-k8s) as reference and contact us for support.

---
## Authors

Module is maintained and supported by [Sysdig](https://sysdig.com).

## License

Apache 2 Licensed. See LICENSE for full details.
