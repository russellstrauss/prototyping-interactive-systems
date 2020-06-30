from tkinter import *
import random
from picturesoundbutton import PictureSoundButton
from Wizard import Step, Wizard
from PIL import Image, ImageTk

class SimonStep(Step):
	def __init__(self, parent, data, stepname, num_trials, mem_seq_len):
		super().__init__(parent, data, stepname)

		self.completed = False
		self.previous_enabled = False

		self.description = Label(self, text="", font="Helvetica 16 bold italic")

		self.top_button = PictureSoundButton(self, {'clickcolor': 'red'}, imgpath="img/fry_200.jpg", soundpath="audio/fry.wav", bg='black', buttonaction=self.top_button_action)
		self.left_button = PictureSoundButton(self, {'clickcolor': 'blue'}, imgpath="img/farnsworth_200.jpg", soundpath="audio/farnsworth.wav", bg='black', buttonaction=self.left_button_action)
		self.right_button = PictureSoundButton(self, {'clickcolor': 'yellow'}, imgpath="img/bender_200.png", soundpath="audio/bender.wav", bg='black', buttonaction=self.right_button_action)
		self.bottom_button = PictureSoundButton(self, {'clickcolor': 'green'}, imgpath="img/zoidberg_200.jpg", soundpath="audio/zoidberg.wav", bg='black', buttonaction=self.bottom_button_action)
		self.disable_buttons()
		
		row = 0
		self.description.grid(row=row, column=0, columnspan=3)
		row += 1
		self.top_button.grid(row=row, column=1, ipadx=40, ipady=40)
		row += 1
		self.left_button.grid(row=row, column=0, ipadx=40, ipady=40)
		self.right_button.grid(row=row, column=2, ipadx=40, ipady=40)
		row += 1
		self.bottom_button.grid(row=row, column=1, ipadx=40, ipady=40)
		
		self.mem_seq_len = mem_seq_len
		self.btn_list = ["top", "bottom", "left", "right"]
		self.btn_cbks = {
			"top": (self.top_button.dobuttonpress, self.top_button.dobuttonrelease),
			"bottom": (self.bottom_button.dobuttonpress, self.bottom_button.dobuttonrelease),
			"left": (self.left_button.dobuttonpress, self.left_button.dobuttonrelease),
			"right": (self.right_button.dobuttonpress, self.right_button.dobuttonrelease),
		}

		self.target_mem_seq = []
		self.curr_target_index = 0
		self.user_response_allowed = False

		self.target_trials = num_trials
		self.curr_trial = 0

		self.data[self.stepname]["mem_seq_cond"] = self.mem_seq_len
		self.data[self.stepname]["num_trials"] = self.target_trials
		self.data[self.stepname]["responses"] = []

	def _build_correct_animation(self):
		self.schedule = [
			(10, self.labelcorrect),
			(2000, self.start_stimulus_presentation)
		]

	def _build_wrong_animation(self):
		self.schedule = [
			(10, self.labelwrong),
			(2000, self.start_stimulus_presentation)
		]

	def _build_finished_animation(self):
		self.schedule = [
			(10, self.labelfinished),
			(10, self._step_completed),
		]

	def _build_trial_animation(self):

		self.target_mem_seq = []
		self.schedule = [
			(10, self.labelcountdown),
			(1000, self.labelcountdown),
			(1000, self.labelcountdown),
			(1000, self.labelbegin),
		]

		for i in range(self.mem_seq_len):
			target_btn_index = random.randint(0, len(self.btn_list) - 1)
			btn_name = self.btn_list[target_btn_index]
			self.target_mem_seq.append(btn_name)
			btn_down = self.btn_cbks[btn_name][0]
			btn_up = self.btn_cbks[btn_name][1]
			tup_down = (1000, btn_down)
			tup_up = (500, btn_up)
			self.schedule.append(tup_down)
			self.schedule.append(tup_up)

		end_sched = [
			(10, self.labelend),
			(1000, self.labelprompt),
			(10, self.start_user_response),
			# (10, self._step_completed),
		]
		self.schedule += end_sched

	def start_user_response(self):
		self.curr_target_index = 0
		#self.user_response_allowed = True
		self.enable_buttons()
		dat = {"target": self.target_mem_seq, "response": []}
		self.data[self.stepname]["responses"].append(dat)

	def start_stimulus_presentation(self):
		self.disable_buttons()
		#self.user_response_allowed = False
		if self.curr_trial >= self.target_trials:
			self._build_finished_animation()
		else:
			self._build_trial_animation()
		self.doanim()

	def start_correct_presentation(self):
		self.disable_buttons()
		#self.user_response_allowed = False
		self._build_correct_animation()
		self.doanim()

	def start_wrong_presentation(self):
		self.disable_buttons()
		#self.user_response_allowed = False
		self._build_wrong_animation()
		self.doanim()

	def enable_buttons(self):
		self.top_button.setinteractive(True)

		self.user_response_allowed = True

	def disable_buttons(self):
		self.top_button.setinteractive(False)

		self.user_response_allowed = False

	def onscreen_enter(self):
		super().onscreen_enter()
		self.start_stimulus_presentation()

	def onscreen_exit(self):
		pass

	def doanim(self):

		if len(self.schedule) <= 0:
			return

		self.sched_item = 0

		s = self.schedule[self.sched_item]
		#run the function stored in the schedule
		self.after(s[0], self.doanim_helper)

	def doanim_helper(self):
		# Note that the structure of this method has changed so that
		# self.schedule and self.sched_item can be re-initialized at
		# the end of an animation and start a new call do doanim()
		# The fix for this is to call s[1]() at the end
		s = self.schedule[self.sched_item]
		self.sched_item += 1

		if self.sched_item < len(self.schedule):
			s_next = self.schedule[self.sched_item]
			self.after(s_next[0], self.doanim_helper)

		# run the function stored in the schedule
		s[1]()

	countdown = 0
	def labelcountdown(self):
		if self.countdown <= 0:
			self.countdown = 3
		cstr = str(self.countdown)
		self.description.config(text="The memory sequence will begin in " + cstr + " sec.", fg="black")
		self.countdown -= 1
		self.update()

	def labelbegin(self):
		self.description.config(text="The memory sequence is playing", fg="green")
		self.update()

	def labelend(self):
		self.description.config(text="The memory sequence has ended", fg="red")
		self.update()

	def labelprompt(self):
		self.description.config(text="Now repeat the sequence", fg="black")
		self.update()

	def labelcorrect(self):
		self.description.config(text="Correct!!!", fg="green")
		self.update()

	def labelwrong(self):
		self.description.config(text="WRONG!!!", fg="red")
		self.update()

	def labelfinished(self):
		self.description.config(text="Block complete. Click next.", fg="black")
		self.update()

	def btn_action(self, btn_name, event):

		if not self.user_response_allowed:
			return

		dat = btn_name
		self.data[self.stepname]["responses"][-1]["response"].append(dat)

		if btn_name != self.target_mem_seq[self.curr_target_index]:
			# start failure presentation, chained with stimulus unless at end
			print("Failure!!!")
			self.data[self.stepname]["responses"][-1]["success"] = False
			self.curr_trial += 1
			self.start_wrong_presentation()
		elif self.curr_target_index >= len(self.target_mem_seq) - 1:
			# start reward presentation, chained with stimulus unless at end
			print("Success!!")
			self.data[self.stepname]["responses"][-1]["success"] = True
			self.curr_trial += 1
			self.start_correct_presentation()
		else:
			print("Good so far...")
			self.curr_target_index += 1

	def top_button_action(self, event):
		self.btn_action("top", event)
	def bottom_button_action(self, event):
		self.btn_action("bottom", event)
	def left_button_action(self, event):
		self.btn_action("left", event)
	def right_button_action(self, event):
		self.btn_action("right", event)