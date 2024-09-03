# Sysdig Secure - Modular Templates

Modular templates support cross sections of Sysdig Secure feature sets. Each template is intended to be installable alongside one another, and amongst multiple instances. 

## Common parameters

* `NameSuffix` - a unique string suffix given to named resources where applicable.
* `TrustedIdentity` - a Sysdig owned identity trusted to assume a permission limited customer installed role
* `ExternalID` - a Sysdig assigned value

## Organizations

Organizations are supported by setting the following template parameters
* `IsOrganizational=true`
* `OrganizationalUnitIDs=ou-...`
