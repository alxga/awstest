from datetime import datetime
import boto3
from .settings import Settings
from .credentials import S3ConnArgs

__author__ = "Alex Ganin"


class S3Mgr:
  def __init__(self, bucketName=Settings.S3BucketName):
    self._Res = boto3.resource('s3', **S3ConnArgs)
    self._Client = boto3.client('s3', **S3ConnArgs)
    self.bucketName = bucketName

  def move_key(self, objKey, nObjKey):
    self._Res.Object(self.bucketName, nObjKey). \
      copy_from(
        CopySource={
          'Bucket': self.bucketName, 'Key': objKey
        }
      )
    self._Res.Object(self.bucketName, objKey).delete()

  def fetch_keys(self, prefix, limit=None):
    objKeys = []
    bucket = self._Res.Bucket(self.bucketName)
    for obj in bucket.objects.filter(Prefix=prefix):
      if limit and len(objKeys) >= limit:
        break
      objKeys.append(obj.key)
    return objKeys

  def fetch_object_body(self, objKey):
    obj = self._Res.Object(self.bucketName, objKey)
    body = obj.get()["Body"].read()
    return body

  def put_object_body(self, objKey, data):
    obj = self._Res.Object(self.bucketName, objKey)
    obj.put(Body=data)

  def upload_file(self, fPath, objKey):
    self._Res.Object(self.bucketName, objKey).upload_file(fPath)

  def prefix_exists(self, prefix):
    result = self._Client.list_objects_v2(
        Bucket=self.bucketName, MaxKeys=1, Prefix=prefix
    )
    return result["KeyCount"] > 0


def S3FeedKeyDT(objKey):
  dtval = objKey[-18:-3] # Naming assumed: 'pb/<Feed Name>/YYYYMMDD/HHMMSS.pb2'
  dt = datetime.strptime(dtval, "%Y%m%d/%H%M%S")
  return dt
