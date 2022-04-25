import os
import io
import json

from structures import *

import argparse

from PIL import Image, ImageDraw


os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'flawless-parity-343711-7c796736ffff.json'

# Imports the Google Cloud client library
from google.cloud import vision
from google.cloud import translate_v2 as translate


# Identify text blocks - genreate image with labels
class VisionEntry():
    def __init__(self,source,lang_pass):
        self.source = source
        self.out_img = ""
        self.out_text = ""
        self.pageObj = Page([])
        self.TranslatedObj = Page([])
        self.bounds_para = []
        self.bounds_block = []
        self.target_lang_pass = lang_pass


    def draw_boxes(self,image,bounds,color):
        """Draw a border around the image using the hints in the vector list."""
        # image = Image.open(self.source)
        draw = ImageDraw.Draw(image)

        for bound in bounds:
            draw.polygon(
                [
                    bound.vertices[0].x,
                    bound.vertices[0].y,
                    bound.vertices[1].x,
                    bound.vertices[1].y,
                    bound.vertices[2].x,
                    bound.vertices[2].y,
                    bound.vertices[3].x,
                    bound.vertices[3].y,
                ],
                None,
                color,
            )

        correct_ver = './images_bound/' + self.out_img
        if correct_ver != 0:
            image.save(correct_ver)
        else:
            image.show()

        return image


    def vision_act(self):
        # Main Vision code
        client = vision.ImageAnnotatorClient()

        with io.open(self.source, "rb") as self.source:
            content = self.source.read()

        image = vision.Image(content=content)
        response = client.document_text_detection(image=image)
        document = response.full_text_annotation

        # Key component
        # Page For loop - This is generally a 1 off thing per picture as the resolution should not support multi page veriations.
        for page in document.pages:
            page_data = []

            # Blocks for loop - Expected 1-15~ average blocks as space in between certain labels on products and documents vary too much - it will still be pretty useful for general marking to the user. - SEARCHING FOR way to number
            for block in page.blocks:
                # Build Temp data holders
                block_data = []
                block_Obj = Block(block_data)

                # Paragraph for loop - Paragraph specifacation is not too good but will be used as the general marking of bounds for text because it still allows to be very clear what text is focused on.
                for paragraph in block.paragraphs:
                    # Build Temp data holders
                    text_paragraph = ""
                    para_Obj = Paragraph(text_paragraph,True)

                    para_size = len(paragraph.words)
                    illegal_words = 0

                    # Word and Symbol - always connected - will probably not have colouring because it will clutter the image too much also colour coding is difficult ot manage in small amounts - Word doesn't hold much value in the final solution its a fixed solution for current idea.
                    for word in paragraph.words:
                        legal_word = True
                        text_word = ""
                        # word_length = len(word.symbols.text)

                        for symbol in word.symbols:
                            # Append symbol text data to the final word until completion.
                            text_word += symbol.text
                            if not (any(c.isalpha() for c in symbol.text)):
                                legal_word = False

                        if not legal_word:
                            illegal_words += 1

                        # Append the word to the paragraph.
                        text_paragraph += (text_word + " ")

                    # Paragraph text validity for translation -
                    if illegal_words == para_size:
                        para_Obj.valid_false()
                        # Colour Differently
                    else:
                        para_Obj.valid_true()

                        self.bounds_para.append(paragraph.bounding_box)

                    # Update the objects to be correct with the text data.
                    para_Obj.add_item(text_paragraph)
                    # para_Obj.set_bounds(paragraph.bounding_box)
                    block_Obj.add_item(para_Obj)

                    self.bounds_para.append(paragraph.bounding_box)

                # block_Obj.set_bounds(block.bounding_box)
                self.bounds_block.append(block.bounding_box)
                self.pageObj.add_item(block_Obj)


    # Google translate call and functionality
    def translation_func(self,t_language):
        translate_client = translate.Client()

        for each in self.pageObj.field:
            trans_block_Obj = Block([])

            for paragraphs_i in each.field:
                trans_para_Obj = Paragraph("",True)

                if paragraphs_i.valid:
                    trans_para_Obj.add_item((translate_client.translate(paragraphs_i.field, target_language=t_language))["translatedText"])
                    trans_para_Obj.valid_true()
                else:
                    trans_para_Obj.add_item(paragraphs_i.field)
                    trans_para_Obj.valid_false()

                trans_block_Obj.add_item(trans_para_Obj)

            self.TranslatedObj.add_item(trans_block_Obj)


    def trim_input_data(self):
        self.out_img = self.source.replace('old ','').replace('./images','')
        self.out_img = self.out_img.replace('..','').replace('/','').replace('\\','')


    def alter_output(self):
        self.out_text = self.out_img.replace('.jpg', '').replace('.png', '')
        # print(self.out_text)
        self.out_text = './text_data/' + self.out_text + '.json'
        # print(self.out_text)


    # Default main function for vision class that does all background operations
    # Any API calls and any file handling is managed in this class so all actions proceed through this system.
    # Will need patches when file loading is introduced unless a new format is introduced
    def vision_op(self):
        image2 = Image.open(self.source)
        self.trim_input_data()
        self.vision_act()
        self.draw_boxes(image2,self.bounds_block,"blue")
        self.draw_boxes(image2,self.bounds_para,"red")

        self.translation_func(self.target_lang_pass)
        self.alter_output()

        xd_dict = {}
        for x in range(len(self.TranslatedObj.field)):
            para_li = []
            for y in range(len(self.TranslatedObj.field[x].field)):
                if (self.TranslatedObj.field[x].field[y].valid):
                    para_li.append({
                    "original_text": self.pageObj.field[x].field[y].field,
                    "translated_text": self.TranslatedObj.field[x].field[y].field,
                    })
                else:
                    para_li.append({
                    "original_text": self.pageObj.field[x].field[y].field,
                    "translated_text": "Invalid Translation #000044",
                    })

            xd_dict[f"block{x}"] = para_li

        json_str = json.dumps(xd_dict, indent=4,ensure_ascii=False)
        # print(json_str)

        with open(self.out_text,'w', encoding="utf-8") as outfile:
            outfile.write(json_str)


# if __name__ == "__main__":
#     parser = argparse.ArgumentParser()
#     parser.add_argument("detect_file",help="The image for text detection")
#     args = parser.parse_args()
#
#     vision_C = VisionEntry(args.detect_file)
#     vision_C.vision_op()
