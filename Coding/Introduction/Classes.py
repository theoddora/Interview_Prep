# Class
class MyClass:
    # Constructor
    def __init__(self, name):
        # self is passed in every method of a class
        # similar to this keyword in other languages

        # this creates a member variable called name
        self.name = name

    # self keyword required as param
    def get_name(self):
        return self.name