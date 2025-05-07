# Sysdig Secure - Modular Templates

Modular templates support cross sections of Sysdig Secure feature sets. Each template is intended to be installable alongside one another, and amongst multiple instances. 

## Common parameters

* `NameSuffix` - a unique string suffix given to named resources where applicable.
* `TrustedIdentity` - a Sysdig owned identity trusted to assume a permission limited customer installed role
* `ExternalID` - a Sysdig assigned value

## Organizations

Organizations are supported by setting the following template parameters
* `IsOrganizational=true`
* `OrganizationalUnitIDs=ou-...` (to be deprecated on 30th November, 2025, please read below)

### Organizational Install Configurations

Following are the new parameters to configure organizational deployments on the cloud for Sysdig Secure for Cloud :-
1. `RootOUID` - Root Organization Unit ID
2. `IncludeOUIDs` - List of AWS Organizational Unit IDs to deploy the Sysdig Secure for Cloud resources in.
3. `IncludeAccounts` - List of AWS Accounts to deploy the Sysdig Secure for Cloud resources in.
4. `ExcludeAccounts` - List of AWS Accounts to exclude deploying the Sysdig Secure for Cloud resources in.

**WARNING**: module template parameter `OrganizationalUnitIDs` will be DEPRECATED on 30th November, 2025. Please work with Sysdig to migrate your CFT based installs to use `IncludeOUIDs` instead to achieve the same deployment outcome.
