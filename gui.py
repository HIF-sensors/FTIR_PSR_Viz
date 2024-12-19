import sys
from PyQt5.QtCore import QRect
from PyQt5.QtWidgets import QApplication, QPushButton, QWidget, QLabel, QFileDialog

from dataloader import *
from vizualization import *

class Window(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.filenames = None
        self.raw_df = None
        self.setFixedWidth(400)
        self.setFixedHeight(200)

        self.btn1 = QPushButton(self)
        self.btn1.setObjectName('Load files')
        self.btn1.setText('Load files')
        self.btn1.setGeometry(QRect(10, 35, 111, 50))
        self.btn1.clicked.connect(self.open_file_dialog)

        self.label1 = QLabel(self)
        self.label1.setObjectName('Loaded')
        self.label1.setText('')
        self.label1.setStyleSheet("border: 0.5px solid gray;")
        self.label1.setGeometry(QRect(125, 40, 111, 40))

        self.btn2 = QPushButton(self)
        self.btn2.setObjectName('Open Data')
        self.btn2.setText('Open Data')
        self.btn2.setGeometry(QRect(10, 100, 111, 50))
        self.btn2.clicked.connect(self.open_images)
        

    def open_file_dialog(self):
        # Open the file dialog and get the selected file name
        self.filenames, _ = QFileDialog.getOpenFileNames(self)
        if self.filenames:
            self.label1.setText("Loaded")
            dataloader = Dataloader(self.filenames)
            self.raw_df = dataloader.raw_df
            

    def open_images(self):
        viz(self.raw_df)
        self.filenames = None
        self.raw_df = None
        self.label1.setText("")



if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Window()
    window.show()
    sys.exit(app.exec())