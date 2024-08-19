
class Tag:
    """ Tag class"""

    """ Constructor """
    def __init__(self, name: str):
        self.__name = name

    """ To str """
    def __str__(self):
        return f"Tag: {self.__name}"
    
    """ Getter for name"""
    @property
    def name(self):
        return self.__name
    
    """ Setter for name"""
    @name.setter
    def name(self, new_name: str):
        self.__name = new_name