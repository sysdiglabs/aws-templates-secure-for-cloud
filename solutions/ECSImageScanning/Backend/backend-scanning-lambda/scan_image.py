import os

import boto3
import sdcclient


def handler(event, context):
    parameters = Parameters()

    scanning_client = sdcclient.SdScanningClient(
        token=parameters.secure_api_token(),
        sdc_url=parameters.secure_url()
    )

    return handler_with_client(event, context, scanning_client)


def handler_with_client(event, context, scanning_client):
    if event is not None and "detail" in event and "containers" in event["detail"]:
        images = (container["image"] for container in event["detail"]["containers"] if "image" in container)
        for image in images:
            ok, result = scanning_client.add_image(image, autosubscribe=False)
            if not ok:
                raise RuntimeError('Image cannot be analyzed from SasS backend. More details: {}'.format(result))


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
