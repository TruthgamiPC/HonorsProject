class Structures():
    def __init__(self,data,valid):
        self.field = data
        self.valid = valid

    def add_item(self,data):
        self.field.append(data)

    def valid_true(self):
        self.valid = True

    def valid_false(self):
        self.valid = False

# Contains Text Data and a state of true or false if the data is valid for translation
class Paragraph(Structures):

    def add_item(self,data):
        self.field = data

# Contains References of Paragraphs
class Block(Structures):
    def __init__(self,data):
        self.field = data

# Contains References of Blocks
class Page(Structures):
    def __init__(self,data):
        self.field = data
