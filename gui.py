import sys
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *

from dataloader import *
from vizualization import *
from pre_processing import *

class Window(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.sensor = None
        self.reflectance_files = None
        self.absorbance_files = None
        self.reflectance_df = None
        self.absorbance_df = None
        self.batchname = None
        self.lib_path = None
        self.library_df = None
        self.spectrum_paths = None
        self.refSpectrum_df = None
        self.rescaling_flag = False
        self.reflectance_rescaled_df = None
        self.absorbance_rescaled_df = None
        self.download_flag = False
        self.setFixedWidth(500)
        self.setFixedHeight(670)

        # Choose sensor
        self.label1 = QLabel(self)
        self.label1.setObjectName('Choose point sensor: ')
        self.label1.setText('Choose point sensor: ')
        font = QFont()
        font.setBold(True)
        font.setPointSize(14)  
        self.label1.setFont(font)
        self.label1.setGeometry(QRect(10, 20, 150, 20))


        # creating check box for choosing sensor
        self.checkBoxSWIR = QCheckBox("VNIR/SWIR", self) 
        self.checkBoxSWIR.setGeometry(10, 50, 100, 20) 
        self.checkBoxMWIR = QCheckBox("MWIR/LWIR", self) 
        self.checkBoxMWIR.setGeometry(120, 50, 100, 20)

        # calling the uncheck method if any check box state is changed 
        self.checkBoxSWIR.stateChanged.connect(self.select_sensor) 
        self.checkBoxMWIR.stateChanged.connect(self.select_sensor) 

         # Select Reflectance files
        self.label2 = QLabel(self)
        self.label2.setObjectName('Select single or multiple "Reflectance" files')
        self.label2.setText('Select single or multiple "Reflectance" files')  
        self.label2.setFont(font)
        self.label2.setGeometry(QRect(10, 90, 300, 20))

        # Button for loading Reflectance
        self.btn1 = QPushButton(self)
        self.btn1.setObjectName('Load Reflectance')
        self.btn1.setText('Load Reflectance')
        self.btn1.setGeometry(QRect(10, 120, 130, 40))
        self.btn1.clicked.connect(self.reflectance_file_dialog)

        # Message for loading Reflectance files
        self.label3 = QLabel(self)
        self.label3.setObjectName('Reflectance loaded')
        self.label3.setText('')
        self.label3.setStyleSheet("border: 0.5px solid gray;")
        self.label3.setGeometry(QRect(150, 125, 130, 30))

        # Select Absorbance files
        self.label4 = QLabel(self)
        self.label4.setObjectName('Select single or multiple "Absorbance" files (Optional)')
        self.label4.setText('Select single or multiple "Absorbance" files (Optional)')  
        self.label4.setFont(font)
        self.label4.setGeometry(QRect(10, 180, 365, 20))

        # Button for loading Absorbance
        self.btn2 = QPushButton(self)
        self.btn2.setObjectName('Load Absorbance')
        self.btn2.setText('Load Absorbance')
        self.btn2.setGeometry(QRect(10, 210, 130, 40))
        self.btn2.clicked.connect(self.absorbance_file_dialog)

        # Message for loading Absorbance files
        self.label5 = QLabel(self)
        self.label5.setObjectName('Absorbance loaded')
        self.label5.setText('')
        self.label5.setStyleSheet("border: 0.5px solid gray;")
        self.label5.setGeometry(QRect(150, 215, 130, 30))

         # Select Library file
        self.label6 = QLabel(self)
        self.label6.setObjectName('Select fingerprint library for the specified sensor (Optional)')
        self.label6.setText('Select fingerprint library for the specified sensor (Optional)')  
        self.label6.setFont(font)
        self.label6.setGeometry(QRect(10, 265, 400, 20))

        # Button for loading Library
        self.btn3 = QPushButton(self)
        self.btn3.setObjectName('Load Fingerprints')
        self.btn3.setText('Load Library')
        self.btn3.setGeometry(QRect(10, 295, 130, 40))
        self.btn3.clicked.connect(self.open_library)

        # Message for library files
        self.label7 = QLabel(self)
        self.label7.setObjectName('Fingerprints loaded')
        self.label7.setText('')
        self.label7.setStyleSheet("border: 0.5px solid gray;")
        self.label7.setGeometry(QRect(150, 300, 130, 30))

        #### test
         # Select Reference spectrum
        self.label8 = QLabel(self)
        self.label8.setObjectName('Select Reference spectrum for the specified sensor (Optional)')
        self.label8.setText('Select Reference spectrum for the specified sensor (Optional)')  
        self.label8.setFont(font)
        self.label8.setGeometry(QRect(10, 350, 420, 20))

        # Button for loading Reference spectrum
        self.btn4 = QPushButton(self)
        self.btn4.setObjectName('Load Spectrums')
        self.btn4.setText('Load Spectrums')
        self.btn4.setGeometry(QRect(10, 380, 130, 40))
        self.btn4.clicked.connect(self.open_spectrums)

        # Message for Reference spectrum
        self.label9 = QLabel(self)
        self.label9.setObjectName('Spectrums loaded')
        self.label9.setText('')
        self.label9.setStyleSheet("border: 0.5px solid gray;")
        self.label9.setGeometry(QRect(150, 385, 130, 30))
        #########

        # Select pre-processing method
        self.label10 = QLabel(self)
        self.label10.setObjectName('Select Pre-processing method (Optional)')
        self.label10.setText('Select Pre-processing method (Optional)')  
        self.label10.setFont(font)
        self.label10.setGeometry(QRect(10, 435, 365, 20))

        # creating check box for choosing sensor
        self.checkBoxRescaling = QCheckBox("Y-axis rescaling", self) 
        self.checkBoxRescaling.setGeometry(10, 465, 160, 30)
        self.checkBoxRescaling.stateChanged.connect(self.select_rescaling)

        # Start visualization
        self.label11 = QLabel(self)
        self.label11.setObjectName('Data visualisation')
        self.label11.setText('Data visualisation')  
        self.label11.setFont(font)
        self.label11.setGeometry(QRect(10, 515, 365, 20))

        # creating check box for choosing sensor
        self.checkBoxDownload = QCheckBox("Download as .html", self) 
        self.checkBoxDownload.setGeometry(10, 545, 150, 30)
        self.checkBoxDownload.stateChanged.connect(self.select_download)

        # For opening data
        self.btn5 = QPushButton(self)
        self.btn5.setObjectName('Open Data')
        self.btn5.setText('Open Data')
        self.btn5.setGeometry(QRect(10, 585, 111, 40))
        self.btn5.clicked.connect(self.open_data)
        
    def select_sensor(self, state):
        if state == Qt.Checked: 
            if self.sender() == self.checkBoxSWIR: 
                self.checkBoxMWIR.setChecked(False) 
                self.sensor = 'VNIR_SWIR' 
            elif self.sender() == self.checkBoxMWIR:  
                self.checkBoxSWIR.setChecked(False) 
                self.sensor = 'MWIR_LWIR' 


    def reflectance_file_dialog(self):
        # Open the file dialog and get the selected file name
        self.reflectance_files, _ = QFileDialog.getOpenFileNames(self)
        if self.reflectance_files:
            self.label3.setText("Reflectance loaded")
            self.reflectance_df = load_reflectance(self.reflectance_files)
            message = "Reflectance loaded" if self.reflectance_df is not None else "Error!"
            self.label3.setText(message)
        
        # Get the batchname
        if self.sensor == 'VNIR_SWIR':
            clock = 3
        elif self.sensor == 'MWIR_LWIR':
            clock = 4
        file_path = self.reflectance_files[0]
        while clock:
            file_path, folder = os.path.split(file_path)
            clock -= 1
        self.batchname = folder

    def absorbance_file_dialog(self):
        # Open the file dialog and get the selected file name
        self.absorbance_files, _ = QFileDialog.getOpenFileNames(self)
        if self.absorbance_files:
            self.absorbance_df = load_absorbance(self.absorbance_files)
            message = "Absorbance loaded" if self.absorbance_df is not None else "Error!"
            self.label5.setText(message)
            

    def open_library(self):
        # Open the file dialog and get the selected excel file
        # Load the file as pandas dataframe
        self.lib_path, _ = QFileDialog.getOpenFileName(self)
        if self.lib_path:
            self.label7.setText("Library loaded")
            self.library_df = pd.read_excel(self.lib_path)

    def open_spectrums(self):
        # Select one or multiple .txt files for reference spectrum
        # Open the file dialog and get the selected .txt files
        # Load the file as pandas dataframe
        self.spectrum_paths, _ = QFileDialog.getOpenFileNames(self)
        if self.spectrum_paths:
            self.refSpectrum_df = load_refSpectrum(self.spectrum_paths)
            self.label9.setText('Spectrums loaded')
        
    def select_rescaling(self, state):
        if state == Qt.Checked: 
            if self.sender() == self.checkBoxRescaling: 
                self.rescaling_flag = True
                if self.reflectance_files:
                    self.reflectance_rescaled_df = rescale_data(self.reflectance_df)
                if self.absorbance_files:
                    self.absorbance_rescaled_df = rescale_data(self.absorbance_df)

    def select_download(self, state):
        if state == Qt.Checked: 
            if self.sender() == self.checkBoxDownload: 
                self.download_flag = True
            

    def open_data(self):
        df_plot = {}
        if self.reflectance_files:
            df_plot['Reflectance'] = (self.reflectance_df, 'Reflectance')
        if self.absorbance_files:
            df_plot['Absorbance'] = (self.absorbance_df, 'Absorbance')
        if self.rescaling_flag:
            df_plot['Reflectance (Re-scaled)'] = (self.reflectance_rescaled_df, 'Reflectance')
            df_plot['Absorbance (Re-scaled)'] = (self.absorbance_rescaled_df, 'Absorbance')
            pass

        # This creates vizualization to plot multiple data
        viz(self.batchname, df_plot, fingerprint_library=self.library_df, 
            reference_Spectrums=self.refSpectrum_df,
            sensor=self.sensor, download=self.download_flag)
        # Check if del obj is possible
        self.reflectance_files = None
        self.absorbance_files = None
        self.reflectance_df = None
        self.absorbance_df = None
        self.batchname = None
        # self.library_df = None
        # self.rescaling_flag = False
        self.reflectance_rescaled_df = None
        self.absorbance_rescaled_df = None
        # self.download_flag = False
        self.label3.setText("")
        self.label5.setText("")
        # self.label7.setText("")



if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Window()
    window.show()
    sys.exit(app.exec())