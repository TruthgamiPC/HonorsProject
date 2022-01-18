import os
import io

os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'turnkey-wording-338516-45d2d1f4d5ca.json'

# Imports the Google Cloud client library
from google.cloud import vision

# Instantiates a client
client = vision.ImageAnnotatorClient()

# The name of the image file to annotate
file_name = os.path.abspath('Screenshot_82.png')

# Loads the image into memory
with io.open(file_name, 'rb') as image_file:
    content = image_file.read()

image = vision.Image(content=content)

# Performs label detection on the image file
response = client.label_detection(image=image)
reponse_text = client.text_detection(image=image)
labels = response.label_annotations

print('Labels:')
for label in labels:
    print(label.description)

print('Text:\n')
text_data = []

for r in reponse_text.text_annotations:
    d = { 'text': r.description}

    text_data.append(d)
    print(d)
