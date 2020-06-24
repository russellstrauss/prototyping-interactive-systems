from tkinter import Tk
from Wizard import Wizard
from LikertStep import LikertStep

class LikertWizard(Wizard):
	def __init__(self, parent, data):
		super().__init__(parent, data)
		steps = [LikertStep(self, self.data, "LTURT", "I like turtles"),
				LikertStep(self, self.data, "LFUN", "This is fun"),
				LikertStep(self, self.data, "LPEA", "I ate a peanut")]

		self.set_steps(steps)
		self.start()

if __name__ == "__main__":
	root = Tk()

	data = {}
	my_gui = LikertWizard(root, data)
	my_gui.pack()

	root.mainloop()
