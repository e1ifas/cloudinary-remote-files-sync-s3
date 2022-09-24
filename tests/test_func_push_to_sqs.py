import json
from func_push_to_sqs.app import get_parameters


def test_get_parameters(shared_datadir):
  _record = (shared_datadir / 'generate-event_s3-delete.json').read_text()
  __record = json.loads(_record)
  for record in __record['Records']:
    # bucketname
    assert get_parameters(record)[0] == "S3_BUCKET_NAME"
    # filename
    assert get_parameters(record)[1] == "cloudinary-content/S3_OBJECT_NAME.jpeg"
    # file_extension
    assert get_parameters(record)[2] == "jpeg"
