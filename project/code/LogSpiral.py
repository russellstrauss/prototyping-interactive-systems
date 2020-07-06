
from panda3d.core import loadPrcFileData

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

from panda3d.core import AmbientLight
from panda3d.core import DirectionalLight
from panda3d.core import Vec3
from panda3d.core import Vec4
from panda3d.core import Point3
from panda3d.core import TransformState
from panda3d.core import BitMask32
from panda3d.core import LineSegs, NodePath

# cleanup
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
from panda3d.core import TextNode

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
		self.a = .1
		self.k = .1
		self.viewing_object = None
		self.viewing_distance = 1000
		self.curve_segment = None
		self.show_curve = True
		self.speed = .25
		self.radius = 1
		self.lower_bound = 1
	
	def startAnimation(self):
		self.animating = not self.animating
	
	def toggleCurveVisibility(self):
		self.show_curve = not self.show_curve
		if (self.show_curve):
			self.curve_segment.show()
		else:
			self.curve_segment.hide()
	
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
		
		if self.animating:
			curve_index = round(len(self.curve) * self.progress)
			if (len(self.curve) < 1): self.createCurve()
			# iterate one by one through elements in curve trajectory array
			curve_x = self.curve[curve_index].getX()
			curve_y = self.curve[curve_index].getY()
			curve_z = self.curve[curve_index].getZ()
			base.cam.setPos(curve_x, curve_y, curve_z)
			
			if (base.cam.getZ() < 0): # make sure camera is never below the ground
				base.cam.setPos(base.cam.getX(), base.cam.getY(), 0)
		else:
			base.cam.setPos(Vec3(1, -1, .5) * self.viewing_distance)
	
		# turn to face focal object after each pos update
		base.cam.lookAt(self.viewing_object.getX(), self.viewing_object.getY(), self.viewing_object.getZ() + 6)
		
	def cleanup(self):
		self.world = None
		self.worldNP.removeNode()
		aspect2d.clear() # remove gui
		
	def addSliders(self):
		
		def updateViewingDistance(sliderIndex):
			self.viewing_distance = sliders[sliderIndex]["object"]["value"]
			
		def updateAValue(sliderIndex):
			self.a = sliders[sliderIndex]["object"]["value"]
			self.createCurve()
			
		def updateKValue(sliderIndex):
			self.k = sliders[sliderIndex]["object"]["value"]
			self.createCurve()
			
		def updateSpeed(sliderIndex):
			self.speed = sliders[sliderIndex]["object"]["value"]
			
		def updateRadialScale(sliderIndex):
			self.radius = sliders[sliderIndex]["object"]["value"]
			self.createCurve()
			
		def updateLowerBound(sliderIndex):
			self.lower_bound = sliders[sliderIndex]["object"]["value"]
			self.createCurve()
		
		# if "myVar" in locals(): print(len(sliders))
		
		sliders = [
			{ "text": "Viewing Distance", "range": (10, 10000), "value": 100, "pageSize": 1000, "method": updateViewingDistance, "extraArgs": [0] },
			{ "text": "Log Spiral \"a\" Coeffificient", "range": (.001, 1), "value": .1, "pageSize": .1, "method": updateAValue, "extraArgs": [1] },
			{ "text": "Log Spiral \"k\" Coeffificient", "range": (.001, 1), "value": .7, "pageSize": .1, "method": updateKValue, "extraArgs": [2] },
			{ "text": "Camera Movement Speed", "range": (.01, 2), "value": .1, "pageSize": .1, "method": updateSpeed, "extraArgs": [3] },
			{ "text": "Radial Scale", "range": (1, 10), "value": 1, "pageSize": .25, "method": updateRadialScale, "extraArgs": [4] },
			{ "text": "Lift", "range": (0, 100), "value": 0, "pageSize": 100, "method": updateLowerBound, "extraArgs": [5] }
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
			slider["object"] = DirectSlider(range=slider["range"], value=slider["value"], pageSize=slider["pageSize"], command=slider["method"],
				extraArgs = slider["extraArgs"],
				pos=position,
				frameSize=(-1.75, -1, -0.008, 0.008),
				frameVisibleScale=(1, 0.25))

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
		
		viewing_object_NP = loader.loadModel("models/bunny.obj")
		geom = viewing_object_NP.findAllMatches("**/+GeomNode").getPath(0).node().getGeom(0)
		mesh = BulletTriangleMesh()
		mesh.addGeom(geom)
		shape = BulletTriangleMeshShape(mesh, dynamic=True)
		body = BulletRigidBodyNode("Bowl")
		bodyNP = self.worldNP.attachNewNode(body)
		bodyNP.node().addShape(shape)
		bodyNP.setHpr(0, 90,0)
		bodyNP.setPos(0, 0, -1.7)
		bodyNP.setCollideMask(BitMask32.allOn())
		self.world.attachRigidBody(bodyNP.node())
		# viewing_object_NP.reparentTo(bodyNP)
		bodyNP.setScale(50)
		self.viewing_object = bodyNP

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
		
		for index in np.arange(curve_length * .25, curve_length, step_delta):
			
			# Calculate curve point position
			spiral_x = self.radius * self.a * pow(math.e, self.k * index) * math.cos(index)
			spiral_y = self.radius * self.a * pow(math.e, self.k * index) * math.sin(index)
			spiral_z = (index*index/2) + self.lower_bound
			
			if (self.showCurve): ls.drawTo(spiral_x, spiral_y, spiral_z)
			self.curve.append(Vec3(spiral_x, spiral_y, spiral_z))
		
		self.curve.reverse()
		if (self.curve_segment != None): self.curve_segment.removeNode()
		node = ls.create(dynamic=False)
		body = BulletRigidBodyNode("lsRB")
		bodyNP = self.worldNP.attachNewNode(body)
		self.curve_segment = bodyNP.attachNewNode(node)
		
		if (not self.show_curve): self.curve_segment.hide()
		print("Curve created of length " + str(len(self.curve)))
		
animation = LogSpiral()
# base.useDrive()
base.disableMouse()
base.run()