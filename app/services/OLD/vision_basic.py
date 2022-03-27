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

os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'flawless-parity-343711-7c796736ffff.json'

# Imports the Google Cloud client library
from google.cloud import vision

# Instantiates a client
client = vision.ImageAnnotatorClient()

# The name of the image file to annotate
file_name = os.path.abspath('../images/Screenshot_90.png')

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



# for page in document.pages:
#     for block in page.blocks:
#         block_size = len(block.paragraphs)
#         print(block_size)
#         for paragraph in block.paragraphs:
#             para_size = len(paragraph.words)
#             # print(para_size)
#             for word in paragraph.words:
#                 line = ""
#                 for symbol in word.symbols:
#                     line += symbol.text


for page in document.pages:
    for block in page.blocks:
        legal_block = True

        for paragraph in block.paragraphs:
            legal_paragraph = True
            text_paragraph = ""
            para_size = len(paragraph.words)
            # print(para_size)
            illegal_words = 0


            for word in paragraph.words:
                legal_word = True
                text_word = ""
                length = 0


                for symbol in word.symbols:
                    # if not (any(c.isalpha() for c in symbol.text)):
                    #     legal_word = False
                    #     break
                    # else:
                    text_word += symbol.text
                    # length += 1


                if not legal_word:
                    illegal_words += 1
                    continue
                else:
                    text_paragraph += (text_word + " ")

            # Paragraph text validity for translation -
            if illegal_words == para_size:
                legal_paragraph = False
                # Colour Differently
                break
            else:
                # Here it works
                print(text_paragraph)
                # print(line)


                # illegal_word = 0
                # length = 0
                # print("---------------------------")
                # for symbol in word.symbols:
                #     length += 1
                #     if not (any(c.isalpha() for c in symbol.text)):
                #         illegal_word = 1
                #         #print(symbol.text)
                #
                # if illegal_word != 1:
                #     if length => 1:
                #         if not ()
                #         for symbol in word.symbols:
                #             print(symbol.text)




'''
for r in reponse_text.text_annotations:
    d = { 'text': r.description}

    text_data.append(d)
    print(d)
'''
