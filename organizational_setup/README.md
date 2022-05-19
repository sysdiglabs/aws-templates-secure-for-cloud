# Secure for Cloud - Organizational

WIP.

<!-- 
    TODO, add diagram image 
-->

## Use-Case

- AWS Organization setup
- AWS Organizational Cloudtrail reporting to an S3 bucket in the management account


Sysdig Template will
- Create SysdigComplianceRole on all organization member accounts
- Create SysdigRole on management account to be able to read events from the cloudtrail
- WIP. Deploy Sysdig workload to ingest events from the cloudtrail
   

## Usage

This template is to be **deployed on an Organization Management account**

1. Before launching StackSet you will need a pre-provisioning on Sysdig Cloud
Review `./sysdig_provisioning.sh` and get `SysdigTrustedEntity` and `ExternalId` values for next step.

2. Launch StackSet

This will create two StackSets
 - Managemenet Sysdig Role preparation to be able to access Cloudtrail
[Cloudformation Stacksets](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/what-is-cfnstacksets.html) will be used
>  Using an administrator account, you define and manage an AWS CloudFormation template, and use the template as the basis for provisioning stacks into selected target accounts across specified AWS Regions.
- [Prerequisites for stack set operations](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/stacksets-prereqs.html)
