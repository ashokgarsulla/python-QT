import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget,QVBoxLayout,QHBoxLayout
from PyQt5.QtGui import QPalette, QColor


class Color(QWidget):

    def __init__(self, color):
        super(Color, self).__init__()
        self.setAutoFillBackground(True)

        palette = self.palette()
        palette.setColor(QPalette.Window, QColor(color))
        self.setPalette(palette)


class MainWindow(QMainWindow):

    def __init__(self):
        super(MainWindow, self).__init__()

        self.setWindowTitle("My App")

        layout = QVBoxLayout()

        layout.addWidget(Color('red'))
        layout.addWidget(Color('green'))
        layout.addWidget(Color('red'))
        layout.addWidget(Color('green'))

        hlayout = QHBoxLayout()

        hlayout.addWidget(Color('red'))
        hlayout.addWidget(Color('green'))
        hlayout.addWidget(Color('red'))
        hlayout.addWidget(Color('green'))

        mainLayout = QVBoxLayout()

        mainLayout.addLayout(layout)
        mainLayout.addLayout(hlayout)


        widget = QWidget()
        widget.setLayout(mainLayout)
        self.setCentralWidget(widget)


app = QApplication(sys.argv)

window = MainWindow()
window.show()

app.exec()