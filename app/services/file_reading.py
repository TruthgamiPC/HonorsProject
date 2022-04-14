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

    def stripper(self,file_name):
        return (file_name.replace('.jpg','').replace('.png',''))

    def searchDir(self):
        self.image_files = os.listdir('../images_bound/')
        print(self.image_files)

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


    def testOpen(self):
        x = self.image_files[0]
        y = self.stripper(x)
        self.target_file = '../text_data/' + y + '.json'
        print(self.target_file)

        try:
            file = open(self.target_file, encoding="utf8")
            data = json.load(file)

            for num in range(0,len(data)):
                # print(data[f'block{num}'])
                for n,each_seg in enumerate(data[f'block{num}']):
                    # print(each_seg['translated_text'])
                    # print(each_seg['original_text'])
                    og = tk.Text(window, height = 4, width = 70)
                    trans = tk.Text(window, height = 4, width = 70)

                    og.grid(column=0,row=(num+n)) # ,ipadx=25,ipady=5
                    trans.grid(column=1,row=(num+n)) # ipadx=25,ipady=5

                    og.insert(tk.END,each_seg['original_text'])
                    trans.insert(tk.END,each_seg['translated_text'])

                    og.configure(state='disabled')
                    trans.configure(state='disabled')

        except FileNotFoundError:
            msg = "Sorry, the file "+ self.target_file + "does not exist."
            print(msg) # Sorry, the file John.txt does not exist.
