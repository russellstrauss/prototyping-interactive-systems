from Wizard import Step, Wizard
from LikertStep import LikertStep
from LikertWizard import LikertWizard
from tkinter import *
import json

root = Tk()
root.minsize(425, 100)

class Checklist(Frame):
	def __init__(self, step, group_label, parent=None, picks=[], side=LEFT, anchor=W):
		Frame.__init__(self, parent)
		self.vars = []
		self.labels = []
		self.state = {}
		
		for index, pick in enumerate(picks):
			var = IntVar()
			chk = Checkbutton(self, text=pick, variable=var, command=lambda: step.updateChecklist(group_label, self.getState()))
			chk.grid(row=index, column=0, sticky=W)
			self.labels.append(pick)
			self.vars.append(var)
	
	def getState(self):
		self.state = {}
		for index, item in enumerate(self.labels):
			self.state[item] = self.vars[index].get()
		return self.state

def set_up_demographics(self, demographics_frame):
	current_row = 0
	first_name_label = Label(demographics_frame, text="First Name")
	last_name_label = Label(demographics_frame, text="Last Name")
	
	first_name_stringvar = StringVar()
	first_name_stringvar.trace("w", lambda name, index, mode, sv=first_name_stringvar: self.updateEntry("first_name", first_name_stringvar))
	first_name_input = Entry(demographics_frame, textvariable=first_name_stringvar)
	
	last_name_stringvar = StringVar()
	last_name_stringvar.trace("w", lambda name, index, mode, sv=last_name_stringvar: self.updateEntry("last_name", last_name_stringvar))
	last_name_input = Entry(demographics_frame, textvariable=last_name_stringvar)
	
	first_name_label.grid(row=current_row, sticky=W)
	first_name_input.grid(row=current_row, column=1, sticky=E)
	current_row += 1
	last_name_label.grid(row=current_row, sticky=W)
	last_name_input.grid(row=current_row, column=1, sticky=E)
	current_row += 1

	gender_label = Label(demographics_frame, text="Gender")
	gender_selection = StringVar()
	gender_selection.trace("w", lambda name, index, mode, sv=gender_selection: self.updateEntry("gender", gender_selection))
	male_option = Radiobutton(demographics_frame, text="Male", variable=gender_selection, value="male")
	female_option = Radiobutton(demographics_frame, text="Female", variable=gender_selection, value="female")
	gender_selection.set("no response")
	gender_label.grid(row=current_row, column=0, sticky=W, rowspan=2)
	male_option.grid(row=current_row, column=1, sticky=E)
	current_row += 1
	female_option.grid(row=current_row, column=1, sticky=E)
	current_row += 1
	
	age_label = Label(demographics_frame, text="Age")
	age_label.grid(row=current_row, column=0, sticky=W)
	age_intvar = IntVar()
	age_intvar.trace("w", lambda name, index, mode, sv=age_intvar: self.updateEntry("age", age_intvar))
	age_spinbox = Spinbox(demographics_frame, from_=10, to=99, textvariable=age_intvar)
	age_spinbox.config(font=("times", 16))
	age_spinbox.grid(row=current_row, column=1, sticky=E)
	current_row += 1

	meal_label = Label(demographics_frame, text="Preferred meal")
	meal_select_value = StringVar()
	meal_select_value.set("chicken")
	meal_option_menu = OptionMenu(demographics_frame, meal_select_value, "chicken", "beef", "vegetarian")
	meal_label.grid(row=current_row, column=0, sticky=W)
	meal_option_menu.grid(row=current_row, column=1, sticky=E, pady=20)
	current_row += 1

	dessert_options_label = Label(demographics_frame, text="Select dessert options")
	dessert_options_label.grid(row=current_row, column=0, sticky=W)
	dessert_options = Checklist(self, "dessert_options", demographics_frame, ['Ice Cream', 'Popsicle', 'Cake', 'Cookie'])
	dessert_options.grid(row=current_row, column=1, sticky=E)
	current_row += 1

	col_count, row_count = demographics_frame.grid_size()
	for col in range(col_count):
		demographics_frame.grid_columnconfigure(col, minsize=20)

	for row in range(row_count):
		demographics_frame.grid_rowconfigure(row, minsize=30)
		
	return demographics_frame

class DemographicStep(Step):
	def __init__(self, parent, data, stepname, step_label):
		super().__init__(parent, data, stepname)

		self.step_label = step_label
		lbl1 = Label(self, text=self.step_label)
		lbl1.pack(side="top", fill="x", padx=5, pady=5)
	
		my_frame = Frame(self)
		my_frame = set_up_demographics(self, my_frame)
		my_frame.pack(padx=15, pady=15)

		self.data[self.stepname]["step_label"] = self.step_label
	
	def updateChecklist(self, field_label, state):
		self.data[self.stepname][field_label] = state
	
	def updateEntry(self, field_label, field_input_text):
		self.data[self.stepname][field_label] = field_input_text.get()

def set_up_multiple_choice(self, my_frame):
	
	current_row = 0
	question_stringvar = StringVar()
	question_stringvar.trace("w", lambda name, index, mode, sv=question_stringvar: self.updateEntry("question", question_stringvar))
	
	question_label = Label(my_frame, text=self.question)
	question_label.grid(row=current_row, column=0)
	current_row += 1
	answer_selection = StringVar()
	answer_selection.trace("w", lambda name, index, mode, sv=answer_selection: self.updateEntry("user_response", answer_selection))
	
	radio_buttons = []
	alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
	for index, item in enumerate(self.options):
		radio_option = Radiobutton(my_frame, text=alphabet[index] + ". " + item, variable=answer_selection, value=item)
		radio_buttons.append(radio_option)
		radio_option.grid(row=current_row, column=0, sticky=W)
		current_row += 1
		
	answer_selection.set("no response")
	
	return my_frame

class MultipleChoiceStep(Step):
	def __init__(self, parent, data, stepname, step_label, question, options, answer):
		super().__init__(parent, data, stepname)

		self.step_label = step_label
		lbl1 = Label(self, text=self.step_label)
		lbl1.pack(side="top", fill="x", padx=5, pady=5)
		self.question = question
		self.options = options
		self.answer = answer
	
		my_frame = Frame(self)
		my_frame = set_up_multiple_choice(self, my_frame)
		my_frame.pack(padx=10, pady=10)

		self.data[self.stepname]["step_label"] = self.step_label
		self.data[self.stepname]["question"] = self.question
		self.data[self.stepname]["options"] = self.options
		self.data[self.stepname]["answer"] = self.answer

	def updateEntry(self, field_label, field_input_text):
		self.data[self.stepname][field_label] = field_input_text.get()

def set_up_multiselect(self, my_frame):
	
	current_row = 0
	question_label = Label(my_frame, text=self.question)
	question_label.grid(row=current_row, column=0)
	current_row += 1
	
	answer_selection = StringVar()
	answer_selection.trace("w", lambda name, index, mode, sv=answer_selection: self.updateChecklist("user_response", answer_selection))

	options = Checklist(self, "user_response", my_frame, self.options)
	options.grid(row=current_row, column=0, sticky=E)
		
	answer_selection.set("no response")
	return my_frame
		
class MultiselectStep(Step):
	def __init__(self, parent, data, stepname, step_label, question, options):
		super().__init__(parent, data, stepname)

		self.step_label = step_label
		lbl1 = Label(self, text=self.step_label)
		lbl1.pack(side="top", fill="x", padx=5, pady=5)
		self.question = question
		self.options = options
	
		my_frame = Frame(self)
		my_frame = set_up_multiselect(self, my_frame)
		my_frame.pack(padx=10, pady=10)

		self.data[self.stepname]["step_label"] = self.step_label
		self.data[self.stepname]["question"] = self.question
		self.data[self.stepname]["options"] = self.options
	
	def updateChecklist(self, field_label, state):
		self.data[self.stepname][field_label] = state
		
	def updateEntry(self, field_label, field_input_text):
		self.data[self.stepname][field_label] = field_input_text.get()

class MyWizard(Wizard):
	def __init__(self, parent, data):
		super().__init__(parent, data)
		steps = [
					DemographicStep(self, self.data, "demographics", "Demographics Section"),
					LikertStep(self, self.data, "distressed", "I feel distressed", "(1=not at all, 2=a litte, 3=moderately, 4=quite a bit, 5=extremely)"),
					MultipleChoiceStep(self, self.data, "multiple-choice", "Animal Quiz", "How long can the American lobster live?", ["5 years", "20 years", "50 years", "100 years"], "100 years"),
					MultiselectStep(self, self.data, "multiselect", "Music Preference", "Which artists do you like?", ["Pink Floyd", "Kay Perry","OutKast", "Willie Nelson"])
				]
		self.set_steps(steps)
		self.start()

data = {}
my_gui = MyWizard(root, data)
my_gui.pack()

root.mainloop()