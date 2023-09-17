
from runner import ModelRunner
from PyQt6 import QtCore, QtGui, QtWidgets

STYLE_IMAGE1 = 'StyleImages/monet.jpg'
STYLE_IMAGE2 = 'StyleImages/munch.jpg'
STYLE_IMAGE3 = 'StyleImages/van gogh.jpg'
ORIGINAL_IMAGE = 'OriginalImages/02.jpg'

def ui_update_image1(event):
    # change a picture on the gui
    # notice that at the bottom of the file your UI class is named ui
    # ui = Ui_MainWindow()
    # so you can use ui.object_name to access its member
    ui.label.setFrameShape(QtWidgets.QFrame.Shape.NoFrame)
    ui.label_2.setFrameShape(QtWidgets.QFrame.Shape.NoFrame)
    ui.label_3.setFrameShape(QtWidgets.QFrame.Shape.NoFrame)
    ui.worker.runner.set_style_image(STYLE_IMAGE1)
    ui.label.setFrameShape(QtWidgets.QFrame.Shape.Panel)
    ui.label.setLineWidth(10)

def ui_update_image2(event):
    # change a picture on the gui
    # notice that at the bottom of the file your UI class is named ui
    # ui = Ui_MainWindow()
    # so you can use ui.object_name to access its member
    ui.label.setFrameShape(QtWidgets.QFrame.Shape.NoFrame)
    ui.label_2.setFrameShape(QtWidgets.QFrame.Shape.NoFrame)
    ui.label_3.setFrameShape(QtWidgets.QFrame.Shape.NoFrame)
    ui.worker.runner.set_style_image(STYLE_IMAGE2)
    ui.label_2.setFrameShape(QtWidgets.QFrame.Shape.Panel)
    ui.label_2.setLineWidth(10)

def ui_update_image3(event):
    # change a picture on the gui
    # notice that at the bottom of the file your UI class is named ui
    # ui = Ui_MainWindow()
    # so you can use ui.object_name to access its member
    ui.label.setFrameShape(QtWidgets.QFrame.Shape.NoFrame)
    ui.label_2.setFrameShape(QtWidgets.QFrame.Shape.NoFrame)
    ui.label_3.setFrameShape(QtWidgets.QFrame.Shape.NoFrame)
    ui.worker.runner.set_style_image(STYLE_IMAGE3)
    ui.label_3.setFrameShape(QtWidgets.QFrame.Shape.Panel)
    ui.label_3.setLineWidth(10)

def ui_update_output_image(filename):
    pixmap = QtGui.QPixmap(filename)
    ui.label_5.setPixmap(pixmap)


# def ui_update_progressbar(RT,step):  #called by runner thread
#     ui.progressBar.setValue(int(step/RT.total_step*100))
    # print(f'updated progress bar: {int(step/RT.total_step*100)}')


class RunnerThread(QtCore.QObject):
    def __init__(self):
        super(RunnerThread, self).__init__()
        self.runner = ModelRunner(STYLE_IMAGE1,ORIGINAL_IMAGE)
        self.total_step = 300

    def perform_style_transfer(self):
        self.runner.calculate_os_features()
        for step in range(self.total_step):
            # Do some ui update here for example the progress bar
            # ui_update_progressbar(self, step)
            self.runner.train_one_step(step)
            if step % self.runner.get_output_interval() == 0:
                try:
                    ui_update_output_image('ResultImages/'+'generated' + str(step) + '.png')
                except:
                    None
                # do some ui update here for example update the generated image
                # here I just do some dummy things.
                print(step)


class Ui_MainWindow(object):
    def __init__(self):
        self.worker = RunnerThread()
        self.thread = QtCore.QThread()
        self.worker.moveToThread(self.thread)
        self.thread.start()

    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 600)
        MainWindow.setStyleSheet("background-color: rgb(6, 35, 61);")
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        # self.progressBar = QtWidgets.QProgressBar(self.centralwidget)
        # self.progressBar.setGeometry(QtCore.QRect(50, 510, 561, 31))
        # self.progressBar.setStyleSheet("QProgressBar::chunk {\n"
        #                                "    border-top-left-radius: 13px;\n"
        #                                "    border-bottom-left-radius: 13px;\n"
        #                                "    background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:1, stop:0 rgba(0, 108, 184, 255), stop:1 rgba(0, 198, 176, 255));\n"
        #                                "}\n"
        #                                "QProgressBar {\n"
        #                                "    border: 2px ;\n"
        #                                "    border-radius: 15px;\n"
        #                                "    background-color: rgb(6, 26, 44);\n"
        #                                "    text-align: center;\n"
        #                                "}")
        # self.progressBar.setProperty("value", 0)
        # self.progressBar.setAlignment(QtCore.Qt.AlignmentFlag.AlignLeading | QtCore.Qt.AlignmentFlag.AlignLeft | QtCore.Qt.AlignmentFlag.AlignVCenter)
        # self.progressBar.setTextVisible(True)
        # self.progressBar.setInvertedAppearance(False)
        # self.progressBar.setObjectName("progressBar")
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(345, 500, 91, 51))
        font = QtGui.QFont()
        font.setFamily("Arial Black")
        font.setBold(True)
        font.setWeight(75)
        self.pushButton.setFont(font)
        self.pushButton.setStyleSheet(
            "background:qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:1, stop:0 rgba(255, 46, 0, 255), stop:1 rgba(255, 203, 0, 255));\n"
            "border-radius:15px;\n"
            "")
        self.pushButton.setObjectName("pushButton")
        self.pushButton.clicked.connect(self.worker.perform_style_transfer)
        self.textBrowser = QtWidgets.QTextBrowser(self.centralwidget)
        self.textBrowser.setGeometry(QtCore.QRect(10, 0, 281, 41))
        self.textBrowser.setStyleSheet("color: rgb(231, 231, 231);\n"
                                       "border: 0px;")
        self.textBrowser.setObjectName("textBrowser")
        self.textBrowser_2 = QtWidgets.QTextBrowser(self.centralwidget)
        self.textBrowser_2.setGeometry(QtCore.QRect(290, 0, 251, 41))
        self.textBrowser_2.setStyleSheet("color: rgb(231, 231, 231);\n"
                                         "border: 0px;")
        self.textBrowser_2.setObjectName("textBrowser_2")
        self.textBrowser_3 = QtWidgets.QTextBrowser(self.centralwidget)
        self.textBrowser_3.setGeometry(QtCore.QRect(550, 0, 231, 41))
        self.textBrowser_3.setStyleSheet("color: rgb(231, 231, 231);\n"
                                         "border: 0px;")
        self.textBrowser_3.setObjectName("textBrowser_3")
        self.textBrowser_4 = QtWidgets.QTextBrowser(self.centralwidget)
        self.textBrowser_4.setGeometry(QtCore.QRect(430, 430, 331, 51))
        self.textBrowser_4.setStyleSheet("color: rgb(231, 231, 231);\n"
                                         "border: 0px;\n"
                                         "")
        self.textBrowser_4.setObjectName("textBrowser_4")
        self.textBrowser_5 = QtWidgets.QTextBrowser(self.centralwidget)
        self.textBrowser_5.setGeometry(QtCore.QRect(40, 430, 331, 51))
        self.textBrowser_5.setStyleSheet("color: rgb(231, 231, 231);\n"
                                         "border: 0px;")
        self.textBrowser_5.setObjectName("textBrowser_5")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(50, 40, 171, 131))
        self.label.setText("")
        self.label.setPixmap(QtGui.QPixmap(STYLE_IMAGE1))
        # self.label.clicked.connect(ui_update_image(STYLE_IMAGE1,1))  #label 1 click

        self.label.setScaledContents(True)
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(310, 40, 171, 131))
        self.label_2.setText("")
        self.label_2.setPixmap(QtGui.QPixmap(STYLE_IMAGE2))
        # self.label_2.clicked.connect(ui_update_image(STYLE_IMAGE2,2)) #label 2 click

        self.label_2.setScaledContents(True)
        self.label_2.setObjectName("label_2")
        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_3.setGeometry(QtCore.QRect(570, 40, 171, 131))
        self.label_3.setText("")
        self.label_3.setPixmap(QtGui.QPixmap(STYLE_IMAGE3))
        # self.label_3.clicked.connect(ui_update_image(STYLE_IMAGE3,3)) #label 3 click

        self.label_3.setScaledContents(True)
        self.label_3.setObjectName("label_3")
        self.label_4 = QtWidgets.QLabel(self.centralwidget)
        self.label_4.setGeometry(QtCore.QRect(50, 200, 301, 231))
        self.label_4.setText("")
        self.label_4.setPixmap(QtGui.QPixmap(ORIGINAL_IMAGE))
        self.label_4.setScaledContents(True)
        self.label_4.setObjectName("label_4")
        self.label_5 = QtWidgets.QLabel(self.centralwidget)
        self.label_5.setGeometry(QtCore.QRect(440, 200, 301, 231))
        self.label_5.setText("")
        self.label_5.setPixmap(QtGui.QPixmap(ORIGINAL_IMAGE))
        self.label_5.setScaledContents(True)
        self.label_5.setObjectName("label_5")

        self.label.mousePressEvent = ui_update_image1
        self.label_2.mousePressEvent = ui_update_image2
        self.label_3.mousePressEvent = ui_update_image3


        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 24))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        # self.statusbar = QtWidgets.QStatusBar(MainWindow)
        # self.statusbar.setObjectName("statusbar")
        # MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)


        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.pushButton.setText(_translate("MainWindow", "Start"))
        self.textBrowser.setHtml(_translate("MainWindow",
                                            "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
                                            "<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
                                            "p, li { white-space: pre-wrap; }\n"
                                            "</style></head><body style=\" font-family:\'SimSun\'; font-size:9pt; font-weight:400; font-style:normal;\">\n"
                                            "<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">Claude Monet</p></body></html>"))
        self.textBrowser_2.setHtml(_translate("MainWindow",
                                              "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
                                              "<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
                                              "p, li { white-space: pre-wrap; }\n"
                                              "</style></head><body style=\" font-family:\'SimSun\'; font-size:9pt; font-weight:400; font-style:normal;\">\n"
                                              "<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">Edvard Munch</p></body></html>"))
        self.textBrowser_3.setHtml(_translate("MainWindow",
                                              "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
                                              "<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
                                              "p, li { white-space: pre-wrap; }\n"
                                              "</style></head><body style=\" font-family:\'SimSun\'; font-size:9pt; font-weight:400; font-style:normal;\">\n"
                                              "<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">Vincent Van Gogh</p></body></html>"))
        self.textBrowser_4.setHtml(_translate("MainWindow",
                                              "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
                                              "<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
                                              "p, li { white-space: pre-wrap; }\n"
                                              "</style></head><body style=\" font-family:\'SimSun\'; font-size:9pt; font-weight:400; font-style:normal;\">\n"
                                              "<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">Generated Image</p></body></html>"))
        self.textBrowser_5.setHtml(_translate("MainWindow",
                                              "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
                                              "<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
                                              "p, li { white-space: pre-wrap; }\n"
                                              "</style></head><body style=\" font-family:\'SimSun\'; font-size:9pt; font-weight:400; font-style:normal;\">\n"
                                              "<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">Original Image</p></body></html>"))


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec())

# class Ui_MainWindow(object):
# 	# add this __init__() function in your own ui class.
# 	def __init__(self):
# 		self.worker = RunnerThread()
# 		self.thread = QtCore.QThread()
# 		self.worker.moveToThread(self.thread)
# 		self.thread.start()
# 	# just an example your ui.py file will have the same structure but not the same content.
# 	def setupUi(self, MainWindow):
# 		MainWindow.setObjectName("MainWindow")
# 		MainWindow.resize(941, 646)
# 		MainWindow.setStyleSheet("background-color: rgb(255, 255, 255)")
# 		self.centralwidget = QtWidgets.QWidget(MainWindow)
# 		self.centralwidget.setStyleSheet("")
# 		self.centralwidget.setObjectName("centralwidget")
# 		# A picture placeholder.
# 		self.Image = QtWidgets.QLabel(self.centralwidget)
# 		self.Image.setGeometry(QtCore.QRect(570, 220, 320, 240))
# 		self.Image.setText("")
# 		self.Image.setPixmap(QtGui.QPixmap("small.jpg"))
# 		self.Image.setScaledContents(True)
# 		self.Image.setObjectName("Generated")
# 		# Suppose I have a button called transfer.
# 		# I want to start the style transfer when I click it.
# 		self.Transfer = QtWidgets.QPushButton(self.centralwidget)
# 		self.Transfer.setGeometry(QtCore.QRect(660, 530, 231, 31))
# 		self.Transfer.setObjectName("Transfer")
# 		# This line does the job.
# 		self.Transfer.clicked.connect(self.worker.perform_style_transfer)
#
# 	def retranslateUi(self, MainWindow):
# 		_translate = QtCore.QCoreApplication.translate
# 		MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
#
#
# if __name__ == "__main__":
#     import sys
#     app = QtWidgets.QApplication(sys.argv)
#     MainWindow = QtWidgets.QMainWindow()
#     ui = Ui_MainWindow()
#     ui.setupUi(MainWindow)
#     MainWindow.show()
#     sys.exit(app.exec_())
