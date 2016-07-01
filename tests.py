import os

import requests

from unittest import TestCase


from s3sign import S3BaseSigner, S3GETSigner, S3PUTSigner, S3PUTPublicSigner


class S3SignTestCase(TestCase):
    def test_get_put_signature(self):
        file_name = 'tos3.png'
        mime_type = 'image/png'
        valid = 60  # seconds
        # S3_NAME, AWS_ACCESS_KEY, AWS_SECRET_KEY can be set as environment
        # variables or passed as keyword arguments
        signer = S3PUTSigner()

        # Get the signature
        put_signature = signer.get_signed_url(file_name, mime_type, valid)

        # Use the signature to upload a file
        url = put_signature['signed_url']
        headers = put_signature['headers']
        with open(file_name, 'rb') as tos3:
            content = tos3.read()

        # PUT the object
        response = requests.put(url, data=content, headers=headers)

        self.assertEqual(response.status_code, 200)

        # Test S3GETSigner
        # I'm not doing this test in a different method because it
        # requires the an existing object in the bucket
        url = put_signature['url']

        signer = S3GETSigner()

        # GET a file
        signed_url = signer.get_signed_url(url, valid)
        response = requests.get(signed_url)

        self.assertEqual(response.status_code, 200)

    def test_get_put_signature__public(self):
        file_name = 'tos3.png'
        valid = 60  # seconds
        signer = S3PUTPublicSigner()

        mime_type = 'image/png'
        put_signature = signer.get_signed_url(file_name, mime_type, valid)

        url = put_signature['signed_url']
        headers = put_signature['headers']
        with open(file_name, 'rb') as tos3:
            content = tos3.read()

        response = requests.put(url, data=content, headers=headers)

        self.assertEqual(response.status_code, 200)

        url = put_signature['url']

        response = requests.get(url)

        self.assertEqual(response.status_code, 200)

    def test_get_secret_key_form_environment(self):
        original = os.environ.get('AWS_SECRET_KEY', '')
        os.environ['AWS_SECRET_KEY'] = 'a-secret'

        bucket_name = 'a-bucket'

        S3BaseSigner(s3_bucket=bucket_name, aws_access_key='a-key')

        os.environ['AWS_SECRET_KEY'] = original

    def test_get_access_key_form_environment(self):
        original = os.environ.get('AWS_ACCESS_KEY', '')
        os.environ['AWS_ACCESS_KEY'] = 'a-secret'

        bucket_name = 'a-bucket'

        S3BaseSigner(s3_bucket=bucket_name, aws_secret_key='a-secret')

        os.environ['AWS_ACCESS_KEY'] = original

    def test_get_bucket_name_form_environment(self):
        original = os.environ.get('S3_BUCKET', '')

        os.environ['S3_BUCKET'] = 'a-bucket'

        S3BaseSigner(aws_secret_key='a-secret', aws_access_key='a-key')

        os.environ['S3_BUCKET'] = original
