from tkinter import *
import threading
import datetime
import simpleaudio as sa
from picturebutton import PictureButton

class PictureSoundButton(PictureButton):

	def __init__(self, master=None, cnf={}, **kw):

		if "soundpath" in cnf.keys():
			self.soundpath = cnf['soundpath']
			cnf.pop('soundpath')

		if "soundpath" in kw.keys():
			self.soundpath = kw['soundpath']
			kw.pop('soundpath')

		super().__init__(master, cnf, **kw)

	def _buttonpress(self, event):
		super()._buttonpress(event)
		if self.soundpath != None:
			# use of thread due to blocking nature of the sound playback
			t1 = threading.Thread(target=playsound, args=[self.soundpath])
			t1.start()

def playsound(spath):
	wo = sa.WaveObject.from_wave_file(spath)
	po = wo.play()
	po.wait_done()