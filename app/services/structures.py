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

class Paragraph(Structures):

    def add_item(self,data):
        self.field = data

class Block(Structures):
    def __init__(self,data):
        self.field = data

class Page(Structures):
    def __init__(self,data):
        self.field = data
