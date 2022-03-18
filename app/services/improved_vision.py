import os
import io

from structures import *

import argparse
from enum import Enum
from PIL import Image, ImageDraw

os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'flawless-parity-343711-7c796736ffff.json'

# Imports the Google Cloud client library
from google.cloud import vision

class FeatureType(Enum):
    PAGE = 1
    BLOCK = 2
    PARA = 3
    WORD = 4
    SYMBOL = 5

# Identify text blocks - genreate image with labels
class VisionEntry():
    def __init__(self,source):
        self.source = source
        self.out_img = ""
        self.pageObj = Page([])
        self.bounds_para = []
        self.bounds_block = []
        self.bounds_words = []

    def set_out(self,fileout):
        self.out_img = fileout

    '''
    ?#Block1:
    ?#Para: xxx xxx xxx xxx ~#Para.
    ?#Para: asd dsa bro wut ~#Para.
    ~#Block1.

    ?#Block2:
    ?#Para: asd dsa bro wut ~#Para.
    ~#Block2.

    ?#Block3:
    ?#Para: dsadsa dsadwq21 xxx xxx ~#Para.
    ?#Para: asd wut ~#Para.
    ~#Block3.
    '''

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

        if self.out_img != 0:
            image.save(self.out_img)
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
        page_obj = Page([])
        for page in document.pages:
            page_data = []

            # Blocks for loop - Expected 1-15~ average blocks as space in between certain labels on products and documents vary too much - it will still be pretty useful for general marking to the user. - SEARCHING FOR way to number
            for block in page.blocks:
                # Build Temp data holders
                legal_block = True
                block_data = []
                block_Obj = Block(block_data,legal_block)


                # Paragraph for loop - Paragraph specifacation is not too good but will be used as the general marking of bounds for text because it still allows to be very clear what text is focused on. - WILL INCLUDE the key colouring for the images.
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
                        word_length = len(word.symbols.text)

                        for symbol in word.symbols:
                            # Append symbol text data to the final word until completion.
                            text_word += symbol.text
                            if not (any(c.isalpha() for c in symbol.text)):
                                legal_word = False



                        self.bounds_words.append(word.bounding_box)
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

                    # self.bounds_para.append(paragraph.bounding_box)

                #print(block_Obj.field)
                # Testing object storage
                # for each in block_Obj.field:
                #     print(each.valid)

                block_Obj.set_bounds(block.bounding_box)
                # self.bounds_block.append(block.bounding_box)
                self.pageObj.add_item(block_Obj)
        # print(self.bounds_para)
        #------------------------
        # print(self.bounds_block)
        # image2 = Image.open(self.source)
        # self.draw_boxes(image2,self.bounds_para,"green")
        # self.draw_boxes(image2,self.bounds_block,"blue")





    def vision_op(self):
        image2 = Image.open(self.source)
        self.vision_act()
        # self.draw_boxes(image2,self.bounds_block,"blue")
        self.draw_boxes(image2,self.bounds_para,"red")

        # for each in self.pageObj.field:
        #     for paragraphs_i in each.field:
        #         if paragraphs_i.valid:
        #             self.draw_boxes(image2,paragraphs_i.bounds,"green")
        #         else:
        #             self.draw_boxes(image2,paragraphs_i.bounds,"red")


        for each in self.pageObj.field:
            for eachP in each.field:
                print(eachP.field)



if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("detect_file", help="The image for text detection")
    parser.add_argument("-out_file", help="Optimal output file",default=0)
    args = parser.parse_args()

    vision_C = VisionEntry(args.detect_file)
    vision_C.set_out(args.out_file)
    vision_C.vision_op()
    #render_doc_text(args.detect_file, args.out_file)
