#
#
#
#
# def parser(image_link, web=False):
#     if web:  # if web is True, the image link is a web resource, so we need to download it first
#
#         # download the image from the corresponding link and save it as a temp file
#     else:
#
#
#
#
#
#
#
#
#
#
#
#
#
# if __name__ == '__main__':
#     parser('test_cases/img-001.jpg')


import io
import os

# Imports the Google Cloud client library
from google.cloud import vision

# Instantiates a client
vision_client = vision.Client()

# The name of the image file to annotate
file_name = os.path.join(
    os.path.dirname(__file__),
    'resources/wakeupcat.jpg')

# Loads the image into memory
with io.open(file_name, 'rb') as image_file:
    content = image_file.read()
    image = vision_client.image(
        content=content)

# Performs label detection on the image file
labels = image.detect_labels()

print('Labels:')
for label in labels:
    print(label.description)