# ## ## ## ## ## ## ## ## ## ## ## ##
#                                   #
#  supported file for Translator    #
#  Project, imported into main.py   #
#  Used to hold words given player  #
#  previous translations            #
#  Made by Max Bethke at Tech Tree  #
#  Labs . . .                       #
#                                   #
#                                   #
# ## ## ## ## ## ## ## ## ## ## ## ##
import json
class TranslatedWord:

    def __init__(self):
        self.tolan = ''
        self.fromlan = ''
        self.trans = ''
        self.entry = ''

    def toJson(self):
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4)



