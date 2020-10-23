import os

import boto3
import sdcclient


def handler(event, context):
    parameters = Parameters()

    scanning_client = sdcclient.SdScanningClient(
        token=parameters.secure_api_token(),
        sdc_url=parameters.secure_url()
    )

    ok, result = scanning_client.add_registry(_registry(event),
                                              parameters.access_key_id(),
                                              parameters.secret_access_key(),
                                              registry_type='awsecr')

    if not ok and result != 'registry already exists in DB':
        raise RuntimeError(
            'Cannot set up a registry in Secure with credentials provided. ' +
            'More details: {}'.format(result)
        )
    ok, result = scanning_client.add_image(_image(event), autosubscribe=False)

    if not ok:
        raise RuntimeError(
            'Image cannot be analyzed from SasS backend. More details: {}'.
            format(result)
        )


class Parameters:
    def __init__(self):
        self._ssm_client = boto3.client('ssm')

    def secure_api_token(self):
        return self._value_from_env_or_ssm('SECURE_API_TOKEN',
                                           'SysdigSecureAPIToken')

    def _value_from_env_or_ssm(self, environment_variable, parameter):
        if environment_variable in os.environ:
            return os.getenv(environment_variable)

        return self._ssm_client.get_parameter(
            Name=parameter)['Parameter']['Value']

    def secure_url(self):
        return self._value_from_env_or_ssm('SECURE_URL',
                                           'SysdigSecureEndpoint')

    def access_key_id(self):
        return self._value_from_env_or_ssm('SCAN_AWS_ACCESS_KEY_ID',
                                           'ScanningUserAccessKeyId')

    def secret_access_key(self):
        return self._value_from_env_or_ssm('SCAN_AWS_SECRET_ACCESS_KEY',
                                           'ScanningUserSecretAccessKey')


def _registry(event):
    return "{account}.dkr.ecr.{region}.amazonaws.com".format(**event)


def _image(event):
    return "{account}.dkr.ecr.{region}.amazonaws.com/{repository_name}:{tag}".\
        format(
            repository_name=event['detail']['repository-name'],
            tag=event['detail']['image-tag'],
            **event
        )
