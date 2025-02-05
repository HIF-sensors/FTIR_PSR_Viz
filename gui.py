import sys
from PyQt5.QtCore import QRect
from PyQt5.QtWidgets import QApplication, QPushButton, QWidget, QLabel, QFileDialog

from dataloader import *
from vizualization import *

class Window(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.filenames = None
        self.batchname = None
        self.dataloader = None
        self.reflectance_df = None
        self.library_df = None
        self.setFixedWidth(400)
        self.setFixedHeight(400)

        # For loading files
        self.btn1 = QPushButton(self)
        self.btn1.setObjectName('Load files')
        self.btn1.setText('Load files')
        self.btn1.setGeometry(QRect(10, 35, 111, 50))
        self.btn1.clicked.connect(self.open_file_dialog)

        # Message for loading operation
        self.label1 = QLabel(self)
        self.label1.setObjectName('Data loaded')
        self.label1.setText('')
        self.label1.setStyleSheet("border: 0.5px solid gray;")
        self.label1.setGeometry(QRect(125, 40, 111, 40))

        # For loading files
        self.btn2 = QPushButton(self)
        self.btn2.setObjectName('Load library')
        self.btn2.setText('Load library')
        self.btn2.setGeometry(QRect(10, 100, 111, 50))
        self.btn2.clicked.connect(self.open_library) # change this to read excel file

        # Message for loading operation
        self.label2 = QLabel(self)
        self.label2.setObjectName('Library loaded')
        self.label2.setText('')
        self.label2.setStyleSheet("border: 0.5px solid gray;")
        self.label2.setGeometry(QRect(125, 105, 111, 40))

        # For opening data
        self.btn3 = QPushButton(self)
        self.btn3.setObjectName('Open Data')
        self.btn3.setText('Open Data')
        self.btn3.setGeometry(QRect(10, 165, 111, 50))
        self.btn3.clicked.connect(self.open_data)
        

    def open_file_dialog(self):
        # Open the file dialog and get the selected file name
        self.filenames, _ = QFileDialog.getOpenFileNames(self)
        if self.filenames:
            self.label1.setText("Data loaded")
            self.dataloader = Dataloader(reflectance_paths=self.filenames)
        
        # Get the batchname
        clock = 3
        file_path = self.filenames[0]
        while clock:
            file_path, folder = os.path.split(file_path)
            clock -= 1
        self.batchname = folder


    def open_library(self):
        # Open the file dialog and get the selected excel file
        # Load the file as pandas dataframe
        self.lib_path, _ = QFileDialog.getOpenFileName(self)
        if self.filenames:
            self.label2.setText("Library loaded")
            self.library_df = pd.read_excel(self.lib_path)
        pass
            

    def open_data(self):
        df_plot = {
                'Reflectance (.sed )':self.dataloader.reflectance_df,
                   'Y-axis rescaled': self.dataloader.rescaled_df
                   }
        # This creates vizualization to plot multiple data
        viz(self.batchname, df_plot, self.library_df)
        # Check if del obj is possible
        self.filenames = None
        self.reflectance_df = None
        self.library_df = None
        self.label1.setText("")
        self.label2.setText("")



if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Window()
    window.show()
    sys.exit(app.exec())