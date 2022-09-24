import json
import os
from func_delete_cloudinary_object.app import get_parameters


def test_get_parameters(shared_datadir):
  _event = (shared_datadir /
            'generate-event_sqs-receive-message.json').read_text()
  __event = json.loads(_event)
  os.environ['MAPPING_DIR_ON_CLOUDINARY'] = "s3-content"
  for record in __event['Records']:
    # filename
    assert get_parameters(record)[0] == "cloudinary-content/S3_OBJECT_NAME.jpeg"
    # filename_withhout_extension
    assert get_parameters(record)[1] == "S3_OBJECT_NAME"
    # file_extension
    assert get_parameters(record)[2] == "jpeg"
    # public_id
    assert get_parameters(record)[3] == "s3-content/S3_OBJECT_NAME"
