from tkinter import Tk, Label, Radiobutton, Button, StringVar, Entry, Scale, IntVar, END, W, E, HORIZONTAL, LEFT, Frame, SUNKEN
from Wizard import Step

class LikertStep(Step):
	def __init__(self, parent, data, stepname, statement, number_labels="(1=Strongly Disagree, 2=Disagree, 3=Neutral, 4=Agree, 5=Strongly Agree)"):
		super().__init__(parent, data, stepname)

		self.statement = statement
		lbl1 = Label(self, text=self.statement)
		lbl1.pack(side="top", fill="x")

		lbl2 = Label(self, text=number_labels)
		
		lbl2.pack()
		likertscale = Scale(self, from_=1, to=5, length=200, tickinterval=1, orient=HORIZONTAL, command=self.updateValue)
		likertscale.set(3)
		likertscale.pack()

		self.data[self.stepname]["statement"] = self.statement
		self.data[self.stepname]["likert_score"] = likertscale.get()

	def updateValue(self, event):
		self.data[self.stepname]["likert_score"] = event
