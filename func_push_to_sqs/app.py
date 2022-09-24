import boto3
import json
import os
import urllib.parse


def lambda_handler(event, context):
  """
  Push to SQS triggered by S3.
  """
  for record in event['Records']:
    bucketname, filename, file_extension = get_parameters(record)

    print("Processing ({filename}).".format(filename=filename))

    res = sqs_send_message(bucketname, filename, file_extension)
    print(json.dumps(res))


def get_parameters(record):
  """
  Get parameters to be sent to SQS.
  """
  bucketname = record['s3']['bucket']['name']
  filename = record['s3']['object']['key']
  file_extension = os.path.splitext(
    os.path.basename(urllib.parse.urlparse(filename).path)
  )[1].replace('.', '')

  return bucketname, filename, file_extension


def sqs_send_message(bucketname, filename, file_extension):
  """
  Send SQS message.
  """
  sqs_queue = boto3.resource('sqs').get_queue_by_name(
    QueueName=os.environ.get('SQS_NAME')
  )

  res = sqs_queue.send_message(
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
  return res
