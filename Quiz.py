# TODO Make this run off of the main.py
# TODO Add yprob system...
# TODO An achievement system

"""
Y prob system:

1. yprob is from 0-100 all words start at 100
2. random chance 0-100 if under yprob it is chosen
3. if none are chosen after ten times, choose a random one
4. if right, half the chance (100 to 50 yprob)
5. if wrong, double the chance (12.5 to 25 yprob)
6. Once all words are 12.5 or 6, add an new word.

"""
import time
import random
import Translate
from difflib import SequenceMatcher
import tkinter as tk
import csv
from unidecode import unidecode
from tkinter import ttk

import json
gSmallWindow = "350x350"

class Quiz:
    def __init__(self, app, parent):
        self.parent = parent
        self.app = app
        self.toDrop = None
        self.fromDrop = None
        self.difficultyLevel = None
        self.entry = None
        self.output = None
        self.level = None
        self.points = None
        self.yprobAverage = tk.StringVar()
        self.levelVar = tk.StringVar()
        self.pointsVar = tk.StringVar()
        self.entryVar = tk.StringVar()
        self.diffOption = tk.StringVar()
        self.toDropOption = tk.StringVar()
        self.fromDropOption = tk.StringVar()
        self.labelVar = tk.StringVar()
        self.numRightVar = tk.StringVar()
        self.numWrongVar = tk.StringVar()
        self.numAverageVar = tk.StringVar()

        self.quizFrame = tk.Frame(self.parent)

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
        self.readCSV()
        self.makeQuiz()

    def confirmSettings(self):
        self.toLang = self.toDropOption.get()
        self.fromLang = self.fromDropOption.get()
        diff = self.diffOption.get()
        if diff == 'Easy':
            self.difficulty = self.difficulties["Easy"]
        elif diff == 'Medium':
            self.difficulty = self.difficulties["Medium"]
        elif diff == 'Hard':
            self.difficulty = self.difficulties["Hard"]

        print(self.fromLang + " to " + self.toLang + " confirmed!")
        print(str(self.difficulty) + " difficulty level confirmed!")

    def gainPoint(self, point):
        # run once the player has completed a word
        if self.difficulty == self.difficulties["Easy"]:
            self.pointValue += point
        if self.difficulty == self.difficulties["Medium"]:
            self.pointValue += (point + (point / 2))
        if self.difficulty == self.difficulties["Hard"]:
            self.pointValue += point * 2
        while self.pointValue >= (self.levelValue + 5):
            self.levelValue += 1
            self.pointValue -= (self.levelValue + 5)
            if self.pointValue < 0:
                self.pointValue = 0

        self.pointsVar.set(self.pointValue)
        self.levelVar.set(self.levelValue)

        self.updateValue()

    def makeQuiz(self):

        print("Called MakeQuiz!")

        self.playLabel = tk.LabelFrame(self.quizFrame, text="Quiz")
        self.fromLabel = tk.LabelFrame(self.quizFrame, text="from", width=20)
        self.toLabel = tk.LabelFrame(self.quizFrame, text="to", width=20)
        self.settingsLabel = tk.LabelFrame(self.quizFrame, text="Settings", width=20)
        self.levelLabel = tk.LabelFrame(self.quizFrame, text="Level", width=20)
        self.pointsLabel = tk.LabelFrame(self.quizFrame, text="Points", width=20)
        self.pbLabel = tk.LabelFrame(self.quizFrame, text="Level Progress", width=20)
        self.statsLabel = tk.LabelFrame(self.quizFrame, text="Statistics",width=20)

        self.toDrop = ttk.Combobox(self.toLabel, textvariable=self.toDropOption, values=Translate.Translate.langList)
        self.toDropOption.set("To")

        self.fromDrop = ttk.Combobox(self.fromLabel, textvariable=self.fromDropOption,
                                     values=Translate.Translate.langList)
        self.fromDropOption.set("From")

        self.difficultyLevel = tk.OptionMenu(self.settingsLabel, self.diffOption,
                                             'Easy', 'Medium', 'Hard')

        self.confirmSettings = tk.Button(self.settingsLabel,
                                         text=u"Confirm",
                                         command=self.confirmSettings)

        self.enterTrans = tk.Button(self.playLabel,
                                    text=u"Enter",
                                    command=self.entertran)

        self.getword = tk.Button(self.settingsLabel,
                                 text="Get Word",
                                 command=self.getWord)

        self.openStats = tk.Button(self.settingsLabel,
                                   text="Show stat",
                                   command=self.makeStatistics)

        self.entry = tk.Entry(self.playLabel, textvariable=self.entryVar)

        self.output = tk.Label(self.playLabel, textvariable=self.labelVar)

        self.level = tk.Label(self.levelLabel, textvariable=self.levelVar)

        self.points = tk.Label(self.pointsLabel, textvariable=self.pointsVar)


        self.levelVar.set("1")
        self.pointsVar.set("0")
        self.entryVar.set("Answer here!")
        self.labelVar.set("Word to Translate here!")

        self.toDropOption.set("French")
        self.fromDropOption.set("English")
        self.diffOption.set("Medium")

        self.toDrop.configure(width=11)
        self.fromDrop.configure(width=11)
        self.difficultyLevel.configure(width=11)
        self.confirmSettings.configure(width=11)
        self.level.configure(width=11)
        self.points.configure(width=11)
        self.entry.configure(width=20)
        self.output.configure(width=20)
        self.getword.configure(width=20)

        self.quizFrame.grid(column=1, row=1)
        self.toDrop.grid(column=2, row=1, sticky="ew")  # First dropbox
        self.fromDrop.grid(column=0, row=1, sticky="ew")
        self.fromLabel.grid(column=0, row=2)
        self.statsLabel.grid(column=2,row=3)
        self.toLabel.grid(column=2, row=2)
        self.difficultyLevel.grid(column=1, row=3)
        self.settingsLabel.grid(column=1, row=3)
        self.levelLabel.grid(column=0, row=3)
        self.pointsLabel.grid(column=0, row=4)
        self.confirmSettings.grid(column=2, row=3)
        self.getword.grid(column=4, row=3)
        self.openStats.grid(column=5, row=3)

        self.playLabel.grid(column=1, row=4)
        self.entry.grid(column=1, row=5)
        self.enterTrans.grid(column=2, row=5)
        self.output.grid(column=1, row=6)
        self.level.grid(column=0, row=4)

        initialValue = 0  # Inital value of Progress Bar

        self.maxValue = self.levelValue + 5  # TODO Maybe make a better version of this?

        fullText = "Points "

        # Create a LabelFrame to hold this points bar
        self.pointsFrame = tk.LabelFrame(self.quizFrame, text=fullText, borderwidth=1, relief="sunken")

        # Setup the progress bar
        self.value = tk.DoubleVar()
        self.value.set(initialValue)
        self.valuetext = tk.StringVar()
        self.valuetext.set(str(initialValue))

        self.pbcanvas = tk.Canvas(self.pointsFrame, relief=tk.FLAT, width=120, height=5)
        s = ttk.Style()
        s.theme_use('alt')
        s.configure("white" + ".points.Horizontal.TProgressbar", foreground="black", background="orange")
        self.pb = ttk.Progressbar(self.pbcanvas, variable=self.value,
                                  style="white" + ".points.Horizontal.TProgressbar",
                                  orient="horizontal", max=self.levelValue + 5, length=120,
                                  value=initialValue, mode="determinate")
        self.pb.grid(column=5, row=4)

        self.pbcanvas.create_window(1, 1, anchor=tk.NW, window=self.pb)
        self.pbcanvas.grid(row=5, column=4)
        self.pointsFrame.grid(row=4, column=0)

        self.pointsTextLabel = tk.Label(self.pointsFrame, textvariable=self.valuetext)
        self.pointsTextLabel.config(width=6, font=("Courier", 11))
        self.pointsTextLabel.grid(row=4, column=5)

    def __del__(self):
        self.pointsFrame.destroy()

    @staticmethod
    def similar(a, b):
        return SequenceMatcher(None, a, b).ratio()

    def updateValue(self):
        value = self.pointValue
        self.value.set(value)
        self.valuetext.set(str("{0:.1f}".format(round(value, 1))))

    def averageyProb(self):
        list = []
        for e in self.englishDict.items():
            randomDict = e
            englishword, data = randomDict
            frenchWord, yprob, numTries = data
            list.append(int(yprob))
            newsum = sum(list)
            average = newsum / len(list)
            average = round(average, 3)
            self.yprobAverage.set(average)

    def makeStatistics(self):
        """
        ..
        ..
        Makes statistics in a new window, all labels with a refresh button to update all
        .. current stats: average yprob, number of correct times number of wrong answers average right/wrong
        ..

        """
        # TODO: [WIP] Make stats for game. yprob for current average yprob
        # TODO: [not started ] Make achievements
        # TODO: [WIP] a more detailed display by pressing a button opening a new window
        # TODO: [WIP] Put all this into a seperate tk window


        self.stats = tk.Toplevel()
        self.stats.title('Statistics')
        self.stats.geometry(gSmallWindow)
        self.frame = tk.LabelFrame(self.stats,text="Settings")
        self.stats.bind('<Return>', lambda e: self.refreshStats())
        self.text = tk.Message(self.frame, text="Statistics")

        self.yprobDisplay = tk.Label(self.stats, textvariable=self.yprobAverage)

        self.numRightDisplay = tk.Label(self.stats, textvariable=self.numRightVar)

        self.numWrongDisplay = tk.Label(self.stats, textvariable=self.numWrongVar)

        self.numAverageDisplay = tk.Label(self.stats, textvariable=self.numAverageVar)
        # Make labels

        # Grab the average yprob from here.


        self.frame.grid(column=0,row=0)
        self.yprobDisplay.grid(column=0,row=1)
        self.numRightDisplay.grid(column=0,row=2)

        pass
    def refreshStats(self):
        """
        Put functions here with a set to the correspondant label.

        :return:
        """
        self.numRightVar.set(str(self.numRight))
        self.numWrongVar.set(str(self.numWrong))
        self.rightWrongAverage()
        self.averageyProb()
        pass

    def rightWrongAverage(self):
        average = self.numRight / self.numWrong
        self.numAverageVar.set(str(average))




    def readCSV(self):
        # Run only once!
        with open('EBEnglishToFrenchVocab.csv') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                self.englishDict[row['English']] = (row["French"], 100, 0)
                print("done with " + str(row))

    def getrandomWord(self):


        chanceofWord = random.randint(1, 100)
        tried = 0
        gotWord = False
        while gotWord == False:
            randomDict = random.choice(list(self.englishDict.items()))
            englishword, data = randomDict
            frenchWord, yprob, numTries = data
            tried += 1
            if yprob <= chanceofWord or tried == 10:
                gotWord = True
                # Receive and store all values
                self.currentWord = str(englishword)
                self.currentfrwd = str(frenchWord)
                self.currentyprob = yprob
                self.currentnumtry = numTries


    def getWord(self):
        self.getrandomWord()
        self.labelVar.set(self.currentWord)

    def entertran(self):
        answer = self.entryVar.get()
        answer = answer.lower()

        trans = self.currentfrwd.lower()

        exact = answer == trans
        sim = (self.similar(answer,unidecode(trans)))
        similar = (0.75 <= sim)
        print(str(sim) + " percentage right")

        unicorrect = answer == unidecode(trans)
        easyMode = self.difficulties == self.difficulties["Easy"]
        if exact or ((unicorrect or similar) and easyMode):
            print("")
            # calculate humor and yprob + numtries
            self.currentyprob /= 2
            self.currentyprob = int(self.currentyprob)  # safety measure
            self.currentnumtry += 1
            print(str(self.currentyprob) + " new yprob")
            print(str(self.currentnumtry) + " new numtry")
            self.englishDict[self.currentWord] = (self.currentfrwd, self.currentyprob, self.currentnumtry)
            print(self.englishDict[self.currentWord])
            pointval = 1
            self.gainPoint(pointval)
            time.sleep(5)
            self.getWord()
            self.numRight += 1
            self.numRightVar.set(str(self.numRight))


        elif unicorrect or similar:
            print("So close! Partial credit!")
            self.currentyprob /= 1.5
            self.currentyprob = int(self.currentyprob)  # safety measure
            self.currentnumtry += 1
            print(str(self.currentyprob) + " new yprob")
            print(str(self.currentnumtry) + " new numtry")
            self.englishDict[self.currentWord] = (self.currentfrwd, self.currentyprob, self.currentnumtry)
            print(self.englishDict[self.currentWord])
            pointval = 0.5
            self.gainPoint(pointval)
            print("Your answer: " + answer)
            print("Right Answer: " + self.currentfrwd)
            self.labelVar.set("Right Answer: " + self.currentfrwd)
            time.sleep(5)
            self.getWord()
            self.numRight += 1

        else:
            print("Your answer: " + answer)
            print("Right Answer: " + self.currentfrwd)
            self.labelVar.set("Right Answer: " + self.currentfrwd)
            self.numWrong += 1
            self.numWrongVar.set(str(self.numWrong))
        self.tested += 1
        self.averageyProb()
        self.rightWrongAverage()



if __name__ == "__main__":
    print("Please run from main.py!")
