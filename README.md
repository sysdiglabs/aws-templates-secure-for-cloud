# Sysdig CloudVision for AWS

This repository contains the CloudFormation templates to deploy the Sysdig
CloudVision suite in an AWS Account.

## Multi Account mode
The CFT is split into several pieces to ease multi-account deployment:

* **cloudtrail**: to be deployed in all the monitored accounts. Can reuse an existing CloudTrail SNS topic (only SQS queue and subscription is created) or create a new Trail, Bucket, SNS Topic, and SQS queue.
* **cloudvision-childaccount**: to be deployed in all the monitored accounts. This CFT creates the roles and trust policies in the child accounts so CloudConnector, CloudScanning and CloudBench, which will run only in the main account, can assume the roles, acquire the permissions, and perform the required actions in the child accounts. The main account ID is provided as a parameter (required to create the role trust policies).
* **cloudvision-mainaccount**: to be deployed in one main account. It creates the S3 config bucket, ECS cluster, and executes the CloudConnector, CloudBench, and CloudScanning tasks.
When deploying the main CFT, there are two new mandatory parameters:
  * Trail account list: a list of accounts and regions where the trails (the SQS queues) are deployed. CloudConnector and CloudScanning will consume the events from these trails.
  * Bench account list: a list of accounts and regions where the benchmarks should run.
If the accounts list parameter is empty, the components deploy using the "single account" mode. When running in single-account mode, the ECS tasks roles include all the required permissions for the executing account. When running in multi-account mode, the ECS tasks roles include AssumeRole permissions, so they assume the roles in the child accounts and execute the required actions in the child accounts.

There is another important parameter, the **NamingPrefix**, shared by all CFTs. All the roles, SQS queues, ... are created using a naming convention and the `${NamingPrefix}-` prefix. It allows wiring all the pieces together (so the main account knows the name of the child accounts roles to assume, the name of the SQS queues, ...). The default parameter value `SysdigCloud` should be safe, but it can be adjusted to prevent a collision if you need to deploy multiple instances of the CFTs in the same account. When changing the **NamingPrefix** from the default value, the parameter value must be the same in all the CFTs to match the resource names.

## Single Account mode
The **cloudvision-singleaccount** folder contains a CFT that deploys a single-account version reusing the multi-account components.

The multi-account CFTs work for single-account scenarios, by deploying the 3 CFTs. But this is not optimal, as it is not necessary to use the AssumeRole mechanism when scraping trail events and executing benchmarks in one single account.

In order to address this minor issue, the **cloudvision-mainaccount** CFT can take an empty list of child accounts, and directly add the permissions to the ECS Task Role and configure the CloudConnector, CloudScanning, and CloudBench to use these permissions instead of the AssumeRole mechanism (this is the old known single-account mode we were using up to now).

To make deployment easier, the **cloudvision-singleaccount** folder CFT mimics the old templates/CloudVision.yaml behavior and parameters, but deploy reusing the new CFT pieces.

Pros: we still support the optimal single-account execution mode, without AssumeRole, while providing a single CFT for single-account scenarios, but maintaining only a set of CFTs, instead of a single-account version and a multi-account version, which share most of the resources.


[Deploy latest version!](https://console.aws.amazon.com/cloudformation/home#/stacks/quickCreate?stackName=Sysdig-CloudVision&templateURL=https://cf-templates-cloudvision-ci.s3-eu-west-1.amazonaws.com/master/entry-point.yaml)
