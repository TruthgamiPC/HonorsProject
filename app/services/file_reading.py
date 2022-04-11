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

    def searchDir(self):
        # self.image_files = glob.glob('../images_bound/*.jpg')
        # self.image_files += glob.glob('../images_bound/*.png')
        # print(self.image_files)

        self.image_files = os.listdir('../images_bound/')
        # tmp_text = os.listdir('../text_data/')
        # tmp = os.listdir('../images/')
        # print(tmp)
        # print(tmp_text)
        print(self.image_files)

        # self.testOpen()

    def testOpen(self):

        # for x in self.image_files:
        x = self.image_files[0]
        y = x.replace('.jpg','').replace('.png','')
        self.target_file = '../text_data/' + y + '.json'
        print(self.target_file)
        window= tk.Tk()
        window.geometry("1000x400")

        # window = tk.Tk()

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

                    # greeting = tk.Text(text=each_seg['original_text'],wraplength=450,state='disabled')
                    # translated = tk.Text(text=each_seg['translated_text'],wraplength=450,state='disabled')
                    # translated.grid(column=0,row=(num+n),ipadx=25,ipady=5)
                    # greeting.grid(column=1,row=(num+n),ipadx=25,ipady=5)
                    # print(n)
                    # if each_seg['translated_text'] == 'Invalid Translation #000044':

                        # continue:


            # for i in data:
            #     print(i)

            # print(data)

        except FileNotFoundError:
            msg = "Sorry, the file "+ self.target_file + "does not exist."
            print(msg) # Sorry, the file John.txt does not exist.

            # try:
            #     f = open(self.target_file)
            #     data = json.load(f)
            #     print(data)

            #     with open(self.target_file) as f_obj:
            #         contents = f_obj.read()
            #         print(contents)

            # except FileNotFoundError:
            #     msg = "Sorry, the file "+ self.target_file + "does not exist."
            #     print(msg) # Sorry, the file John.txt does not exist.







# wow = ReadingFiles()
# window = tk.Tk()
# tk.mainloop()
