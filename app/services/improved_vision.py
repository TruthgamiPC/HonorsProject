import os
import io
import json

from structures import *

import six
import argparse

from PIL import Image, ImageDraw


os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'flawless-parity-343711-7c796736ffff.json'

# Imports the Google Cloud client library
from google.cloud import vision
from google.cloud import translate_v2 as translate


# Identify text blocks - genreate image with labels
class VisionEntry():
    def __init__(self,source):
        self.source = source
        self.out_img = ""
        self.pageObj = Page([])
        self.TranslatedObj = Page([])
        self.bounds_para = []
        self.bounds_block = []


    def set_out(self,fileout):
        self.out_img = fileout


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

    # Default main function for vision class that does all background operations
    # Any API calls and any file handling is managed in this class so all actions proceed through this system.
    # Will need patches when file loading is introduced unless a new format is introduced
    def vision_op(self):
        image2 = Image.open(self.source)
        self.vision_act()
        self.draw_boxes(image2,self.bounds_block,"blue")
        self.draw_boxes(image2,self.bounds_para,"red")

        self.translation_func("bg")

        for x in range(len(self.TranslatedObj.field)):
            temp_block_text = "block_data_" + str(x+1) + ":\n"
            for y in range(len(self.TranslatedObj.field[x].field)):
                print(self.pageObj.field[x].field[y].field)
                print(self.TranslatedObj.field[x].field[y].field)
                print("#---------------------------------------")
        print("##-----------------------------------------------------------------------")

        xd_dict = {}
        for x in range(len(self.TranslatedObj.field)):
            para_li = []
            for y in range(len(self.TranslatedObj.field[x].field)):
                if (self.TranslatedObj.field[x].field[y].valid):
                    para_li.append({
                    "original_text": self.TranslatedObj.field[x].field[y].field,
                    "translated_text": self.pageObj.field[x].field[y].field,
                    })
                else:
                    para_li.append({
                    "original_text": self.TranslatedObj.field[x].field[y].field,
                    "translated_text": "Invalid Translation #000044",
                    })

            xd_dict[f"block{x}"] = para_li

        json_str = json.dumps(xd_dict, indent=4,ensure_ascii=False)
        print(json_str)
        with open("../text_data/test.json",'w', encoding="utf-8") as outfile:
            outfile.write(json_str)



        # for i, b in enumerate(self.pageObj.field):
        #     para_li = []
        #     for p in b.field:
        #         para_li.append({
        #             "og": p.field,
        #             "trans": p.valid,
        #         })
        #     xd_dict[f"block{i}"] = para_li
        #
        # print(json.dumps(xd_dict, indent=4))


        '''
        file version code
        '''
        # Sample code to save the page object to a file
        # file_ver = "../text_data/test" + ".txt"
        # try:
        #     f = open(file_ver,"w", encoding="utf-8")
        #
        #     for x in range(len(self.TranslatedObj.field)):
        #         temp_block_text = "block_data_" + str(x+1) + ":\n"
        #         for y in range(len(self.TranslatedObj.field[x].field)):
        #
        #             if (self.TranslatedObj.field[x]).field[y].valid:
        #                 temp_block_text += ("\t-translated_text_" + str(y+1) + ": " + str(self.TranslatedObj.field[x].field[y].field) + "\n")
        #                 temp_block_text += ("\t-original_text_" + str(y+1) + ": " + str(self.pageObj.field[x].field[y].field) + "\n")
        #
        #             else:
        #                 temp_block_text += ("\t-original_text_" + str(y+1) + ": " + str(self.TranslatedObj.field[x].field[y].field) + "\n")
        #
        #         f.write(temp_block_text)
        #
        # except IOError:
        #     print(file_ver + " - Not found")

            # Original method to writting to a file - used as an example
            # for each in self.TranslatedObj.field:
            #     temp_block_text = "block_data_" + str(block_counter) + ":\n"
            #     para_counter = 1
            #     # print("#------------------------------------#")
            #     for paragraphs_i in each.field:
            #         # print(paragraphs_i.field)
            #         if paragraphs_i.valid:
            #             temp_block_text += ("\t-paragraph_text_" + str(para_counter) + ": " + str(paragraphs_i.field) + "\n")
            #         temp_block_text += ("\t-paragraph_text_" + str(para_counter) + ": " + str(paragraphs_i.field) + "\n")
            #         temp_block_text += ("\t-paragraph_state_" + str(para_counter) + ": " + str(paragraphs_i.valid) + "\n")
            #         para_counter += 1
            #     block_counter += 1
            #     # print(temp_block_text)
            #     f.write(temp_block_text)



if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("detect_file", help="The image for text detection")
    parser.add_argument("-out_file", help="Optimal output file",default=0)
    args = parser.parse_args()

    vision_C = VisionEntry(args.detect_file)
    vision_C.set_out(args.out_file)
    vision_C.vision_op()
    #render_doc_text(args.detect_file, args.out_file)
