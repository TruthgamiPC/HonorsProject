class Structures():
    def __init__(self,field,valid):
        self.field = field
        self.valid = valid
        self.bounds = []

    def add_item(self,data):
        self.field.append(data)

    def set_bounds(self,bound_data):
        self.bounds = bound_data

    def valid_true(self):
        self.valid = True

    def valid_false(self):
        self.valid = False

class Paragraph(Structures):

    def add_item(self,data):
        self.field = data

class Block(Structures):
    pass

class Page(Structures):
    def __init__(self,field):
        self.field = field
