import os
import io
import json

import glob
import tkinter as tk

class ReadingFiles():

    def __init__(self):
        self.target_file = ''
        self.image_files = []
        self.searchDir()

    def og_strip(self,file_name):
        return (file_name.replace('../images/',''))

    def stripper(self,file_name):
        return (file_name.replace('.jpg','').replace('.png',''))

    def searchDir(self):
        self.image_files = os.listdir('../images_bound/')
        # print(self.image_files)

    def targeted_text(self,text_file):
        full_name = '../text_data/' + self.stripper(text_file) + '.json'
        print(full_name)

        try:
            file = open(full_name,encoding='utf8')
            data = json.load(file)

            return data
        except FileNotFoundError:
            msg = "Sorry, the file "+ full_name + " does not exist."
            print(msg) # Sorry, the file John.txt does not exist.
            return
