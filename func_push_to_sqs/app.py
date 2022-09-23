import boto3
import json
import os
import urllib.parse


def lambda_handler(event, context):
  """
  Push to SQS triggered by S3.
  """
  sqs_queue = boto3.resource('sqs').get_queue_by_name(
    QueueName=os.environ.get('SQS_NAME')
  )

  for record in event['Records']:
    bucketname = record['s3']['bucket']['name']
    filename = record['s3']['object']['key']
    file_extension = os.path.splitext(
      os.path.basename(urllib.parse.urlparse(filename).path)
    )[1].replace('.', '')

    print("Processing ({filename}).".format(filename=filename))

    res_sqs = sqs_queue.send_message(
      MessageBody=filename,
      MessageAttributes={
        'bucketname': {
          'DataType': 'String',
          'StringValue': bucketname
        },
        'filename': {
          'DataType': 'String',
          'StringValue': filename
        },
        'file_extension': {
          'DataType': 'String',
          'StringValue': file_extension
        }
      }
    )
    print(json.dumps(res_sqs))
