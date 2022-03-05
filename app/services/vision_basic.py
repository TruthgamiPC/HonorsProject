import os
import io

import argparse
from enum import Enum

class FeatureType(Enum):
    PAGE = 1
    BLOCK = 2
    PARA = 3
    WORD = 4
    SYMBOL = 5

os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'turnkey-wording-338516-45d2d1f4d5ca.json'

# Imports the Google Cloud client library
from google.cloud import vision

# Instantiates a client
client = vision.ImageAnnotatorClient()

# The name of the image file to annotate
file_name = os.path.abspath('out2.jpg')

# Loads the image into memory
with io.open(file_name, 'rb') as image_file:
    content = image_file.read()

image = vision.Image(content=content)

# Performs label detection on the image file
#response = client.label_detection(image=image)
reponse_text = client.document_text_detection(image=image)
document = reponse_text.full_text_annotation
#labels = response.label_annotations

#print('Labels:')
#for label in labels:
#    print(label.description)

print('Text:\n')
text_data = []



for page in document.pages:
    for block in page.blocks:
        for paragraph in block.paragraphs:
            for word in paragraph.words:
                illegal_word = 0
                length = 0
                print("---------------------------")
                for symbol in word.symbols:
                    length += 1
                    if not (any(c.isalpha() for c in symbol.text)):
                        illegal_word = 1
                        #print(symbol.text)

                if illegal_word != 1:
                    if length => 1:
                        if not ()
                        for symbol in word.symbols:
                            print(symbol.text)




'''
for r in reponse_text.text_annotations:
    d = { 'text': r.description}

    text_data.append(d)
    print(d)
'''
