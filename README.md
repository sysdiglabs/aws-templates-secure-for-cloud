# Sysdig CloudVision for AWS

This repository contains the CloudFormation templates to deploy the Sysdig
CloudVision suite in an AWS Account.


[Deploy latest version!](https://console.aws.amazon.com/cloudformation/home#/stacks/quickCreate?stackName=Sysdig-CloudVision&templateURL=https://cf-templates-cloudvision-ci.s3-eu-west-1.amazonaws.com/master/entry-point.yaml)


## Multi Account mode

The CFT is split into several pieces to ease multi-account deployment:

* **cloudtrail**: to be deployed in all the monitored accounts. Can reuse an existing CloudTrail SNS topic (only SQS queue and subscription is created) or create a new Trail, Bucket, SNS Topic, and SQS queue.
* **cloudvision-childaccount**: to be deployed in all the monitored accounts. This CFT creates the roles and trust policies in the child accounts so CloudConnector, CloudScanning and CloudBench, which will run only in the main account, can assume the roles, acquire the permissions, and perform the required actions in the child accounts. The main account ID is provided as a parameter (required to create the role trust policies).
* **cloudvision-mainaccount**: to be deployed in one main account. It creates the S3 config bucket, ECS cluster, and executes the CloudConnector, CloudBench, and CloudScanning tasks.
When deploying the main CFT, there are two new mandatory parameters:
  * Trail account list: a list of accounts and regions where the trails (the SQS queues) are deployed. CloudConnector and CloudScanning will consume the events from these trails.
  * Bench account list: a list of accounts where the benchmarks should run.

If the accounts list parameter is empty, the components deploy using the "single account" mode. When running in single-account mode, the ECS tasks roles include all the required permissions for the executing account. When running in multi-account mode, the ECS tasks roles include AssumeRole permissions, so they assume the roles in the child accounts and execute the required actions in the child accounts.

There is another important parameter, the **NamingPrefix**, shared by all CFTs. All the roles, SQS queues, ... are created using a naming convention and the `${NamingPrefix}-` prefix. It allows wiring all the pieces together (so the main account knows the name of the child accounts roles to assume, the name of the SQS queues, ...). The default parameter value `SysdigCloud` should be safe, but it can be adjusted to prevent a collision if you need to deploy multiple instances of the CFTs in the same account. When changing the **NamingPrefix** from the default value, the parameter value must be the same in all the CFTs to match the resource names.

## Common scenarios

### Single Account mode

The **cloudvision-singleaccount** folder contains a CFT that deploys a single-account version reusing the multi-account components.

#### Explanation

The multi-account CFTs work for single-account scenarios, by deploying the 3 CFTs. But this is not optimal, as it is not necessary to use the AssumeRole mechanism when scraping trail events and executing benchmarks in one single account.

In order to address this minor issue, the **cloudvision-mainaccount** CFT can take an empty list of child accounts, and directly add the permissions to the ECS Task Role and configure the CloudConnector, CloudScanning, and CloudBench to use these permissions instead of the AssumeRole mechanism (this is the old known single-account mode we were using up to now).

To make deployment easier, the **cloudvision-singleaccount** folder CFT mimics the old templates/CloudVision.yaml behavior and parameters, but deploy reusing the new CFT pieces.

Pros: we still support the optimal single-account execution mode, without AssumeRole, while providing a single CFT for single-account scenarios, but maintaining only a set of CFTs, instead of a single-account version and a multi-account version, which share most of the resources.

#### Requirements

...

#### Prepare

...

#### Install

...

### AWS Organizations

The **cloudvision-organizations** folder contains a CFT that can be used to deploy in the organization main or audit account.

This CFT will deploy the CloudVision components and connect to the existing organization CloudTrail SNS topic.

You will still need to deploy the **cloudvision-childaccount** CFT on every child account to support scanning and benchmarking (not required for cloud connector).

#### Requirements

* AWS Organization
* Existing Organizational CloudTrail with SNS topic
* Must deploy on the same region where the Organization CloudTrail is created

#### Prepare

* The **main** account is the acount where Organization CloudTrail is publishing logs. It can be the organization master account, or an special Audit account. We will use **main** acount to refer to it. You will need the account ID.
* Child accounts are all the accounts, belonging to the organization, where you will be consuming CloudTrail events from. Make a list of the child account IDs.

#### Install

* Deploy **cloudvision-childaccount** CFT on every child account in the organization where you want CloudScanning to scan images, and CloudBench to execute benchmarks. This includes the main account too.
  - You will need to provide the **main** account ID as a parameter
  - The CFT can be deployed manually
  - You can use StackSet service to deploy in all accounts at once
* Deploy **cloudvision-organization** CFT on the **main** account.
  - You need to provide the ARN of the existing CloudTrail SNS Topic
  - You need to provide a comma separated list of the child accounts ID, like `account1,account2,...`

### Independent accounts

Use case: multiple accounts that don't belong to an organization.

#### Prepare

* The **main** account is the account where the CloudVision components will be running
*  The **child** accounts are every account that are going to be monitored by CloudVision (this usually includes the **main** account itself.)

#### Install

* Deploy the **cloudtrail** CFT on every **child** account, either creating a new CloudTrail in the account, or provide the ARN of existing SNS topic in case a CloudTrail already exists.
* Deploy the **cloudvision-childaccount** CFT on every **child** account.
  - You need to provide the **main** account ID as a parameter
* Deploy **cloudvision-mainaccount** CFT on the **main** account.
  - You need to provide a comma separated list of the child account IDs and regions (the region where the CloudTrail is deployed in that account), and a list of child accounts (without regions) where CloudBench will execute the benchmarks.

### Hybrid environments

Mixed use-cases, where you need to monitor several individual accounts along with some accounts belonging to one or more organizations.

Using the **cloudtrail**, **cloudvision-childaccount** and **cloudvision-mainaccount** it is possible to cover all cases.

* Deploy **cloudtrail** CFT in the accounts where you either need to create a CloudTrail, or use an existing one via the SNS topic. This includes the Organizational CloudTrails.
* Deploy **cloudvision-childaccount** on *every* account to monitor, including the **main** account.
* Deploy **cloudvision-mainaccount** on the **main** account.
  - Provide a comma separated list of the child account IDs and regions (the region where the CloudTrail is deployed in that account), and a list of child accounts (without regions) where CloudBench will execute the benchmarks.
  - Please note, for the list of child **account IDs and regions*+ (`TrailAccountsAndRegionsList` parameter), you only need to provide the accounts where a ClodTrail exists. You must include every individual account not in an organization, and for organizations, you only need to include the Organization CloudTrail account.
  - For the list of `BenchAccountsList`, you need to include every account where the benchmarks should be executed.

