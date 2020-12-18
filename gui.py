# steps
# 1. program audio waveform
# create gui for analyzing audio
# 2. convert to rbg
# 3. send to arduino or raspberry pi

import time
import numpy
import pyqtgraph as pg
from PyQt5 import QtGui
from pyqtgraph.dockarea import *


class GUI:
    plot = []
    curve = []

    def __init__(self, width = 800, height = 450, title = ''):
        # Setting up the GUI window and its layout
        self.app = QtGui.QApplication([])
        self.win = pg.GraphicsWindow(title)
        self.win.resize(width, height)
        self.win.setWindowTitle(title)
        self.layout = QtGui.QVBoxLayout()
        self.win.setLayout(self.layout)

    def add_plot(self, title):
        new_plot = pg.PlotWidget()
        self.layout.addWidget(new_plot)
        self.plot.append(new_plot)
        self.curve.append([])

    def add_curve(self, plot_index, pen=(255, 255, 255)):
        self.curve[plot_index].append(self.plot[plot_index].plot(pen=pen))


if __name__ == '__main__':
    # Example test gui
    N = 48
    gui = GUI(title='Test')
    # Sin plot
    gui.add_plot(title='Sin Plot')
    gui.add_curve(plot_index=0)
    gui.win.nextRow()
    # Cos plot
    gui.add_plot(title='Cos Plot')
    gui.add_curve(plot_index=1)
    while True:
        t = time.time()
        x = numpy.linspace(t, 2 * numpy.pi + t, N)
        gui.curve[0][0].setData(x=x, y=numpy.sin(x))
        gui.curve[1][0].setData(x=x, y=numpy.cos(x))
        gui.app.processEvents()
        time.sleep(1.0 / 30.0)