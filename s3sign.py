import base64
import hmac
import os
import time
import urllib.parse
from hashlib import sha1


class S3BaseSigner:
    signed_url = '{}?AWSAccessKeyId={}&Expires={}&Signature={}'
    url_amz = '.s3.amazonaws.com/'
    url = 'https://{}' + url_amz + '{}'

    def __init__(self, s3_bucket='', aws_access_key='', aws_secret_key=''):
        s3_bucket = os.environ.get('S3_BUCKET', s3_bucket)
        assert s3_bucket is not '', '''You must provide a bucket name. As
        keyword argument `s3_bucket` or an environment variable `S3_BUCKET`'''
        self.bucket_name = s3_bucket

        aws_access_key = os.environ.get('AWS_ACCESS_KEY', aws_access_key)
        assert aws_access_key is not '', '''You must provide an aws access key.
        As keyword argument `aws_access_key` or an environment variable
        `AWS_ACCESS_KEY`'''
        self.aws_access_key = aws_access_key

        aws_secret_key = os.environ.get('AWS_SECRET_KEY', aws_secret_key)
        assert aws_secret_key is not '', '''You must provide an aws secret key.
        As keyword argument `aws_secret_key` or an environment variable
        `AWS_SECRET_KEY`'''
        self.encoded_key = aws_secret_key.encode()

    def _get_expires(self, valid):
        return int(time.time() + valid)

    def _get_signature(self, **kwargs):
        string_to_sign = self.string_to_sign.format(bucket_name=self.bucket_name, object_name=self.object_name, **kwargs)

        encodedString = string_to_sign.encode()
        h = hmac.new(self.encoded_key, encodedString, sha1)
        hDigest = h.digest()
        signature = base64.encodebytes(hDigest).strip()
        signature = urllib.parse.quote_plus(signature)

        return signature

    def _get_signed_url(self, object_name, valid, mime_type=None):
        self.object_name = object_name
        expires = self._get_expires(valid)
        signature = self._get_signature(expires=expires, mime_type=mime_type)
        self.url = self._get_url()

        return self.signed_url.format(
            self.url, self.aws_access_key, expires, signature)

    def _get_url(self):
        url = self.url.format(self.bucket_name, self.object_name)
        return url

    def _get_headers(self, mime_type):
        headers = {'content-type': mime_type}
        return headers


class S3PUTSigner(S3BaseSigner):
    """Returns the signed url, the headers and the url to PUT an object in
    an S3 bucket. You will need a signed url to GET the object.

    """
    string_to_sign = "PUT\n\n{mime_type}\n{expires}\n/{bucket_name}/{object_name}"

    def get_signed_url(self, object_name, valid, mime_type):
        signed_url = self._get_signed_url(object_name, valid, mime_type)
        headers = self._get_headers(mime_type)

        return {'signed_url': signed_url,
                'headers': headers,
                'url': self.url,
                'object_name': self.object_name}


class S3PUTPublicSigner(S3PUTSigner):
    """Returns the signed url, the headers and the url to PUT an object
    *publicly* available in an S3 bucket.

    """
    amz_header = "x-amz-acl:public-read"
    string_to_sign_begin = "PUT\n\n{mime_type}\n{expires}\n"
    string_to_sign_end = "/{bucket_name}/{object_name}"

    def __init__(self, *args, **kwargs):
        self._set_string_to_sign()
        super(S3PUTPublicSigner, self).__init__(*args, **kwargs)

    def _get_headers(self, mime_type):
        headers = super(S3PUTPublicSigner, self)._get_headers(mime_type)
        headers.update(dict([self.amz_header.split(':')]))
        return headers

    def _set_string_to_sign(self):
        self.string_to_sign = self.string_to_sign_begin
        self.string_to_sign += self.amz_header + '\n'
        self.string_to_sign += self.string_to_sign_end


class S3GETSigner(S3BaseSigner):
    """Returns the signed url to GET an object from an S3 bucket"""
    string_to_sign = "GET\n\n\n{expires}\n/{bucket_name}/{object_name}"

    def get_signed_url(self, object_name, valid):
        signed_url = self._get_signed_url(object_name, valid)

        return {'signed_url': signed_url}


__version__ = '0.2.0'
