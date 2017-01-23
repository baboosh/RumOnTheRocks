# ## ## ## ## ## ## ## ## ## ## ## ##
#                                   #
#  translations file for Translator #
#  Project, imported into main.py   #
#  Used to translate given player   #
#  input . . .                      #
#  Made by Max Bethke at Tech Tree  #
#  Labs . . .                       #
#                                   #
#                                   #
# ## ## ## ## ## ## ## ## ## ## ## ##

from translate import *  # Import third party library translate (Not mine.)


class Translations:
    @staticmethod
    def translate(entry, from_lang, to_lang):  # Old translate function
        intrans = entry
        translator = Translator(from_lang=from_lang, to_lang=to_lang)
        print("entry text: " +intrans)
        translation = translator.translate(intrans)
        print("translated "+translation)
        var = ("(" + from_lang + " to " + to_lang +") Translation: " + translation)
        return var, translation

    @staticmethod
    def translateCustom(entry,lanfrom,lanto):  # Newer translate function
        translator = Translator(from_lang=lanfrom, to_lang=lanto)
        translation = translator.translate(entry)
        var = ("(" + lanfrom + " to " + lanto + ") Translation: " + translation)
        return var




