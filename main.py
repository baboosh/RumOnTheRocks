#
#
# Translator MAIN for translating, requires two other files (translations and supported) to function.
# Also requires translate, "pip install translate" into commandline should do it.
# Made by Max Bethke at Tech Tree Labs
#
# TODO If french vocab is in a spreadsheet, save to csv then dict then json
# TODO Have fun.

import json
from tkinter import ttk
import os
import tkinter as tk
from difflib import SequenceMatcher
from PIL import Image, ImageTk
import Translate
import Achievements
import Quiz
import translations  # Import translations.py

gInitialGeomtery = "950x498"


class SimpleAppTk(tk.Frame):


    def __init__(self, master=None):
        self.mainFrame = tk.Frame.__init__(self, master)
        self.master = master
        self.screenWidth, self.screenHeight = int(gInitialGeomtery.split("x")[0]), int(gInitialGeomtery.split("x")[1])

        self.quiz = None
        self.translate = None
        self.achievement = None
        self.states = {"None": 0, "Translate": 1, "Quiz": 2,"Achievement":3}
        self.state = self.states["Translate"]

        self.backgroundImage = None
        self.backgroundImageLabel = None

        # self.drawBackground()
        self.switchMode()
        self.updateUX()  # Initialize the UX elements

    # stays in main.py
    def drawBackground(self):
        image = Image.open("./tower.png").convert("RGB")
        image = image.resize((self.screenWidth, self.screenHeight), Image.ANTIALIAS)
        self.backgroundImage = ImageTk.PhotoImage(image)
        self.backgroundImageLabel = tk.Label(self.mainFrame, image=self.backgroundImage)
        self.backgroundImageLabel.place(x=0, y=0, relwidth=1, relheight=1)
        print("tried to draw bg")

    # Stays in main.py
    def updateUX(self):  # Initialize function
        self.drawBackground()
        self.changeModeButton = tk.Button(self.mainFrame,
                                          text=u"Switch Modes",
                                          command=self.switchMode)
        self.changeModeButton.grid(column=0, row=0)

        if self.state == self.states["Translate"]:
            print("Translate, Please press Switch Modes")

        elif self.state == self.states["Quiz"]:
            print("Quiz, please switch modes")




    # Stays in main.py
    def switchMode(self):
        self.master.title('Translator')
        print("Switching Modes!")
        if self.state == self.states["Translate"]:
            if self.translate is None:
                self.translate = Translate.Translate(self, self.mainFrame)
                print("translate frame is none")
                print("did not switch")
            else:
                print("Switched to Quiz")
                self.translate.translateFrame.destroy()
                self.master.title("Quiz")
                self.state = self.states["Quiz"]
                self.quiz = Quiz.Quiz(self, self.mainFrame)


        elif self.state == self.states["Quiz"]:
            if self.quiz is None:
                print("quiz frame is none")
                self.quiz = Quiz.Quiz(self, self.mainFrame)
            else:
                print("Switched to Achievement")
                self.quiz.quizFrame.destroy()
                self.master.title('Achievement')
                self.state = self.states["Achievement"]
                self.achievement = Achievements.Achievement(self, self.mainFrame)
        elif self.state == self.states["Achievement"]:
            if self.achievement is None:
                self.achievement = Achievements.Achievement(self ,self.mainFrame)
                print("achievement frame is none")
            else:
                print("Switched to Translate")
                self.achievement.achieveFrame.destroy()
                self.master.title('Translator')
                self.state = self.states["Translate"]
                self.translate = Translate.Translate(self, self.mainFrame)


if __name__ == "__main__":
    root = tk.Tk()
    root.geometry(gInitialGeomtery)
    trans = translations.Translations
    app = SimpleAppTk(root)
    app.mainloop()
