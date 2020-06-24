from Wizard import Step, Wizard
from LikertStep import LikertStep
from LikertWizard import LikertWizard
from tkinter import *
import json
from datetime import datetime
import os
from PIL import Image, ImageTk
# print(os.getcwd())
# print(os.listdir())

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

def set_up_participant_info(self, my_frame):
	
	current_row = 0
	
	start_time_label = Label(my_frame, text="Start Time")
	start_time_label.grid(row=current_row, sticky=W)
	start_time = str(datetime.strptime(str(datetime.now()), '%Y-%m-%d %H:%M:%S.%f'))
	start_time_timestamp = Label(my_frame, text=start_time)
	start_time_timestamp.grid(row=current_row, column=1, sticky=E)
	current_row += 1
	
	participant_id_label = Label(my_frame, text="Participant ID")
	session_id_label = Label(my_frame, text="Session ID")
	participant_id_stringvar = StringVar()
	participant_id_stringvar.trace("w", lambda name, index, mode, sv=participant_id_stringvar: self.updateEntry("participant_id", participant_id_stringvar))
	participant_id_input = Entry(my_frame, textvariable=participant_id_stringvar)
	session_id_stringvar = StringVar()
	session_id_stringvar.trace("w", lambda name, index, mode, sv=session_id_stringvar: self.updateEntry("session_id", session_id_stringvar))
	session_id_input = Entry(my_frame, textvariable=session_id_stringvar)
	participant_id_label.grid(row=current_row, sticky=W)
	participant_id_input.grid(row=current_row, column=1, sticky=E)
	current_row += 1
	session_id_label.grid(row=current_row, sticky=W)
	session_id_input.grid(row=current_row, column=1, sticky=E)
	current_row += 1

	col_count, row_count = my_frame.grid_size()
	for col in range(col_count):
		my_frame.grid_columnconfigure(col, minsize=20)

	for row in range(row_count):
		my_frame.grid_rowconfigure(row, minsize=30)
		
	return my_frame

class ParticipantInfo(Step):
	def __init__(self, parent, data, stepname, step_label):
		super().__init__(parent, data, stepname)

		self.step_label = step_label
		lbl1 = Label(self, text=self.step_label)
		lbl1.pack(side="top", fill="x", padx=5, pady=5)
	
		my_frame = Frame(self)
		my_frame = set_up_participant_info(self, my_frame)
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

def set_up_memorization(self, my_frame):
	
	fry_image = Image.open("img/fry_200.jpg")
	fry_photo = ImageTk.PhotoImage(fry_image)
	farnsworth_image = Image.open("img/farnsworth_200.jpg")
	farnsworth_photo = ImageTk.PhotoImage(farnsworth_image)
	bender_image = Image.open("img/bender_200.png")
	bender_photo = ImageTk.PhotoImage(bender_image)
	zoidberg_image = Image.open("img/zoidberg_200.jpg")
	zoidberg_photo = ImageTk.PhotoImage(zoidberg_image)
	
	fry_image_label = Label(my_frame, image=fry_photo)
	fry_image_label.image = fry_photo
	zoidberg_image_label = Label(my_frame, image=zoidberg_photo)
	zoidberg_image_label.image = zoidberg_photo
	bender_image_label = Label(my_frame, image=bender_photo)
	bender_image_label.image = bender_photo
	farnsworth_image_label = Label(my_frame, image=farnsworth_photo)
	farnsworth_image_label.image = farnsworth_photo
	
	Button(my_frame, image=fry_photo).grid(row=0, column=1, padx=10, pady=10)
	Button(my_frame, text='2', image=farnsworth_photo).grid(row=1, column=0, padx=10, pady=10)
	Button(my_frame, text='3', image=bender_photo).grid(row=1, column=2, padx=10, pady=10)
	Button(my_frame, text='4', image=zoidberg_photo).grid(row=2, column=1, padx=10, pady=10)

	return my_frame

class MemorizationStep(Step):
	def __init__(self, parent, data, stepname, page_label):
		super().__init__(parent, data, stepname)

		self.page_label = page_label
		lbl1 = Label(self, text=self.page_label)
		lbl1.pack(side="top", fill="x")

		my_frame = Frame(self)
		my_frame = set_up_memorization(self, my_frame)
		my_frame.pack(padx=10, pady=10)

		self.data[self.stepname]["page_label"] = self.page_label
		# self.data[self.stepname]["likert_score"] = likertscale.get()

	def updateValue(self, event):
		self.data[self.stepname]["likert_score"] = event


class MyWizard(Wizard):
	def __init__(self, parent, data):
		super().__init__(parent, data)
		steps = [
					MemorizationStep(self, self.data, "memorization", "Memorization Analysis"),
					ParticipantInfo(self, self.data, "initialization", "Participant Info")
				]
		self.set_steps(steps)
		self.start()

data = {}
my_gui = MyWizard(root, data)
my_gui.pack()

root.mainloop()