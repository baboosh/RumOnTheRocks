# Move to Translate.py
gSmallWindow = "362x158"

import tkinter as tk
from tkinter import ttk
import translations  # Import translations.py
import json
import os
from tkinter import filedialog
import Word
trans = translations.Translations
class Translate:
    langList = ['English', 'Spanish', 'Chinese', "Japanese", "French", "Russian", "Hindi",
                     "Arabic", "German", "Korean", "Bengali", "Portuguese",
                     "Vietnamese", "Turkish", "Italian", "Hungarian"]

    def __init__(self,app, parent):

        self.mainFrame = parent
        self.translateFrame = None
        self.translated = {}  # Holds already translated words
        self.entryVariable = tk.StringVar()  # Set up some widget variables
        self.langtoVariable = tk.StringVar()
        self.langfromVariable = tk.StringVar()
        self.messageVar = tk.StringVar()
        self.entryvar2 = tk.StringVar()
        self.labelVariable = tk.StringVar()
        self.toDropOption = tk.StringVar()
        self.fromDropOption = tk.StringVar()
        self.fileVariable = ''
        self.quiz = None
        self.transButton = None
        self.saveButton = None
        self.saveAsButton = None
        self.openButton = None
        self.changeModeButton = None
        self.terminal = None
        self.messageBox = None
        self.currentFile = None
        self.removeOptions = []

        self.fromDrop = None
        self.toDrop = None
        self.entry = None
        self.log = "Log text!"
        self.saveOptions = tk.StringVar()

        self.path = "./saves/default.json"  # Change this for the default file

        self.makeTranslate()

    def makeTranslate(self):

        self.getFilenames()
        self.translateFrame = tk.Frame(self.mainFrame)

        self.fileLabel = tk.LabelFrame(self.translateFrame, text="File Options", width=20)
        self.translateLabel = tk.LabelFrame(self.translateFrame, text="Translate Options", width=20)

        self.entry = tk.Entry(self.translateFrame,
                              textvariable=self.entryVariable)  # Make the entry variable for inputs
        self.entryVariable.set(u"Enter Text:")  # Player input for stuff to be translated



        self.toDrop = ttk.Combobox(self.translateLabel, textvariable=self.toDropOption, values=self.langList)
        self.toDropOption.set("To")


        self.fromDrop = ttk.Combobox(self.translateLabel, textvariable=self.fromDropOption, values=self.langList)

        self.fromDropOption.set("From")

        self.removeButton = tk.Button(self.fileLabel,
                                      text=u"Remove",
                                      command=self.OnButtonClickRemove)

        self.transButton = tk.Button(self.translateLabel,
                                     text=u"Translate",
                                     command=self.OnButtonClickCustom)

        self.saveButton = tk.Button(self.fileLabel,
                                    text=u"Save",
                                    command=self.save_it)

        self.saveAsButton = tk.Button(self.fileLabel,
                                      text=u"Save as",
                                      command=self.save_as)

        self.openButton = tk.Button(self.fileLabel,
                                    text=u"Open File",
                                    command=self.open_it)

        self.newButton = tk.Button(self.fileLabel,
                                   text=u"New File",
                                   command=self.new_file)

        self.currentFile = tk.Label(self.translateFrame, textvariable=self.fileVariable,
                                    anchor="w", fg="black", bg="black", width=90)

        label = tk.Label(self.translateFrame, textvariable=self.labelVariable,  # Translation
                         anchor="w", fg="white", bg="black", width=90)

        self.removeButton.grid(column=2, row=2)
        self.toDrop.grid(column=3, row=0, sticky="ew")  # First dropbox
        self.fromDrop.grid(column=3, row=1, sticky="ew")

        self.newButton.configure(width=12)
        self.removeButton.configure(width=12)
        self.toDrop.configure(width=12)
        self.fromDrop.configure(width=12)
        self.saveAsButton.configure(width=11)
        self.saveButton.configure(width=11)
        self.openButton.configure(width=11)
        self.transButton.configure(width=11)

        self.transButton.grid(column=3, row=2)
        self.saveButton.grid(column=2, row=3)
        self.saveAsButton.grid(column=2, row=4)
        self.openButton.grid(column=2, row=5)
        self.entry.grid(column=0, row=3, sticky='ew')  # Grid it
        self.newButton.grid(column=2, row=6)

        self.fileLabel.grid(column=2, row=1)
        self.translateLabel.grid(column=2, row=8)

        label.grid(column=0, row=7, sticky='ew')
        label.configure(width=40)
        self.labelVariable.set(u" Translation:")

        self.currentFile.grid(column=0, row=10, sticky='ew')
        self.currentFile.configure(width=40)

        self.fileVariable = ("current file:" + self.path)
        print(self.fileVariable)
        self.entry.focus_set()
        self.entry.selection_range(0, tk.END)
        self.translateFrame.grid(row=2, column=5)



    def dump_dict(self, fromLang, toLang, entry, trans):
        if self.path == "./saves/default.json":
            print("DUMPING INTO DEFAULT FILE")
        with open(self.path, 'w') as fp:
            fullDict = {}
            fullDict["from_lang"] = fromLang
            fullDict["to_lang"] = toLang
            fullDict["entry"] = entry
            fullDict["trans"] = trans
            twl = {}
            idx = 0
            for t in self.translated:
                tw = self.translated[t].toJson()
                twl[idx] = tw
                idx += 1
                print(tw)
            fullDict["wordsList"] = twl
            json.dump(fullDict, fp)
            print("Dumped in " + self.path)
            print(trans)
        # Move to translate.py
    def OnButtonClickCustom(self):


        entry = self.entryVariable.get()
        lang_to = self.toDropOption.get()
        lang_from = self.fromDropOption.get()
        if lang_to == "To":
            print("Invalid Choice: To")
        if lang_from == "From":
            print("Invalid Choice: From")

        key = lang_from + lang_to + entry

        if key in self.translated:
            print("Already here!")

        var, translation = trans.translate(entry, lang_from, lang_to)
        self.labelVariable.set(var)

        word = Word.TranslatedWord()
        word.lanto = lang_to
        word.fromlan = lang_from
        word.entry = entry
        word.trans = translation
        self.translated[key] = word
        for key, value in self.translated.items():
            print(key + " : " + value.trans)
        self.dump_dict(lang_from, lang_to, entry, translation)

    # Move to translate.py
    def OnButtonClickRemove(self):
        filename = tk.filedialog.askopenfilename(defaultextension=".json", initialdir="./saves/",
                                                 title="Translator", message="Open a file for Translator")
        if filename.endswith(".json"):
            os.remove(filename)
            print("Removed " + filename)
        else:
            print("Thats not a save file!")

    # Move to translate.py
    def destroyFunc(self):
        self.newwindow.destroy()


        # Move to translate.py
    def new_file(self):
        self.file = None
        self.newwindow = None
        self.text = None
        self.yes = None
        self.no = None
        self.frame = None

        self.newwindow = tk.Toplevel()
        self.newwindow.title('Make New File')
        self.newwindow.geometry(gSmallWindow)
        self.frame = tk.Frame(self.newwindow)
        self.newwindow.bind('<Return>', lambda e: self.printResult())
        self.text = tk.Message(self.frame, text="Please input name (Don't Put .json)")
        self.entry2 = tk.Entry(self.frame,
                               textvariable=self.entryvar2)  # Make the entry variable for inputs

        self.entryvar2.set("default")
        self.confirmButton = tk.Button(self.frame, text="Confirm", command=self.makeNewFile)
        self.cancelButton = tk.Button(self.frame, text="Cancel", command=self.destroyFunc)

        self.cancelButton.grid(column=2, row=1)
        self.confirmButton.grid(column=1, row=1)
        self.text.grid(column=2, row=0)
        self.frame.grid(column=0, row=0)
        self.entry2.grid(column=3, row=1)

    # Move to translate.py
    def makeNewFile(self):
        filename = self.entryvar2.get()
        fileexetension = ".json"
        dir = "./saves/"
        fullpath = dir + filename + fileexetension
        if fullpath.endswith(".json"):
            with open(fullpath, 'a') as fp:
                twl = {"description:": "Save file for translator!"}
                json.dump(twl, fp)
                print("Made file: " + fullpath + " and dumped defaults.")
                self.destroyFunc()
        else:
            print("file does not end with .json")

    # Dunno, debug statement for newwindow binding
    def printResult(self):
        filename = self.entryvar2.get()
        print(filename + " filename")

        # Move to Translate.py
    def getFilenames(self):
        filepath = ('./saves/')
        listnames = os.listdir(filepath)
        print(listnames, " filenames")
        self.removeOptions = []
        for l in listnames:
            if l.endswith(".json"):
                k = l  # Add things here
                self.removeOptions.append(k)
                print(l, " added to directory" + filepath)
            else:
                print("not a valid save file (" + l + ")")
        if self.removeOptions == []:
            self.removeOptions = ["No Save found"]

        # Move to Translate.py
    def open_it(self):
        filename = tk.filedialog.askopenfilename(defaultextension=".json", initialdir="./saves/",
                                                 title="Translator", message="Open a file for Translator")
        self.path = filename
        print(filename + " OPENED")  # test

    @staticmethod
    def save_it():
        filename = tk.filedialog.askopenfile(defaultextension=".json", title="Translator")
        print(filename + " SAVED IT")  # test

    # Move to Translate.py
    @staticmethod
    def save_as():
        filename = tk.filedialog.asksaveasfilename(defaultextension=".json", initialfile="auto_save.json",
                                                   title="Translator")
        print(filename + " SAVE AS")
        with open(filename, 'a') as fp:
            twl = {"description:": "Save file for translator!"}
            json.dump(twl, fp)
            print("Done! ")

    # Move to Translate.py
    def removeFile(self):
        full_file_paths = os.listdir("./saves/")
        for f in full_file_paths:
            if f.endswith(".json"):
                os.remove(f)
            else:
                print("Not a valid save file!")