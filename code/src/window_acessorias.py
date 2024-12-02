# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'window_acessorias.ui'
##
## Created by: Qt User Interface Compiler version 6.8.0
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QAbstractSpinBox, QApplication, QComboBox, QDateEdit,
    QDateTimeEdit, QFrame, QGridLayout, QLabel,
    QMainWindow, QMenuBar, QProgressBar, QPushButton,
    QSizePolicy, QSpacerItem, QStackedWidget, QStatusBar,
    QVBoxLayout, QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(754, 545)
        MainWindow.setMinimumSize(QSize(754, 545))
        MainWindow.setStyleSheet(u"")
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.verticalLayout = QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.grid_header = QGridLayout()
        self.grid_header.setObjectName(u"grid_header")
        self.line = QFrame(self.centralwidget)
        self.line.setObjectName(u"line")
        self.line.setMinimumSize(QSize(0, 5))
        self.line.setStyleSheet(u"background-color: rgb(85, 170, 255);")
        self.line.setLineWidth(0)
        self.line.setFrameShape(QFrame.Shape.HLine)
        self.line.setFrameShadow(QFrame.Shadow.Sunken)

        self.grid_header.addWidget(self.line, 2, 0, 1, 3)

        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.grid_header.addItem(self.horizontalSpacer_2, 0, 0, 1, 1)

        self.titulo = QLabel(self.centralwidget)
        self.titulo.setObjectName(u"titulo")
        font = QFont()
        font.setFamilies([u"Tw Cen MT"])
        font.setPointSize(28)
        font.setBold(True)
        self.titulo.setFont(font)
        self.titulo.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.grid_header.addWidget(self.titulo, 1, 1, 1, 1)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.grid_header.addItem(self.horizontalSpacer, 0, 2, 1, 1)

        self.logo = QLabel(self.centralwidget)
        self.logo.setObjectName(u"logo")
        self.logo.setMinimumSize(QSize(580, 160))
        self.logo.setMaximumSize(QSize(1060, 216))
        self.logo.setPixmap(QPixmap(u"../imgs/acessorias_hori.png"))
        self.logo.setScaledContents(True)

        self.grid_header.addWidget(self.logo, 0, 1, 1, 1)


        self.verticalLayout.addLayout(self.grid_header)

        self.stackedWidget = QStackedWidget(self.centralwidget)
        self.stackedWidget.setObjectName(u"stackedWidget")
        self.page_main = QWidget()
        self.page_main.setObjectName(u"page_main")
        self.verticalLayout_2 = QVBoxLayout(self.page_main)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.grid_main = QGridLayout()
        self.grid_main.setObjectName(u"grid_main")
        self.dateEdit_competencia = QDateEdit(self.page_main)
        self.dateEdit_competencia.setObjectName(u"dateEdit_competencia")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.dateEdit_competencia.sizePolicy().hasHeightForWidth())
        self.dateEdit_competencia.setSizePolicy(sizePolicy)
        self.dateEdit_competencia.setMinimumSize(QSize(250, 0))
        font1 = QFont()
        font1.setPointSize(12)
        font1.setItalic(False)
        self.dateEdit_competencia.setFont(font1)
        self.dateEdit_competencia.setButtonSymbols(QAbstractSpinBox.ButtonSymbols.UpDownArrows)
        self.dateEdit_competencia.setMinimumDateTime(QDateTime(QDate(2024, 9, 14), QTime(0, 0, 0)))
        self.dateEdit_competencia.setMinimumDate(QDate(2024, 9, 14))
        self.dateEdit_competencia.setCurrentSection(QDateTimeEdit.Section.MonthSection)
        self.dateEdit_competencia.setCalendarPopup(False)
        self.dateEdit_competencia.setDate(QDate(2024, 10, 15))

        self.grid_main.addWidget(self.dateEdit_competencia, 3, 2, 1, 1)

        self.label_usuario = QLabel(self.page_main)
        self.label_usuario.setObjectName(u"label_usuario")
        font2 = QFont()
        font2.setFamilies([u"Yu Gothic UI"])
        font2.setPointSize(16)
        self.label_usuario.setFont(font2)

        self.grid_main.addWidget(self.label_usuario, 0, 2, 1, 1)

        self.comboBox_usuario = QComboBox(self.page_main)
        self.comboBox_usuario.addItem("")
        self.comboBox_usuario.setObjectName(u"comboBox_usuario")
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Minimum)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.comboBox_usuario.sizePolicy().hasHeightForWidth())
        self.comboBox_usuario.setSizePolicy(sizePolicy1)
        font3 = QFont()
        font3.setPointSize(12)
        self.comboBox_usuario.setFont(font3)

        self.grid_main.addWidget(self.comboBox_usuario, 1, 2, 1, 1)

        self.horizontalSpacer_3 = QSpacerItem(40, 20, QSizePolicy.Policy.Maximum, QSizePolicy.Policy.Minimum)

        self.grid_main.addItem(self.horizontalSpacer_3, 2, 1, 1, 1)

        self.pushButton_upload = QPushButton(self.page_main)
        self.pushButton_upload.setObjectName(u"pushButton_upload")
        sizePolicy.setHeightForWidth(self.pushButton_upload.sizePolicy().hasHeightForWidth())
        self.pushButton_upload.setSizePolicy(sizePolicy)
        font4 = QFont()
        font4.setFamilies([u"Tw Cen MT"])
        font4.setPointSize(20)
        self.pushButton_upload.setFont(font4)
        self.pushButton_upload.setLayoutDirection(Qt.LayoutDirection.LeftToRight)
        icon = QIcon()
        icon.addFile(u"../imgs/upload-icon.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.pushButton_upload.setIcon(icon)
        self.pushButton_upload.setIconSize(QSize(64, 64))

        self.grid_main.addWidget(self.pushButton_upload, 1, 0, 3, 1)

        self.label_matriz = QLabel(self.page_main)
        self.label_matriz.setObjectName(u"label_matriz")
        font5 = QFont()
        font5.setFamilies([u"Yu Gothic UI"])
        font5.setPointSize(18)
        font5.setBold(False)
        self.label_matriz.setFont(font5)
        self.label_matriz.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.grid_main.addWidget(self.label_matriz, 0, 0, 1, 1)

        self.frame = QFrame(self.page_main)
        self.frame.setObjectName(u"frame")
        self.frame.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame.setFrameShadow(QFrame.Shadow.Raised)
        self.gridLayout_4 = QGridLayout(self.frame)
        self.gridLayout_4.setObjectName(u"gridLayout_4")
        self.pushButton_enviar = QPushButton(self.frame)
        self.pushButton_enviar.setObjectName(u"pushButton_enviar")
        sizePolicy.setHeightForWidth(self.pushButton_enviar.sizePolicy().hasHeightForWidth())
        self.pushButton_enviar.setSizePolicy(sizePolicy)
        self.pushButton_enviar.setMinimumSize(QSize(300, 50))
        self.pushButton_enviar.setMaximumSize(QSize(200, 16777215))
        font6 = QFont()
        font6.setPointSize(16)
        self.pushButton_enviar.setFont(font6)

        self.gridLayout_4.addWidget(self.pushButton_enviar, 1, 0, 1, 1)


        self.grid_main.addWidget(self.frame, 5, 0, 1, 3)

        self.label_competencia = QLabel(self.page_main)
        self.label_competencia.setObjectName(u"label_competencia")
        self.label_competencia.setFont(font2)

        self.grid_main.addWidget(self.label_competencia, 2, 2, 1, 1)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Maximum)

        self.grid_main.addItem(self.verticalSpacer, 4, 1, 1, 1)


        self.verticalLayout_2.addLayout(self.grid_main)

        self.stackedWidget.addWidget(self.page_main)
        self.page_load = QWidget()
        self.page_load.setObjectName(u"page_load")
        self.gridLayout = QGridLayout(self.page_load)
        self.gridLayout.setObjectName(u"gridLayout")
        self.horizontalSpacer_4 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout.addItem(self.horizontalSpacer_4, 1, 0, 1, 1)

        self.horizontalSpacer_7 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout.addItem(self.horizontalSpacer_7, 1, 2, 1, 1)

        self.load_movie = QLabel(self.page_load)
        self.load_movie.setObjectName(u"load_movie")
        self.load_movie.setMinimumSize(QSize(128, 128))
        self.load_movie.setMaximumSize(QSize(192, 192))
        self.load_movie.setPixmap(QPixmap(u"../imgs/load.gif"))
        self.load_movie.setScaledContents(True)
        self.load_movie.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout.addWidget(self.load_movie, 1, 1, 1, 1)

        self.load_title = QLabel(self.page_load)
        self.load_title.setObjectName(u"load_title")
        font7 = QFont()
        font7.setFamilies([u"Yu Gothic UI"])
        font7.setPointSize(18)
        font7.setBold(False)
        font7.setItalic(True)
        self.load_title.setFont(font7)
        self.load_title.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout.addWidget(self.load_title, 2, 1, 1, 1)

        self.frame_2 = QFrame(self.page_load)
        self.frame_2.setObjectName(u"frame_2")
        self.frame_2.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_2.setFrameShadow(QFrame.Shadow.Raised)
        self.gridLayout_2 = QGridLayout(self.frame_2)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.gridLayout_2.setContentsMargins(75, -1, 75, -1)
        self.progressBar = QProgressBar(self.frame_2)
        self.progressBar.setObjectName(u"progressBar")
        font8 = QFont()
        font8.setPointSize(13)
        self.progressBar.setFont(font8)
        self.progressBar.setValue(0)
        self.progressBar.setTextVisible(True)

        self.gridLayout_2.addWidget(self.progressBar, 0, 0, 1, 1)


        self.gridLayout.addWidget(self.frame_2, 4, 0, 1, 3)

        self.verticalSpacer_2 = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.gridLayout.addItem(self.verticalSpacer_2, 8, 0, 1, 3)

        self.verticalSpacer_3 = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.gridLayout.addItem(self.verticalSpacer_3, 3, 1, 1, 1)

        self.verticalSpacer_4 = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.gridLayout.addItem(self.verticalSpacer_4, 0, 1, 1, 1)

        self.stackedWidget.addWidget(self.page_load)

        self.verticalLayout.addWidget(self.stackedWidget)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 754, 22))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        self.statusbar.setStyleSheet(u"background-color: rgb(85, 170, 255);")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)

        self.stackedWidget.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"Consultor Acessorias", None))
        self.titulo.setText(QCoreApplication.translate("MainWindow", u"Consultor Acessorias", None))
        self.logo.setText("")
        self.dateEdit_competencia.setDisplayFormat(QCoreApplication.translate("MainWindow", u"MM/yyyy", None))
        self.label_usuario.setText(QCoreApplication.translate("MainWindow", u"Usu\u00e1rio Acessorias", None))
        self.comboBox_usuario.setItemText(0, QCoreApplication.translate("MainWindow", u"Wellington", None))

        self.pushButton_upload.setText(QCoreApplication.translate("MainWindow", u" Upload", None))
        self.label_matriz.setText(QCoreApplication.translate("MainWindow", u"Arquivo matriz", None))
        self.pushButton_enviar.setText(QCoreApplication.translate("MainWindow", u"Enviar", None))
        self.label_competencia.setText(QCoreApplication.translate("MainWindow", u"Data Compet\u00eancia", None))
        self.load_movie.setText("")
        self.load_title.setText(QCoreApplication.translate("MainWindow", u"Loading...", None))
    # retranslateUi

