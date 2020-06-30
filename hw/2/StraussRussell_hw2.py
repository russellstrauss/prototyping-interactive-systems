from Wizard import Step, Wizard
from LikertStep import LikertStep
from LikertWizard import LikertWizard
from tkinter import *
import json
from PIL import Image, ImageTk
from playsound import playsound
import random
from SimonStep import SimonStep
from ParticipantInfo import ParticipantInfo

root = Tk()
root.minsize(825, 100)

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
	
		my_frame = Frame(self, width=825)
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
		lbl1 = Label(self, text=self.step_label, font="bold")
		lbl1.pack(side="top", fill="x", padx=5, pady=5)
		self.question = question
		self.options = options
	
		my_frame = Frame(self, width=825)
		my_frame = set_up_multiselect(self, my_frame)
		my_frame.pack(padx=10, pady=10)

		self.data[self.stepname]["step_label"] = self.step_label
		self.data[self.stepname]["question"] = self.question
		self.data[self.stepname]["options"] = self.options
	
	def updateChecklist(self, field_label, state):
		self.data[self.stepname][field_label] = state
		
	def updateEntry(self, field_label, field_input_text):
		self.data[self.stepname][field_label] = field_input_text.get()

def set_up_tlx(self, my_frame):
	
	current_row = 0
	mental_demand_label = Label(my_frame, text="Mental Demand", font="bold", pady=10)
	mental_demand_label.grid(row=current_row, sticky=W)
	current_row += 1
	mental_demand_description = Message(my_frame, text="How much mental and perceptual activity was required? Was the task easy or demanding, simple or complex, exacting or forgiving?", width=825)
	mental_demand_description.grid(row=current_row, sticky=W)
	
	current_row += 1
	mental_demand_scale = Scale(my_frame, from_=0, to=100, length=800, tickinterval=5, orient=HORIZONTAL, command=self.updateMentalDemand)
	mental_demand_scale.set(50)
	mental_demand_scale.grid(row=current_row, sticky=W)
	current_row += 1
	low_label = Label(my_frame, text="Low")
	high_label = Label(my_frame, text="High")
	low_label.grid(row=current_row, sticky=W)
	high_label.grid(row=current_row, sticky=E)
	current_row += 1
	
	physical_demand_label = Label(my_frame, text="Physical Demand", font="bold", pady=10)
	physical_demand_label.grid(row=current_row, sticky=W)
	current_row += 1
	physical_demand_description = Message(my_frame, text="How much physical activity was required? Was the task easy or demanding, slow or brisk, slack or strenuous, restful or laborious?", width=825)
	physical_demand_description.grid(row=current_row, sticky=W)
	current_row += 1
	physical_demand_scale = Scale(my_frame, from_=0, to=100, length=800, tickinterval=5, orient=HORIZONTAL, command=self.updatePhysicalDemand)
	physical_demand_scale.set(50)
	physical_demand_scale.grid(row=current_row, sticky=W)
	current_row += 1
	low_label = Label(my_frame, text="Low")
	high_label = Label(my_frame, text="High")
	low_label.grid(row=current_row, sticky=W)
	high_label.grid(row=current_row, sticky=E)
	current_row += 1
	
	temporal_demand_label = Label(my_frame, text="Temporal Demand", font="bold", pady=10)
	temporal_demand_label.grid(row=current_row, sticky=W)
	current_row += 1
	temporal_demand_description = Message(my_frame, text="How much time pressure did you feel due to the rate of pace at which the tasks or task elements occurred? Was the pace slow and leisurely or rapid and frantic?", width=825)
	temporal_demand_description.grid(row=current_row, sticky=W)
	current_row += 1
	temporal_demand_scale = Scale(my_frame, from_=0, to=100, length=800, tickinterval=5, orient=HORIZONTAL, command=self.updateTemporalDemand)
	temporal_demand_scale.set(50)
	temporal_demand_scale.grid(row=current_row, sticky=W)
	current_row += 1
	low_label = Label(my_frame, text="Low")
	high_label = Label(my_frame, text="High")
	low_label.grid(row=current_row, sticky=W)
	high_label.grid(row=current_row, sticky=E)
	current_row += 1
	
	performance_label = Label(my_frame, text="Performance", font="bold", pady=10)
	performance_label.grid(row=current_row, sticky=W)
	current_row += 1
	performance_description = Message(my_frame, text="How successful do you think you were in accomplishing the goals of the task set by the experimenter (or yourself)? How satisfied were you with your performance in accomplishing these goals?", width=825)
	performance_description.grid(row=current_row, sticky=W)
	current_row += 1
	performance_scale = Scale(my_frame, from_=0, to=100, length=800, tickinterval=5, orient=HORIZONTAL, command=self.updatePerformance)
	performance_scale.set(50)
	performance_scale.grid(row=current_row, sticky=W)
	current_row += 1
	low_label = Label(my_frame, text="Low")
	high_label = Label(my_frame, text="High")
	low_label.grid(row=current_row, sticky=W)
	high_label.grid(row=current_row, sticky=E)
	current_row += 1
	
	effort_label = Label(my_frame, text="Effort", font="bold", pady=10)
	effort_label.grid(row=current_row, sticky=W)
	current_row += 1
	effort_description = Message(my_frame, text="How hard did you have to work (mentally and physically) to accomplish your level of performance?", width=825)
	effort_description.grid(row=current_row, sticky=W)
	current_row += 1
	effort_scale = Scale(my_frame, from_=0, to=100, length=800, tickinterval=5, orient=HORIZONTAL, command=self.updateEffort)
	effort_scale.set(50)
	effort_scale.grid(row=current_row, sticky=W)
	current_row += 1
	low_label = Label(my_frame, text="Low")
	high_label = Label(my_frame, text="High")
	low_label.grid(row=current_row, sticky=W)
	high_label.grid(row=current_row, sticky=E)
	current_row += 1
	
	frustration_label = Label(my_frame, text="Frustration", font="bold", pady=10)
	frustration_label.grid(row=current_row, sticky=W)
	current_row += 1
	frustration_description = Message(my_frame, text="How insecure, discouraged, irritated, stressed and annoyed versus secure, gratified, content, relaxed and complacent did you feel during the task?", width=825)
	frustration_description.grid(row=current_row, sticky=W)
	current_row += 1
	frustration_scale = Scale(my_frame, from_=0, to=100, length=800, tickinterval=5, orient=HORIZONTAL, command=self.updateFrustation)
	frustration_scale.set(50)
	frustration_scale.grid(row=current_row, sticky=W)
	current_row += 1
	low_label = Label(my_frame, text="Low")
	high_label = Label(my_frame, text="High")
	low_label.grid(row=current_row, sticky=W)
	high_label.grid(row=current_row, sticky=E)
	current_row += 1
	
	return my_frame

class TLXScaleStep(Step):
	def __init__(self, parent, data, stepname, page_label):
		super().__init__(parent, data, stepname)
		self.data["tlx-raw-rating"]["total_weighted_rating"] = 0
		self.page_label = page_label
		lbl1 = Label(self, text=self.page_label, font="bold")
		lbl1.pack(side="top", fill="x")

		my_frame = Frame(self, width=825)
		my_frame = set_up_tlx(self, my_frame)
		my_frame.pack(padx=10, pady=10)

		self.data[self.stepname]["page_label"] = self.page_label

	def updateMentalDemand(self, event):
		self.data[self.stepname]["mental_demand"] = event
	def updatePhysicalDemand(self, event):
		self.data[self.stepname]["physical_demand"] = event
	def updateTemporalDemand(self, event):
		self.data[self.stepname]["temporal_demand"] = event
	def updatePerformance(self, event):
		self.data[self.stepname]["performance"] = event
	def updateEffort(self, event):
		self.data[self.stepname]["effort"] = event
	def updateFrustation(self, event):
		self.data[self.stepname]["frustration"] = event

# Create list of pairwise comparisons with no duplicate matches, then shuffle the order
tlx_scale_factors = ["mental_demand", "physical_demand", "temporal_demand", "performance", "effort", "frustration"]
pairwise_factors = []
for i in range(len(tlx_scale_factors)):
	for j in range(i + 1, len(tlx_scale_factors)):
		if (random.randint(1, 1000) % 2 == 0): # Flip flop pair order to avoid pair order consistency
			pairwise_factors.append((tlx_scale_factors[i], tlx_scale_factors[j]))
		else:
			pairwise_factors.append((tlx_scale_factors[j], tlx_scale_factors[i]))
random.shuffle(pairwise_factors)

def set_up_tlx_ranking(self, my_frame, pair):
	
	self.data[self.stepname]["options"] = pair
	
	current_row = 0
	mental_demand_label = Label(my_frame, text="Task Factor Weighting", font="bold", pady=10)
	mental_demand_label.grid(row=current_row, sticky=W)
	current_row += 1
	mental_demand_description = Message(my_frame, text="Which NASA TLX factor do you consider to be more important for this specific task?", width=825)
	mental_demand_description.grid(row=current_row, sticky=W)
	current_row += 1
	
	answer_selection = StringVar()
	answer_selection.trace("w", lambda name, index, mode, sv=answer_selection: self.updateEntry("user_response", answer_selection))

	radio_option_1 = Radiobutton(my_frame, text=pair[0].replace("_", " "), variable=answer_selection, value=pair[0])
	radio_option_1.grid(row=current_row, column=0, sticky=W)
	current_row += 1
	
	radio_option_2 = Radiobutton(my_frame, text=pair[1].replace("_", " "), variable=answer_selection, value=pair[1])
	radio_option_2.grid(row=current_row, column=0, sticky=W)
	current_row += 1
		
	answer_selection.set("no response")
	
	return my_frame

class TLXRankStep(Step):
	def __init__(self, parent, data, stepname, page_label, pair):
		super().__init__(parent, data, stepname)

		self.page_label = page_label
		lbl1 = Label(self, text=self.page_label, font="bold")
		lbl1.pack(side="top", fill="x")
		self.options = []
		self.data["tlx-rank-weights"] = {}
		for factor in tlx_scale_factors:
			self.data["tlx-rank-weights"][factor] = 0
		self.user_response = ""

		my_frame = Frame(self, width=825)
		my_frame = set_up_tlx_ranking(self, my_frame, pair)
		my_frame.pack(padx=10, pady=10)

		self.data[self.stepname]["page_label"] = self.page_label
	
	def updateEntry(self, key, answer_selection):
		if (answer_selection.get() != "no response"):
			self.data["tlx-rank-weights"][answer_selection.get()] += 1
		self.data[self.stepname][key] = answer_selection.get()

class MyWizard(Wizard):
	def __init__(self, parent, data):
		super().__init__(parent, data)
		steps = [
					ParticipantInfo(self, self.data, "initialization", "Participant Info")
					SimonStep(self, self.data, "SIMON0", 2, 2),
					SimonStep(self, self.data, "SIMON1", 2, 2),
					
					# SimonStep(self, self.data, "SIMON0", 5, 3),
					# SimonStep(self, self.data, "SIMON1", 5, 6),
					# SimonStep(self, self.data, "SIMON2", 5, 9),
					TLXScaleStep(self, self.data, "tlx-raw-rating", "TLX Analysis"),
				]
		for index, pair in enumerate(pairwise_factors):
			# if (index == 0):
			steps.append(TLXRankStep(self, self.data, "tlx-weight-rank-step-" + str(index+1), "TLX Task Ranking", pair))
			
		self.set_steps(steps)
		self.start()

data = {}
my_gui = MyWizard(root, data)
my_gui.pack()

root.mainloop()