# Very simple diagram generator
import sys
from PyQt4 import QtGui, QtCore
import math

resolution = (500, 500)
beta = 1.0
power = 10.0
points = set()
drawArea = None

COLORS = [
        QtGui.QColor(0xD3, 0xD7, 0xCF, 50),
        QtGui.QColor(0xED, 0xD4, 0x00, 50),
        QtGui.QColor(0x73, 0xD2, 0x16, 50),
        QtGui.QColor(0xF5, 0x79, 0x00, 50),
        QtGui.QColor(0xC1, 0x7D, 0x11, 50),
        QtGui.QColor(0x34, 0x65, 0xA4, 50),
        QtGui.QColor(0x75, 0x50, 0x7B, 50),
        QtGui.QColor(0x55, 0x57, 0x53, 50),
        QtGui.QColor(0xCC, 0x00, 0x00, 50),
]

def managePoints(e):
    x = e.x() * resolution[0] // drawArea.width()
    y = e.y() * resolution[1] // drawArea.height()
    if QtGui.QApplication.keyboardModifiers() == QtCore.Qt.ControlModifier:
        points.remove((x, y))

    else:
        points.add((x, y))

    drawArea.repaint()

def clearPoints(e):
    global points
    points = set()
    drawArea.repaint()

def betaChanged(e):
    global beta
    beta = e
    drawArea.repaint()

def powerChanged(e):
    global power
    power = e
    drawArea.repaint()

def simulate(e):
    if not points:
        return

    painter = QtGui.QPainter()
    painter.begin(drawArea)
    def distance(x, y):
        return math.sqrt((x[0] - y[0]) ** 2 + (x[1] - y[1]) ** 2)

    painter.setBrush(QtCore.Qt.gray)
    painter.setPen(QtCore.Qt.gray)
    for x in range(resolution[0]):
        for y in range(resolution[1]):
            signals = []
            for i, p in enumerate(points):
                if (x, y) == p:
                    continue

                signals.append((power * resolution[0] / 10 / distance((x, y), p) ** 2, i))

            signals.sort()
            if not signals:
                continue

            summed = sum([p for p, _ in signals])
            for s, i in signals:
                if s / (summed - s + 1.0) >= beta:
                    painter.setBrush(COLORS[i % len(COLORS)])
                    painter.setPen(COLORS[i % len(COLORS)])
                    painter.drawRect(x * drawArea.width() // resolution[0],
                                     y * drawArea.height() // resolution[1],
                                     drawArea.width() // resolution[0],
                                     drawArea.height() // resolution[1])



    painter.setBrush(QtCore.Qt.black)
    painter.setPen(QtCore.Qt.black)
    for (x, y) in points:
        painter.drawRect(x * drawArea.width() // resolution[0],
                         y * drawArea.height() // resolution[1],
                         drawArea.width() // resolution[0],
                         drawArea.height() // resolution[1])

    painter.end()

def main():
    app = QtGui.QApplication(sys.argv)

    window = QtGui.QWidget()
    window.resize(800, 1000)
    window.setWindowTitle("SINR Diagrams simulator")

    vbox = QtGui.QVBoxLayout()

    global drawArea
    drawArea = QtGui.QLabel()
    drawArea.setStyleSheet("QWidget { background-color: white }")
    drawArea.mousePressEvent = managePoints
    drawArea.paintEvent = simulate
    vbox.addWidget(drawArea, 1)

    helpInformation = QtGui.QLabel("Add new senders with mouse left-click. To remove keep CTRL pressed.")
    vbox.addWidget(helpInformation)

    clearButton = QtGui.QPushButton("Clear")
    clearButton.clicked.connect(clearPoints)
    powerChooser = QtGui.QDoubleSpinBox(value=power, minimum=0.0, maximum=10000000.0)
    powerChooser.valueChanged.connect(powerChanged)
    betaChooser = QtGui.QDoubleSpinBox(value=beta, minimum=0.0, maximum=10000000.0)
    betaChooser.valueChanged.connect(betaChanged)
    hbox = QtGui.QHBoxLayout()
    hbox.addStretch(1)
    hbox.addWidget(clearButton, 1)
    hbox.addWidget(powerChooser, 1)
    hbox.addWidget(betaChooser, 1)
    vbox.addLayout(hbox, 1)

    window.setLayout(vbox)
    window.show()

    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
