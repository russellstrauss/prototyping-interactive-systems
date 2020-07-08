from Wizard import Step, Wizard
from tkinter import *
from datetime import datetime

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
		lbl1 = Label(self, text=self.step_label, font="bold")
		lbl1.pack(side="top", fill="x", padx=5, pady=5)
	
		my_frame = Frame(self, width=825)
		my_frame = set_up_participant_info(self, my_frame)
		my_frame.pack(padx=15, pady=15)

		self.data[self.stepname]["step_label"] = self.step_label
	
	def updateChecklist(self, field_label, state):
		self.data[self.stepname][field_label] = state
	
	def updateEntry(self, field_label, field_input_text):
		self.data[self.stepname][field_label] = field_input_text.get()