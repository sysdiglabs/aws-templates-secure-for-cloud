import os
from mamba import description, it
from expects import expect, be_true

from scan_image import handler
import sdcclient

with description('Backend Scanning from ECR') as self:
    with context('when receiving an event from ECR'):
        with before.each:
            self.scanning_client = sdcclient.SdScanningClient(os.getenv("SECURE_API_TOKEN"))

        with it('creates the registry specified in event in Secure'):
            registry = '845151661675.dkr.ecr.eu-west-1.amazonaws.com'

            handler(self.ecr_push_event(), None)

            expect(self.scanning_client.get_registry(registry)[0]).to(be_true)

        with it('scans the image specified in the event'):
            image = '845151661675.dkr.ecr.eu-west-1.amazonaws.com/ecr-trigger:latest'

            handler(self.ecr_push_event(), None)

            expect(self.scanning_client.get_image(image)[0]).to(be_true)

    def ecr_push_event(self):
        return {
            'version': '0',
            'id': 'b7cecd64-2516-2f04-57bb-7ab31e446733',
            'detail-type': 'ECR Image Action',
            'source': 'aws.ecr',
            'account': '845151661675',
            'time': '2020-03-26T18:06:24Z',
            'region': 'eu-west-1',
            'resources': [],
            'detail': {
                'result': 'FAILURE',
                'repository-name': 'ecr-trigger',
                'image-digest': '',
                'action-type': 'PUSH',
                'image-tag': 'latest'
            }
        }
