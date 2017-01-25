import time
import random
from difflib import SequenceMatcher
import tkinter as tk
from tkinter import ttk
import json

class Achievement:
    def __init__(self, app, parent):
        self.parent = parent
        self.app = app
        self.TranslateLabel = None
        self.nearAchieveTrans = None
        self.nearTransVar = tk.StringVar()

        self.achieveFrame = tk.Frame(self.parent)

        self.difficulties = {"Easy": 0, "Medium": 1, "Hard": 2}
        self.difficulty = self.difficulties["Medium"]
        self.pointValue = 0
        self.averyprob = 100
        self.levelValue = 1

        self.numRight = 0
        self.tested = 0
        self.numWrong = 0

        self.currentWord = ''
        self.currentfrwd = ''
        self.currentyprob = 0
        self.currentnumtry = 0

        self.englishDict = {}
        self.toLang = "French"
        self.fromLang = "English"
        self.makeAchievements()


    def makeAchievements(self):

        print("Called Achievements!")

        self.TranslateLabel = tk.LabelFrame(self.achieveFrame,
                                            text="Translate Things",
                                            width=30)
        self.refresh = tk.LabelFrame(self.achieveFrame,
                                     text="",
                                     width=30)
        self.nearAchieveTrans = tk.Label(self.TranslateLabel,
                                         textvariable=self.nearTransVar)

        self.nearTransVar.set("Nearest Achievement here")

        self.refreshButton = tk.Button(self.refresh,
                                       text="Refresh",
                                       command=self.checkAchieve)

        self.checkAchieve()

        self.achieveFrame.grid(column=2, row=2)
        self.nearAchieveTrans.grid(column=2,row=4)
        self.TranslateLabel.grid(column=2, row=3)
        self.refresh.grid(column=4,row=4)
        self.refreshButton.grid(column=4,row=5)

    def checkAchieve(self):
        self.nearTransVar.set("Closest Achievement: Easy Peasy ")
        print("refresh here.. . .. .")





