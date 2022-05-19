# Secure for Cloud - Organizational

## Use-Case explanation

**Current User Setup**

- AWS Organization setup
- AWS Organizational Cloudtrail with a managed account level SNS activated + reporting to an S3 bucket
- K8s workload available to re-use for workload deployment
- Permission provisioning will be performed manually

**Sysdig Secure for Cloud [Features](https://docs.sysdig.com/en/docs/installation/sysdig-secure-for-cloud/)**

- Thread-Detection
- Posture; Compliance + Identity Access Management

## Suggested building-blocks

1. Sysdig Cloud Compliance backend provisioning will be performed manually

Following resources will be provisioned
- each member cloud-account from the organization, where compliance is wanted to be checked
- a Task that will run "aws_foundations_bench-1.3.0" schema on previously defined accounts

This step can be performed at the end too, but you will need Sysdig `TrustIdentity` and `ExternalId` for role AWS SysdigCompliance role provisioning.

Find [sysdig_cloud_compliance_provisioning.sh](../../utils/sysdig_cloud_compliance_provisioning.sh)

2. Compute Workload deployment in K8s

We will make use of the [Sysdig cloud-connector helm chart](https://charts.sysdig.com/charts/cloud-connector/) component.

We will also need to create a SQS to be able to ingest the events of the cloudtrail-sns.
// TODO provide a way to create this sqs?
// TODO check deployment auth

With the following values
```helm
-- values.yaml suggestion
sysdig:
  url: "https://secure.sysdig.com"
  secureAPIToken: "SYSDIG_API_TOKEN"
  
ingestors:
    - cloudtrail-sns-sqs: 
        queueURL = "SNS_SUBSCRIBED_SQS_URL"        
```

3. Permissions setup - Compliance Role

On each member-account where Compliance wants to be checked (see step 1), we need to provide a role for Sysdig to be able to impersonate and
perform `SecurityAudit` tasks.

Find the following [Sysdig Compliance IAM policy](../../general_templates/ComplianceAgentlessRole.yaml) as guidance to create these roles.


4. Permissions setup - K8s Compute Role 

For Sysdig Compute workload to be able to ingest Cloudtrail events (consume S3 and process SQS), a role must be provisioned in the management account,
to enable Sysdig to read these S3 bucket events.

Find following [Sysdig Organizational Management Account Role](./OrgManagementAccountSysdigRole.yaml) as guidance to create this role.

// TODO SQS handling