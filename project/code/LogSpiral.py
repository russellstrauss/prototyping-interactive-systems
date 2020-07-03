
from panda3d.core import loadPrcFileData

from win32api import GetSystemMetrics
screen_width = str(GetSystemMetrics(0))
screen_height = str(GetSystemMetrics(1))
loadPrcFileData('', 'win-size ' + screen_width + ' ' + screen_height)
loadPrcFileData('', 'load-display pandagl')

import sys
import math
import numpy as np
from direct.showbase.ShowBase import ShowBase
base = ShowBase()

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

class Game(ShowBase):
	
	def __init__(self):
		
		base.setBackgroundColor(0.1, 0.1, 0.5, 1)
		base.setFrameRateMeter(True)

		# base.cam.setPos(0, 20, 1)
		# base.cam.lookAt(0, 0, 0)

		# Light
		alight = AmbientLight('ambientLight')
		alight.setColor(Vec4(0.5, 0.5, 0.5, 1))
		alightNP = render.attachNewNode(alight)

		dlight = DirectionalLight('directionalLight')
		dlight.setDirection(Vec3(1, 1, -1))
		dlight.setColor(Vec4(0.7, 0.7, 0.7, 1))
		dlightNP = render.attachNewNode(dlight)

		render.clearLight()
		render.setLight(alightNP)
		render.setLight(dlightNP)

		# Input
		self.accept('escape', self.doExit)
		self.accept('r', self.doReset)
		self.accept('1', self.toggleWireframe)
		self.accept('2', self.toggleTexture)
		self.accept('3', self.toggleDebug)
		self.accept('4', self.doScreenshot)

		inputState.watchWithModifiers('forward', 'w')
		inputState.watchWithModifiers('left', 'a')
		inputState.watchWithModifiers('reverse', 's')
		inputState.watchWithModifiers('right', 'd')
		inputState.watchWithModifiers('turnLeft', 'q')
		inputState.watchWithModifiers('turnRight', 'e')

		# Task
		self.count = 1
		taskMgr.add(self.renderLoop, 'updateWorld')

		# Physics
		self.setup()

	# _____HANDLER_____

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
		base.screenshot('Bullet')

	# ____TASK___

	def processInput(self, dt):
		force = Vec3(0, 0, 0)
		torque = Vec3(0, 0, 0)

		if inputState.isSet('forward'): force.setY( 1.0)
		if inputState.isSet('reverse'): force.setY(-1.0)
		if inputState.isSet('left'):    force.setX(-1.0)
		if inputState.isSet('right'):   force.setX( 1.0)
		if inputState.isSet('turnLeft'):  torque.setZ( 1.0)
		if inputState.isSet('turnRight'): torque.setZ(-1.0)

		force *= 30.0
		torque *= 10.0

		# self.boxNP.node().setActive(True)
		# self.boxNP.node().applyCentralForce(force)
		# self.boxNP.node().applyTorque(torque)

	def renderLoop(self, task):
		dt = globalClock.getDt()
		self.processInput(dt)
		self.world.doPhysics(dt)
		
		speed = .1
		self.progress += (dt / 10) * speed
		if (self.progress > 1):
			self.progress = 0
			
		self.updateCameraAlongCurve()
		
		self.count += 1 # increment frame count
		return task.cont
	
	def updateCameraAlongCurve(self):
		
		curve_index = round(len(self.curve) * self.progress)
		
		# iterate one by one through elements in curve trajectory array
		curve_x = self.curve[curve_index].getX()
		curve_y = self.curve[curve_index].getY()
		curve_z = self.curve[curve_index].getZ()
		base.cam.setPos(curve_x, curve_y, curve_z)
		
		if (base.cam.getZ() < 0): # make sure camera is never below the ground
			base.cam.setPos(base.cam.getX(), base.cam.getY(), 0)
		
		# turn to face focal object after each pos update
		base.cam.lookAt(self.viewing_object.getX(), self.viewing_object.getY(), self.viewing_object.getZ() + 6)
	
	def cleanup(self):
		self.world = None
		self.worldNP.removeNode()

	def setup(self):
		
		self.viewing_object = None
		
		# World
		self.worldNP = render.attachNewNode('World')
		self.debugNP = self.worldNP.attachNewNode(BulletDebugNode('Debug'))
		self.debugNP.show()
		self.debugNP.node().showWireframe(True)
		self.debugNP.node().showConstraints(True)
		self.debugNP.node().showBoundingBoxes(False)
		self.debugNP.node().showNormals(True)

		self.world = BulletWorld()
		# self.world.setGravity(Vec3(0, 0, -9.81))
		self.world.setGravity(Vec3(0, 0, 0))
		self.world.setDebugNode(self.debugNP.node())

		# Plane (static)
		shape = BulletPlaneShape(Vec3(0, 0, 1), 0)
		nodePath = self.worldNP.attachNewNode(BulletRigidBodyNode('Ground'))
		nodePath.node().addShape(shape)
		nodePath.setPos(0, 0, 0)
		nodePath.setCollideMask(BitMask32.allOn())
		self.world.attachRigidBody(nodePath.node())

		# Box (dynamic)
		# shape = BulletBoxShape(Vec3(0.5, 0.5, 0.5))
		# nodePath = self.worldNP.attachNewNode(BulletRigidBodyNode('Box'))
		# nodePath.node().addShape(shape)
		# nodePath.setPos(0, 0, 4)
		# # self.world.attachRigidBody(nodePath.node())
		# self.boxNP = nodePath # For applying force & torque
		
		# # box
		# shape = BulletBoxShape(Vec3(1, 1, 1))
		# nodePath = self.worldNP.attachNewNode(BulletRigidBodyNode('Box'))
		# nodePath.node().addShape(shape)
		# nodePath.setPos(0, 10, 10)
		# self.world.attachRigidBody(nodePath.node())
		# # box
		# shape = BulletBoxShape(Vec3(.25, .25, .25))
		# nodePath = self.worldNP.attachNewNode(BulletRigidBodyNode('Box'))
		# nodePath.node().addShape(shape)
		# nodePath.setPos(10, 6, 8)
		# self.world.attachRigidBody(nodePath.node())
		
		
		visNP = loader.loadModel('models/bunny.obj')
		geom = visNP.findAllMatches('**/+GeomNode').getPath(0).node().getGeom(0)
		mesh = BulletTriangleMesh()
		mesh.addGeom(geom)
		shape = BulletTriangleMeshShape(mesh, dynamic=True)
		body = BulletRigidBodyNode('Bowl')
		bodyNP = self.worldNP.attachNewNode(body)
		bodyNP.node().addShape(shape)
		# bodyNP.node().setMass(10.0)
		bodyNP.setHpr(0, 90,0)
		bodyNP.setPos(0, 0, -1.7)
		bodyNP.setCollideMask(BitMask32.allOn())
		self.world.attachRigidBody(bodyNP.node())
		# visNP.reparentTo(bodyNP)
		bodyNP.setScale(50)
		self.viewing_object = bodyNP
		
		self.curve = []
		self.progress = 0
		self.showCurve = False
		lineThickness = 1
		ls = LineSegs("LogSpiral")
		ls.setThickness(lineThickness)

		a = 0.17
		k = .01
		lower_bound = 0
		radius_scale = 100
		
		iteration_count = 40001
		step_delta = 0.001
		curve_length = step_delta * iteration_count
		
		for index in np.arange(step_delta, curve_length, step_delta):
			
			# Calculate curve point position
			spiral_x = radius_scale * a * pow(math.e, k * index) * math.cos(index)
			spiral_y = radius_scale * a * pow(math.e, k * index) * math.sin(index)
			spiral_z = (index) + lower_bound
			
			if (self.showCurve):
				ls.drawTo(spiral_x, spiral_y, spiral_z)
			self.curve.append(Vec3(spiral_x, spiral_y, spiral_z))
		
		# self.curve.reverse()
		node = ls.create(dynamic=False)
		body = BulletRigidBodyNode('lsRB')
		bodyNP = self.worldNP.attachNewNode(body)
		lsNP = bodyNP.attachNewNode(node)
		
game = Game()
# base.useDrive()
base.run()