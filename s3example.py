import boto3
import pyminizip
import tempfile
import os

s3backetread = 'suh7881-exampleread000'
s3backetwrite = 'suh7881-examplewrite0000'

filename = 'myface.png'
s3 = boto3.resource('s3')

# ファイルの読込
# S3からオブジェクト取得
obj = s3.Object(s3backetread, filename)
response = obj.get()
tmpdir = tempfile.TemporaryDirectory()
print(tmpdir.name+'/'+filename)
fp = open(tmpdir.name + '/' + filename, 'wb')
fp.write(response['Body'].read())
fp.close()

# 暗号化
zipname = tempfile.mkstemp(suffix='.zip')
os.chdir(tmpdir.name)

print(zipname)
pyminizip.compress(filename, '', zipname, 'mypassword', 0)

# S3にアップデート
obj = s3.Object(s3backetwrite, filename + '.zip')
response = obj.put(
    Body=open(zipname, 'rb')
)

tmpdir.cleanup()
os.unlink(zipname)