from tkinter import *
from PIL import Image, ImageTk

class PictureButton(Label):

	def __init__(self, master=None,cnf={}, **kw):

		self.__is_interactive = True

		self.imgpath = None
		self.clickcolor = 'red'
		self.buttonaction = None
		# self.imgheight = None

		if "imgpath" in cnf.keys():
			self.imgpath = cnf['imgpath']
			cnf.pop('imgpath')

		if "imgpath" in kw.keys():
			self.imgpath = kw['imgpath']
			kw.pop('imgpath')

		if "clickcolor" in cnf.keys():
			self.clickcolor = cnf['clickcolor']
			cnf.pop('clickcolor')

		if "clickcolor" in kw.keys():
			self.clickcolor = kw['clickcolor']
			kw.pop('clickcolor')

		# if "imgheight" in cnf.keys():
		#     self.imgheight = cnf['imgheight']
		#     cnf.pop('imgheight')
		#
		# if "imgheight" in kw.keys():
		#     self.imgheight = kw['imgheight']
		#     kw.pop('imgheight')
		#

		if "buttonaction" in cnf.keys():
			self.buttonaction = cnf['buttonaction']
			cnf.pop('buttonaction')

		if "buttonaction" in kw.keys():
			self.buttonaction = kw['buttonaction']
			kw.pop('buttonaction')

		super().__init__(master, cnf, **kw)

		self.origbg = self.cget('bg')

		self.image = None

		if self.imgpath != None:
			load_image = Image.open(self.imgpath)
			self.image = ImageTk.PhotoImage(load_image)
			# self.image = PhotoImage(file=self.imgpath)

		if self.image != None:
			self.config(image=self.image)

		self.bind("<ButtonPress-1>", self.__buttonpress_cbk)
		self.bind("<ButtonRelease-1>", self.__buttonrelease_cbk)

	# self.cget('state')

	def __buttonpress_cbk(self, event):
		if self.__is_interactive:
			self._buttonpress(event)

	def __buttonrelease_cbk(self, event):
		if self.__is_interactive:
			self._buttonrelease(event)

	def _buttonpress(self, event):
		self.config(bg=self.clickcolor)
		if self.buttonaction != None:
			self.buttonaction(event)

	def _buttonrelease(self, event):
		self.config(bg=self.origbg)

	def dobuttonpress(self):
		self._buttonpress(None)

	def dobuttonrelease(self):
		self._buttonrelease(None)

	def setinteractive(self, v):
		self.__is_interactive = v

		if not self.__is_interactive:
			self.config(bg=self.origbg)