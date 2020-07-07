
from panda3d.core import loadPrcFileData
from forbiddenfruit import curse

from win32api import GetSystemMetrics
screen_width = str(GetSystemMetrics(0))
screen_height = str(GetSystemMetrics(1))
loadPrcFileData("", "win-size " + screen_width + " " + screen_height)
loadPrcFileData("", "load-display pandagl")

import sys
import math
import numpy as np
from direct.showbase.ShowBase import ShowBase

from direct.showbase.DirectObject import DirectObject
from direct.showbase.InputStateGlobal import inputState

from panda3d.core import *
from panda3d.core import AmbientLight
from panda3d.core import DirectionalLight
from panda3d.core import Vec3
from panda3d.core import Vec4
from panda3d.core import Point3
from panda3d.core import TransformState
from panda3d.core import BitMask32
from panda3d.core import LineSegs, NodePath
from panda3d.core import TextNode

# cleanup me
from panda3d.bullet import BulletWorld
from panda3d.bullet import BulletPlaneShape
from panda3d.bullet import BulletBoxShape
from panda3d.bullet import BulletRigidBodyNode
from panda3d.bullet import BulletDebugNode
from panda3d.bullet import BulletSphereShape
from panda3d.bullet import BulletCapsuleShape
from panda3d.bullet import BulletCylinderShape
from panda3d.bullet import BulletConeShape
from panda3d.bullet import BulletConvexHullShape
from panda3d.bullet import BulletTriangleMesh
from panda3d.bullet import BulletTriangleMeshShape
from panda3d.bullet import BulletMultiSphereShape
from panda3d.bullet import XUp
from panda3d.bullet import YUp
from panda3d.bullet import ZUp

# GUI
import direct.directbase.DirectStart
from direct.gui.OnscreenText import OnscreenText
from direct.gui.DirectGui import *

from tkinter.filedialog import askopenfilename
from tkinter import Tk

class Node(NodePath):
	def __init__(self, node):
		super().__init__(node)
		self.hidden = False
		
	def hide(self):
		super().hide()
	def show(self):
		super().show()

class LogSpiral(ShowBase):
	
	def __init__(self):
		
		base.setBackgroundColor(0.1, 0.1, 0.5, 1)
		base.setFrameRateMeter(True)
		
		# base.cam.setPos(0, 20, 1)
		# base.cam.lookAt(0, 0, 0)

		# Light
		alight = AmbientLight("ambientLight")
		alight.setColor(Vec4(0.5, 0.5, 0.5, 1))
		alightNP = render.attachNewNode(alight)

		dlight = DirectionalLight("directionalLight")
		dlight.setDirection(Vec3(1, 1, -1))
		dlight.setColor(Vec4(0.7, 0.7, 0.7, 1))
		dlightNP = render.attachNewNode(dlight)

		render.clearLight()
		render.setLight(alightNP)
		render.setLight(dlightNP)

		# Input
		self.accept("escape", self.doExit)
		self.accept("r", self.doReset)
		self.accept("2", self.toggleTexture)
		self.accept("3", self.toggleDebug)
		self.accept("4", self.doScreenshot)
		self.accept("g", self.startAnimation)
		self.accept("c", self.toggleCurveVisibility)
		self.accept("h", self.toggleViewingObjectVisibility)

		inputState.watchWithModifiers("forward", "w")
		inputState.watchWithModifiers("left", "a")
		inputState.watchWithModifiers("reverse", "s")
		inputState.watchWithModifiers("right", "d")
		inputState.watchWithModifiers("turnLeft", "q")
		inputState.watchWithModifiers("turnRight", "e")

		# Task
		self.count = 1
		taskMgr.add(self.renderLoop, "updateWorld")

		# Physics
		self.setup()

	# _____HANDLER_____
	
	def setDefaults(self):
		self.animating = False
		self.viewing_object_hidden = False
		self.a = .75
		self.k = .5
		self.viewing_object = None
		self.viewing_distance = 250
		self.viewing_angle = 0
		self.curve_segment = None
		self.show_curve = True
		self.speed = .25
		self.radius_scale = 1
		self.lower_bound = 1
		self.truncate_percentage = .25
		self.height_scale = 1
		self.viewing_object_scaling = 1
	
	def startAnimation(self):
		self.animating = not self.animating
	
	def toggleCurveVisibility(self):
		self.show_curve = not self.show_curve
		if (self.show_curve):
			self.curve_segment.show()
		else:
			self.curve_segment.hide()
			
	def toggleViewingObjectVisibility(self):
		if (self.viewing_object_hidden):
			self.world.attachRigidBody(self.viewing_object.node())
		else:
			self.world.removeRigidBody(self.viewing_object.node())
		self.viewing_object_hidden = not self.viewing_object_hidden
		
	def doExit(self):
		self.cleanup()
		sys.exit(1)
	def doReset(self):
		self.cleanup()
		self.setup()
	def toggleWireframe(self):
		base.toggleWireframe()
	def toggleTexture(self):
		base.toggleTexture()
	def toggleDebug(self):
		if self.debugNP.isHidden():
			self.debugNP.show()
		else:
			self.debugNP.hide()
	def doScreenshot(self):
		base.screenshot("Bullet")
	def loadModel(self):
		
		if (self.viewing_object): self.world.removeRigidBody(self.viewing_object.node())
		
		Tk().withdraw() # we don't want a full GUI, so keep the root window from appearing
		filename = askopenfilename() # show an "Open" dialog box and return the path to the selected file
		# filename = "models/new2.obj"
		pandafile = Filename.fromOsSpecific(filename)
		viewing_object_NP = loader.loadModel(pandafile)
		geom = viewing_object_NP.findAllMatches("**/+GeomNode").getPath(0).node().getGeom(0)
		mesh = BulletTriangleMesh()
		mesh.addGeom(geom)
		shape = BulletTriangleMeshShape(mesh, dynamic=True)
		body = BulletRigidBodyNode("viewing_object")
		self.viewing_object = self.worldNP.attachNewNode(body)
		self.viewing_object.node().addShape(shape)
		# bodyNP.setHpr(0, 90,0)
		# bodyNP.setPos(0, 0, -1.7)
		self.viewing_object.setCollideMask(BitMask32.allOn())
		self.world.attachRigidBody(self.viewing_object.node())
		self.viewing_object.setScale(50)
		
	def renderLoop(self, task):
		dt = globalClock.getDt()
		self.world.doPhysics(dt)
		
		self.progress += (dt / 10) * self.speed
		if (self.progress > 1):
			self.progress = 0
			
		self.updateCamera()
		
		self.count += 1 # increment frame count
		return task.cont
	
	def updateCamera(self):
		
		curve_index = round(len(self.curve) * self.progress)
		if self.animating and len(self.curve) > 0:
			try:
				# iterate one by one through elements in curve trajectory array
				curve_x = self.curve[curve_index].getX()
				curve_y = self.curve[curve_index].getY()
				curve_z = self.curve[curve_index].getZ()
				base.cam.setPos(curve_x, curve_y, curve_z)
			except:
				print(sys.exc_info()[0])
				print("\n\n")
				print("Curve length: ")
				print(len(self.curve))
				print("curve index: ")
				print(curve_index)
			
			if (base.cam.getZ() < 0): # make sure camera is never below the ground
				base.cam.setPos(base.cam.getX(), base.cam.getY(), 0)
		else: # viewing condition
			quat = Quat()
			quat.setFromAxisAngle(self.viewing_angle, Vec3(0, 0, 1))
			rotated_vec = quat.xform(Vec3(1, -1, .5))
			base.cam.setPos(rotated_vec * self.viewing_distance)
	
		# turn to face focal object after each pos update
		base.cam.lookAt(self.viewing_object.getX(), self.viewing_object.getY(), self.viewing_object.getZ())
		
	def cleanup(self):
		self.world = None
		self.worldNP.removeNode()
		aspect2d.clear() # remove gui
		
	def addSliders(self):
		
		def updateViewingDistance(sliderIndex):
			self.viewing_distance = sliders[sliderIndex]["object"]["value"]
		def updateViewingAngle(sliderIndex):
			self.viewing_angle = sliders[sliderIndex]["object"]["value"]
			print(self.viewing_angle)
		def updateAValue(sliderIndex):
			self.a = sliders[sliderIndex]["object"]["value"]
			self.createCurve()
		def updateKValue(sliderIndex):
			self.k = sliders[sliderIndex]["object"]["value"]
			self.createCurve()
		def updateSpeed(sliderIndex):
			self.speed = sliders[sliderIndex]["object"]["value"]
		def updateRadialScale(sliderIndex):
			self.radius_scale = sliders[sliderIndex]["object"]["value"]
			self.createCurve()
		def updateLowerBound(sliderIndex):
			self.lower_bound = sliders[sliderIndex]["object"]["value"]
			self.createCurve()
		def updateTruncationPoint(sliderIndex):
			self.truncate_percentage = sliders[sliderIndex]["object"]["value"]
			self.createCurve()
		def updateHeightScale(sliderIndex):
			self.height_scale = sliders[sliderIndex]["object"]["value"]
			self.createCurve()
		def updateViewingObjectScale(sliderIndex):
			self.viewing_object_scaling = sliders[sliderIndex]["object"]["value"]
			self.viewing_object.setScale(self.viewing_object_scaling)
		
		# if "myVar" in locals(): print(len(sliders))
		
		sliders = [
			{ "text": "Viewing Distance", "range": (10, 10000), "value": self.viewing_distance, "pageSize": 100, "event": updateViewingDistance, "extraArgs": [0] },
			{ "text": "Viewing Angle", "range": (0, 360), "value": self.viewing_angle, "pageSize": 2, "event": updateViewingAngle, "extraArgs": [1] },
			{ "text": "Log Spiral \"a\" Coeffificient", "range": (-3, 3), "value": self.a, "pageSize": .1, "event": updateAValue, "extraArgs": [2] },
			{ "text": "Log Spiral \"k\" Coeffificient", "range": (.01, 1), "value": self.k, "pageSize": .1, "event": updateKValue, "extraArgs": [3] },
			{ "text": "Camera Movement Speed", "range": (.01, 3), "value": self.speed, "pageSize": .1, "event": updateSpeed, "extraArgs": [4] },
			{ "text": "Radial Scale", "range": (1, 10), "value": self.radius_scale, "pageSize": .25, "event": updateRadialScale, "extraArgs": [5] },
			{ "text": "Height Scale", "range": (1, 20), "value": self.height_scale, "pageSize": .5, "event": updateHeightScale, "extraArgs": [6] },
			{ "text": "Lift", "range": (0, 100), "value": self.lower_bound, "pageSize": 100, "event": updateLowerBound, "extraArgs": [7] },
			{ "text": "Truncate", "range": (.001, 1), "value": self.truncate_percentage, "pageSize": .1, "event": updateTruncationPoint, "extraArgs": [8] },
			{ "text": "Scale Viewing Object", "range": (.001, 100), "value": self.viewing_object_scaling, "pageSize": .1, "event": updateViewingObjectScale, "extraArgs": [9] },
		]
		
		for index, slider in enumerate(sliders):
			label_text = slider["text"]
			y_position = .97 - (.06 * index)
			position = (-1.75, y_position)
			
			textObject = OnscreenText(text=label_text,
				pos=position,
				scale=0.02,
				fg=(1, 1, 1, 1), # color
				align=TextNode.ALeft,
				mayChange=1)
				
			y_position = .95 - (.06 * index)
			position = (0, -1.75, y_position)
			slider["object"] = DirectSlider(range=slider["range"], value=slider["value"], pageSize=slider["pageSize"], command=slider["event"],
				extraArgs = slider["extraArgs"],
				pos=position,
				frameSize=(-1.75, -1.5, -0.008, 0.008),
				frameVisibleScale=(1, 0.25))
		
		buttons = [
			{ "text": "Load Model", "event": self.loadModel, "extraArgs": [0] },
			{ "text": "Hide Model", "event": self.toggleViewingObjectVisibility, "extraArgs": [1] }
		]
		
		for index, button in enumerate(buttons):
			position = (-1.7 + (.15 * index), 0, -.98)	
			button["object"] = DirectButton(text=(button["text"]),
				pos=position,
				scale=0.02,
				command=button["event"])

	def setup(self):
		
		# World
		self.worldNP = render.attachNewNode("World")
		self.GUI = self.worldNP.attachNewNode("GUI")
		self.debugNP = self.worldNP.attachNewNode(BulletDebugNode("Debug"))
		self.debugNP.show()
		self.debugNP.node().showWireframe(True)
		self.debugNP.node().showConstraints(True)
		self.debugNP.node().showBoundingBoxes(False)
		self.debugNP.node().showNormals(True)

		self.setDefaults()
		self.addSliders()
		self.createCurve()
		
		self.world = BulletWorld()
		# self.world.setGravity(Vec3(0, 0, -9.81))
		self.world.setGravity(Vec3(0, 0, 0))
		self.world.setDebugNode(self.debugNP.node())

		# Plane (static)
		shape = BulletPlaneShape(Vec3(0, 0, 1), 0)
		nodePath = self.worldNP.attachNewNode(BulletRigidBodyNode("Ground"))
		nodePath.node().addShape(shape)
		nodePath.setPos(0, 0, 0)
		nodePath.setCollideMask(BitMask32.allOn())
		self.world.attachRigidBody(nodePath.node())
		
		self.loadModel()

	def createCurve(self):
		
		self.curve = []
		self.progress = 0
		self.showCurve = True
		lineThickness = 2
		ls = LineSegs("LogSpiral")
		ls.setThickness(lineThickness)

		iteration_count = 10001
		step_delta = 0.001
		curve_length = step_delta * iteration_count
		
		for index in np.arange(1 + (curve_length * self.truncate_percentage), curve_length, step_delta):
			
			# Calculate curve point position
			spiral_x = self.radius_scale * self.a * pow(math.e, self.k * index) * math.cos(index)
			spiral_y = self.radius_scale * self.a * pow(math.e, self.k * index) * math.sin(index)
			spiral_z = self.height_scale * self.height_scale * math.log(index, math.e) + self.lower_bound
			
			if (self.showCurve): ls.drawTo(spiral_x, spiral_y, spiral_z)
			self.curve.append(Vec3(spiral_x, spiral_y, spiral_z))
		
		self.curve.reverse()
		if (self.curve_segment != None): self.curve_segment.removeNode()
		node = ls.create(dynamic=False)
		body = BulletRigidBodyNode("lsRB")
		bodyNP = self.worldNP.attachNewNode(body)
		self.curve_segment = bodyNP.attachNewNode(node)
		
		if (not self.show_curve): self.curve_segment.hide()
		
animation = LogSpiral()
# base.useDrive()
base.disableMouse()
base.run()