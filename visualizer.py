import sys
import numpy as np
from pyqtgraph.Qt import QtCore, QtGui
import pyqtgraph.opengl as gl
from opensimplex import OpenSimplex
import pyaudio
import struct

class Visualizer(object):
	def __init__(self):
		#Setting up the GUI
		self.app = QtGui.QApplication(sys.argv)
		self.window = gl.GLViewWidget()
		self.window.setGeometry(0, 110, 1920, 1080)
		self.window.setWindowTitle('Visualizer')
		self.window.setCameraPosition(distance = 30, elevation = 12)
		self.window.show()
		#adding grid to window, grid for reference
		'''grid = gl.GLGridItem()
		grid.scale(2, 2, 2)
		self.window.addItem(grid)'''

		#vertices
		self.nsteps = 1.36	#distance between vertices, 1.3 to make it 32
		self.offset = 0
		self.xpoints = np.arange(-20, 22 + self.nsteps, self.nsteps)
		self.ypoints = np.arange(-20, 22 + self.nsteps, self.nsteps)
		self.nfaces = len(self.ypoints)
		#noise object
		self.noise = OpenSimplex()
		#creates the verticies array
		verts, faces, colors = self.mesh()

		# create the mesh item
		self.mesh1 = gl.GLMeshItem(vertexes = verts, faces = faces, faceColors = colors, smooth = False, drawEdges = True)
		#view options
		self.mesh1.setGLOptions('additive')
		self.window.addItem(self.mesh1)

		self.RATE = 44100
		#samples per buffer or frame
		self.CHUNK = len(self.xpoints) * len(self.ypoints)

		self.p = pyaudio.PyAudio()
		self.stream = self.p.open(
			format = pyaudio.paInt16,
			channels = 1,
			#input_device_index = int(input()),
			rate = self.RATE,
			input = True,
			output = True,
			frames_per_buffer = self.CHUNK
		)

	def mesh(self, offset = 0, height = 2.5, wf_data = None):

		if wf_data is not None:
			wf_data = struct.unpack(str(2 * self.CHUNK) + 'B', wf_data)
			wf_data = np.array(wf_data, dtype = 'b')[::2] + 128
			wf_data = np.array(wf_data, dtype = 'int32') - 128
			#lowering the height
			wf_data = wf_data * 0.04
			wf_data = wf_data.reshape((len(self.xpoints), len(self.ypoints)))
		else:
			wf_data = np.array([1] * 1024)
			wf_data = wf_data.reshape((len(self.xpoints), len(self.ypoints)))

		faces = []
		colors = []
		#create the veritices array
		verts = np.array([
			[
				x, y, wf_data[xid][yid] * self.noise.noise2d(x = xid/5 + offset, y = yid/5 + offset) #np.random.normal(1) #lower number = smoother, higher number = rougher, multiplier adds higher peaks
			]
			for xid, x in enumerate(self.xpoints) for yid, y in enumerate(self.ypoints)
		],
			dtype=np.float32
		)

		for yid in range(self.nfaces - 1):
			yoff = yid * self.nfaces
			for xid in range(self.nfaces - 1):
				#building the triangle faces, shifting down the row to accomodate for faces
				faces.append([xid + yoff, xid + yoff + self.nfaces, xid + yoff + self.nfaces + 1])
				faces.append([xid + yoff, xid + yoff + 1, xid + yoff + self.nfaces + 1])
				colors.append([xid / self.nfaces, 1 - xid / self.nfaces, yid / self.nfaces, 0.8]) #lower number = less bright
				colors.append([xid / self.nfaces, 1 - xid / self.nfaces, yid / self.nfaces, 0.9]) #different numbers to add slight contrast

		faces = np.array(faces, dtype = np.uint32)
		colors = np.array(colors, dtype = np.float32)

		return verts, faces, colors


	def update(self):
		#waveform data
		wf_data = self.stream.read(self.CHUNK)
		#update the mesh and shift the noise each time
		verts, faces, colors = self.mesh(offset = self.offset, wf_data = wf_data)
		self.mesh1.setMeshData(vertexes = verts, faces = faces, faceColors = colors)
		#lower = slower, higher = faster
		self.offset -= 0.05

	def animation(self, frametime = 10):
		#calls the update method to run in a loop
		timer = QtCore.QTimer()
		timer.timeout.connect(self.update)
		timer.start(frametime)
		self.start()

	def start(self):
		#geting the graphics window to open and setup
		if(sys.flags.interactive != 1) or not hasattr(QtCore, 'PYQT_VERSION'):
			QtGui.QApplication.instance().exec_()


if __name__ == '__main__':
	t = Visualizer()
	#shows the basic layover
	#t.start()
	#moves across the terrain
	t.animation()