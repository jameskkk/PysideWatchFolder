# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'main_window.ui'
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
from PySide6.QtWidgets import (QApplication, QLabel, QMainWindow, QPushButton,
    QSizePolicy, QVBoxLayout, QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(320, 200)
        MainWindow.setDockNestingEnabled(True)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(1)
        sizePolicy.setHeightForWidth(self.centralwidget.sizePolicy().hasHeightForWidth())
        self.centralwidget.setSizePolicy(sizePolicy)
        self.verticalLayout = QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.select_folder_label = QLabel(self.centralwidget)
        self.select_folder_label.setObjectName(u"select_folder_label")
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.select_folder_label.sizePolicy().hasHeightForWidth())
        self.select_folder_label.setSizePolicy(sizePolicy1)

        self.verticalLayout.addWidget(self.select_folder_label)

        self.select_button = QPushButton(self.centralwidget)
        self.select_button.setObjectName(u"select_button")
        sizePolicy1.setHeightForWidth(self.select_button.sizePolicy().hasHeightForWidth())
        self.select_button.setSizePolicy(sizePolicy1)

        self.verticalLayout.addWidget(self.select_button)

        self.fetch_button = QPushButton(self.centralwidget)
        self.fetch_button.setObjectName(u"fetch_button")
        sizePolicy1.setHeightForWidth(self.fetch_button.sizePolicy().hasHeightForWidth())
        self.fetch_button.setSizePolicy(sizePolicy1)

        self.verticalLayout.addWidget(self.fetch_button)

        self.folder_label = QLabel(self.centralwidget)
        self.folder_label.setObjectName(u"folder_label")
        self.folder_label.setAlignment(Qt.AlignmentFlag.AlignLeading|Qt.AlignmentFlag.AlignLeft|Qt.AlignmentFlag.AlignTop)
        self.folder_label.setWordWrap(True)

        self.verticalLayout.addWidget(self.folder_label)

        self.status_label = QLabel(self.centralwidget)
        self.status_label.setObjectName(u"status_label")
        sizePolicy2 = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Ignored)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.status_label.sizePolicy().hasHeightForWidth())
        self.status_label.setSizePolicy(sizePolicy2)
        self.status_label.setAlignment(Qt.AlignmentFlag.AlignLeading|Qt.AlignmentFlag.AlignLeft|Qt.AlignmentFlag.AlignTop)
        self.status_label.setWordWrap(True)

        self.verticalLayout.addWidget(self.status_label)

        self.verticalLayout.setStretch(0, 1)
        self.verticalLayout.setStretch(1, 1)
        self.verticalLayout.setStretch(3, 2)
        self.verticalLayout.setStretch(4, 3)
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"Watch Folder", None))
        self.select_folder_label.setText(QCoreApplication.translate("MainWindow", u"Select a directory to monitor: ", None))
        self.select_button.setText(QCoreApplication.translate("MainWindow", u"Select Directory", None))
        self.fetch_button.setText(QCoreApplication.translate("MainWindow", u"Fetch Data", None))
        self.folder_label.setText(QCoreApplication.translate("MainWindow", u"No directory selected.", None))
        self.status_label.setText(QCoreApplication.translate("MainWindow", u"Not monitoring...", None))
    # retranslateUi

