import boto3
import pyminizip
import tempfile
import os

s3backetread = ''
s3backetwrite = ''

filename = 'myface.png'
s3 = boto3.resource('s3')

obj = s3.Object(s3backetread, filename)
response = obj.get()
tmpdir = tempfile.TemporaryDirectory()
fp = open(tmpdir.name + '/' + filename, 'wb')
fp.write(response['Body'].read())
fp.close()


zipname = tempfile.mkstemp(suffix='.zip')
os.chdir(tmpdir.name)
pyminizip.compress(filename, '', zipname, 'mypassword', 0)

obj = s3.Object(s3backetwrite, filename + '.zip')
response = obj.put(
    Body=open(zipname, 'rb')
)

tmpdir.cleanup()
os.unlink(zipname)