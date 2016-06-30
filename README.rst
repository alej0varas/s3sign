Get a signed url to PUT or GET a file to/from an Amazon S3 bucket

Usage
=====

PUT a file
~~~~~~~~~~
::

   from s3sign import S3PUTSigner

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
   content = open(file_name, 'rb').read()

   # PUT the object
   requests.put(url, data=content, headers=headers)

GET a file
~~~~~~~~~~
::

   signer = S3GETSigner()

   url = <the url to an object>
   signed_url = signer.get_signed_url(url, valid)
   requests.get(signed_url)

Run test
========
::

   export S3_BUCKET=<your-bucket>
   export AWS_ACCESS_KEY=<your-access-key>
   export AWS_SECRET_KEY=<your-secret-key>
   python -m unittest discover