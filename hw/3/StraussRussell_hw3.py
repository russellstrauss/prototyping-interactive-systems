from Wizard import Step, Wizard
from datetime import datetime
from tkinter import *
import json

root = Tk()
# root.minsize(825, 100)

def set_up_participant_info(self, my_frame):
	
	current_row = 0
	start_time_label = Label(my_frame, text="Start Time")
	start_time_label.grid(row=current_row, sticky=W)
	start_time = str(datetime.strptime(str(datetime.now()), '%Y-%m-%d %H:%M:%S.%f'))
	start_time_timestamp = Label(my_frame, text=start_time)
	start_time_timestamp.grid(row=current_row, column=1, sticky=E, columnspan=2)
	current_row += 1
	self.data["start_time"] = start_time
	
	first_name_label = Label(my_frame, text="First Name")
	last_name_label = Label(my_frame, text="Last Name")
	first_name_stringvar = StringVar()
	first_name_stringvar.trace("w", lambda name, index, mode, sv=first_name_stringvar: self.updateEntry("firstname", first_name_stringvar))
	first_name_input = Entry(my_frame, textvariable=first_name_stringvar)
	last_name_stringvar = StringVar()
	last_name_stringvar.trace("w", lambda name, index, mode, sv=last_name_stringvar: self.updateEntry("lastname", last_name_stringvar))
	last_name_input = Entry(my_frame, textvariable=last_name_stringvar)
	first_name_label.grid(row=current_row, sticky=W)
	first_name_input.grid(row=current_row, column=1, sticky=E, columnspan=2)
	current_row += 1
	last_name_label.grid(row=current_row, sticky=W)
	last_name_input.grid(row=current_row, column=2, sticky=E)
	current_row += 1
	
	gender_label = Label(my_frame, text="Gender")
	gender_selection = StringVar()
	gender_selection.trace("w", lambda name, index, mode, sv=gender_selection: self.updateEntry("gender", gender_selection))
	male_option = Radiobutton(my_frame, text="Male", variable=gender_selection, value="male")
	female_option = Radiobutton(my_frame, text="Female", variable=gender_selection, value="female")
	gender_selection.set("no response")
	gender_label.grid(row=current_row, column=0, sticky=W)
	male_option.grid(row=current_row, column=1, sticky=E)
	female_option.grid(row=current_row, column=2, sticky=E)
	current_row += 1

	age_label = Label(my_frame, text="Age")
	age_label.grid(row=current_row, column=0, sticky=W)
	age_intvar = IntVar()
	age_intvar.trace("w", lambda name, index, mode, sv=age_intvar: self.updateEntry("age", age_intvar))
	age_spinbox = Spinbox(my_frame, from_=10, to=99, textvariable=age_intvar)
	age_spinbox.config(font=("times", 16))
	age_spinbox.grid(row=current_row, column=1, sticky=E, columnspan=2)
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
		lbl1 = Label(self, text=self.step_label, font="bold")
		lbl1.pack(side="top", fill="x", padx=5, pady=5)
	
		my_frame = Frame(self, width=825)
		my_frame = set_up_participant_info(self, my_frame)
		my_frame.pack(padx=15, pady=15)

		self.data["step_label"] = self.step_label
	
	def updateEntry(self, field_label, field_input_text):
		self.data[field_label] = field_input_text.get()

class MyWizard(Wizard):
	def __init__(self, parent, data):
		super().__init__(parent, data)
		steps = [
			ParticipantInfo(self, self.data, "initialization", "Participant Info")
		]
			
		self.set_steps(steps)
		self.start()

data = {}
my_gui = MyWizard(root, data)
my_gui.pack()
root.mainloop()