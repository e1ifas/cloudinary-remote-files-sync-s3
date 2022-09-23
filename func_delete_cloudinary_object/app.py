from urllib.parse import urlparse
import cloudinary
import cloudinary.uploader
import json
import os
import sys

cloudinary.config(
  cloud_name=os.environ.get('CLOUDINARY_CLOUDNAME'),
  api_key=os.environ.get('CLOUDINARY_APIKEY'),
  api_secret=os.environ.get('CLOUDINARY_APISECRET')
)

# The delivery type of the asset.
content_type = "upload"

# https://cloudinary.com/documentation/image_transformations#supported_image_formats
supported_image_formats = [
  "ai", "arw", "avif", "bmp", "bw", "cr2", "djvu", "eps", "eps3", "ept", "fbx",
  "flif", "gif", "glb", "gltf", "hdp", "heic", "heif", "ico", "indd", "jp2",
  "jpe", "jpeg", "jpg", "jxr", "obj", "pdf", "ply", "png", "ps", "psd", "svg",
  "tga", "tif", "tiff", "u3ma", "usdz", "wdp", "webp"
]

# https://cloudinary.com/documentation/video_manipulation_and_delivery#supported_video_formats
# https://cloudinary.com/documentation/audio_transformations#supported_audio_formats
supported_video_formats = [
  "3g2", "3gp", "aac", "aiff", "amr", "avi", "flac", "flv", "m2ts", "m3u8",
  "m4a", "mkv", "mov", "mp3", "mp4", "mpd", "mpeg", "mts", "mxf", "ogg", "ogv",
  "opus", "ts", "wav", "webm", "wmv"
]


def lambda_handler(event, context):
  """
  Delete object from Cloudinary.
  """

  for record in event['Records']:
    filename = record['messageAttributes']['filename']['stringValue']
    filename_withhout_extension = os.path.splitext(
      os.path.basename(urlparse(filename).path)
    )[0]
    file_extension = record['messageAttributes']['file_extension']['stringValue'
                                                                  ]

    # image, raw, video or auto. Defaults: image
    _resource_type = ""

    if file_extension in supported_image_formats:
      _resource_type = "image"
    elif file_extension in supported_video_formats:
      _resource_type = "video"
    else:
      print(
        "Error: Failed to delete Cloudinary content. File extension ({file_extension}) is not supported."
        .format(file_extension=file_extension)
      )

    # https://cloudinary.com/documentation/upload_images#public_id
    public_id = os.environ.get(
      'MAPPING_DIR_ON_CLOUDINARY'
    ) + "/" + filename_withhout_extension

    print("Processing {public_id}.".format(public_id=public_id))

    try:
      res_explicit = cloudinary.uploader.explicit(
        public_id, resource_type=_resource_type, type=content_type
      )

      res_destroy = cloudinary.uploader.destroy(
        public_id, resource_type=_resource_type, invalidate=True
      )

      print(json.dumps(res_destroy))
      print(
        "Success: Deleted Cloudinary content ({public_id}).".format(
          public_id=public_id
        )
      )
    except Exception as e:
      print(
        "Error: Failed to delete Cloudinary content ({public_id}).".format(
          public_id=public_id
        )
      )
      print(e)
