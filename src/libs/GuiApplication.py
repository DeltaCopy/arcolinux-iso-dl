from PyQt5 import QtCore, QtGui, QtWidgets, uic
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import sys, traceback, os, tomli, time, threading
from datetime import datetime
import libs.Resources
from libs.ResponseThread import ResponseThread
from libs.DownloadThread import DownloadThread
from libs.ISO import ISO
from libs.ValidateThread import ValidateThread
from libs.ArcoMetadata import ArcoMetadata
from libs.PackageThread import PackageThread
from providers.Sourceforge import Sourceforge
import hashlib
import tomli
import pathlib
import subprocess
import datetime


RAW_PACKAGE_LIST_ARCOLINUX = "https://raw.githubusercontent.com/arcolinux/${ISO}/master/archiso/packages.x86_64"
RAW_PACKAGE_LIST_ARCOLINUXB = "https://raw.githubusercontent.com/arcolinuxb/${ISO}/master/archiso/packages.x86_64"


'''
Class: GuiApplication
Purpose: This is the front-end code for the UI to the main application.
'''

class GuiApplication(QMainWindow):
    def __init__(self,settings):
        self.settings = settings
        super(GuiApplication,self).__init__()

        self.load_main_window()

        self.show()

    # Main method to add gui components

    def load_main_window(self):

        self.setWindowIcon(QtGui.QIcon(":/app_images/images/arcolinux.png"))

        self.setObjectName("MainWindow")
        self.setEnabled(True)

        self.setFixedSize(605, 572)
        self.setWindowTitle("ArcoLinux ISO Downloader")

        self.centralwidget = QtWidgets.QWidget(self)
        self.centralwidget.setMaximumSize(QtCore.QSize(800, 800))
        self.centralwidget.setObjectName("centralwidget")

        self.comboBox_ISO = QtWidgets.QComboBox(self.centralwidget)
        self.comboBox_ISO.setGeometry(QtCore.QRect(130, 20, 281, 39))
        self.comboBox_ISO.setObjectName("comboBox_ISO")


        self.pushButton_exportPkgList = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_exportPkgList.setGeometry(QtCore.QRect(180, 480, 151, 39))
        self.pushButton_exportPkgList.setObjectName("pushButton_exportPkgList")
        self.pushButton_exportPkgList.setText("Export package list")
        self.pushButton_exportPkgList.setIcon(QtGui.QIcon(":/app_images/images/export.png"))

        self.label_packages_ISO = QtWidgets.QLabel(self.centralwidget)
        self.label_packages_ISO.setGeometry(QtCore.QRect(10, 210, 111, 17))
        self.label_packages_ISO.setObjectName("label_packages_ISO")
        self.label_packages_ISO.setText("Packages-x86_64:")

        self.label_selectISO = QtWidgets.QLabel(self.centralwidget)
        self.label_selectISO.setGeometry(QtCore.QRect(10, 30, 91, 20))
        self.label_selectISO.setObjectName("label_selectISO")
        self.label_selectISO.setText("ISO:")

        self.pushButton_download_ISO = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_download_ISO.setGeometry(QtCore.QRect(330, 480, 141, 39))
        self.pushButton_download_ISO.setObjectName("pushButton_download_ISO")
        self.pushButton_download_ISO.setText("Download ISO")
        self.pushButton_download_ISO.setIcon(QtGui.QIcon(":/app_images/images/download.png"))

        self.plainTextEdit_ISO_Desc = QtWidgets.QPlainTextEdit(self.centralwidget)
        self.plainTextEdit_ISO_Desc.setEnabled(True)
        self.plainTextEdit_ISO_Desc.setGeometry(QtCore.QRect(130, 70, 441, 121))

        font = QtGui.QFont()
        font.setBold(False)
        font.setWeight(50)

        self.plainTextEdit_ISO_Desc.setFont(font)
        self.plainTextEdit_ISO_Desc.setReadOnly(True)
        self.plainTextEdit_ISO_Desc.setObjectName("plainTextEdit_ISO_Desc")

        self.label_packages_ISO_Desc = QtWidgets.QLabel(self.centralwidget)
        self.label_packages_ISO_Desc.setGeometry(QtCore.QRect(10, 80, 71, 17))
        self.label_packages_ISO_Desc.setObjectName("label_packages_ISO_Desc")
        self.label_packages_ISO_Desc.setText("Description:")

        self.label_iso_github = QtWidgets.QLabel(self.centralwidget)
        self.label_iso_github.setGeometry(QtCore.QRect(180, 450, 321, 17))

        font = QtGui.QFont()
        font.setUnderline(False)
        self.label_iso_github.setFont(font)
        self.label_iso_github.setObjectName("label_iso_github")

        self.label_iso_pkgcount = QtWidgets.QLabel(self.centralwidget)
        self.label_iso_pkgcount.setGeometry(QtCore.QRect(250, 420, 191, 17))
        self.label_iso_pkgcount.setObjectName("label_iso_pkgcount")

        self.listWidget_pkglist = QtWidgets.QListWidget(self.centralwidget)
        self.listWidget_pkglist.setGeometry(QtCore.QRect(130, 200, 441, 211))
        self.listWidget_pkglist.setSelectionMode(QtWidgets.QAbstractItemView.MultiSelection)
        self.listWidget_pkglist.setViewMode(QtWidgets.QListView.ListMode)
        self.listWidget_pkglist.setObjectName("listWidget_pkglist")

        self.setCentralWidget(self.centralwidget)

        self.statusbar = QtWidgets.QStatusBar(self)
        self.statusbar.setObjectName("statusbar")
        self.setStatusBar(self.statusbar)

        self.menuBar = QtWidgets.QMenuBar(self)
        self.menuBar.setGeometry(QtCore.QRect(0, 0, 605, 29))
        self.menuBar.setObjectName("menuBar")

        self.menuFile = QtWidgets.QMenu(self.menuBar)
        self.menuFile.setObjectName("menuFile")
        self.menuFile.setTitle("&File")


        self.menuHelp = QtWidgets.QMenu(self.menuBar)
        self.menuHelp.setObjectName("menuHelp")
        self.menuHelp.setTitle("&Help")

        self.menuFind = QtWidgets.QMenu(self.menuBar)
        self.menuFind.setObjectName("menuFind")
        self.menuFind.setTitle("&Find")

        self.menuTools = QtWidgets.QMenu(self.menuBar)
        self.menuTools.setObjectName("menuTools")
        self.menuTools.setTitle("&Tools")

        self.setMenuBar(self.menuBar)

        self.actionExit_Downloader = QtWidgets.QAction(self)
        self.actionExit_Downloader.setObjectName("actionExit_Downloader")
        self.actionExit_Downloader.setText("Exit")

        self.actionAbout = QtWidgets.QAction(self)
        self.actionAbout.setObjectName("actionAbout")
        self.actionAbout.setText("About")

        self.actionSearch_remote_pkg = QtWidgets.QAction(self)
        self.actionSearch_remote_pkg.setObjectName("actionSearch_remote_pkg")
        self.actionSearch_remote_pkg.setText("Search remote packages")

        self.actionSearch_local_pkg_list = QtWidgets.QAction(self)
        self.actionSearch_local_pkg_list.setObjectName("actionSearch_local_pkg_list")
        self.actionSearch_local_pkg_list.setText("Search local packages")

        self.actionCheck_updates = QtWidgets.QAction(self)
        self.actionCheck_updates.setObjectName("actionCheck_updates")

        self.actionView_local_package_list = QtWidgets.QAction(self)
        self.actionView_local_package_list.setObjectName("actionView_local_package_list")
        self.actionView_local_pkglist = QtWidgets.QAction(self)
        self.actionView_local_pkglist.setObjectName("actionView_local_pkglist")

        self.actionExport_local_pkglist = QtWidgets.QAction(self)
        self.actionExport_local_pkglist.setObjectName("actionExport_local_pkglist")
        self.actionView_local_pkglist_view = QtWidgets.QAction(self)
        self.actionView_local_pkglist_view.setObjectName("actionView_local_pkglist_view")
        self.actionView_local_pkglist_view.setText("View local packages")

        self.actionCheck_for_package_updates = QtWidgets.QAction(self)
        self.actionCheck_for_package_updates.setObjectName("actionCheck_for_package_updates")
        self.actionCheck_for_package_updates.setText("Check pacman updates")

        self.menuFile.addAction(self.actionExit_Downloader)
        self.menuHelp.addAction(self.actionAbout)
        self.menuFind.addAction(self.actionSearch_remote_pkg)
        self.menuFind.addAction(self.actionSearch_local_pkg_list)
        self.menuTools.addAction(self.actionView_local_pkglist_view)
        self.menuTools.addAction(self.actionCheck_for_package_updates)
        self.menuBar.addAction(self.menuFile.menuAction())
        self.menuBar.addAction(self.menuFind.menuAction())
        self.menuBar.addAction(self.menuTools.menuAction())
        self.menuBar.addAction(self.menuHelp.menuAction())

        self.listWidget_pkglist.setCurrentRow(-1)
        QtCore.QMetaObject.connectSlotsByName(self)
        self.setTabOrder(self.comboBox_ISO, self.pushButton_exportPkgList)

        self.arcolinux_iso_dict = self.get_arcolinux_iso_dict()

        for arcolinux_iso in self.arcolinux_iso_dict:
            self.comboBox_ISO.addItem(arcolinux_iso)

        self.update_ISO_Desc()

        self.update_pkg_list_view(self.arcolinux_iso_dict)

        self.comboBox_ISO.currentTextChanged.connect(lambda: self.update_ISO_Desc())

        self.comboBox_ISO.currentTextChanged.connect(lambda: self.update_pkg_list_view(self.arcolinux_iso_dict))

        self.pushButton_download_ISO.clicked.connect(lambda: self.display_download_dialog())
        self.pushButton_download_ISO.setShortcut("Ctrl+D")

        self.pushButton_exportPkgList.clicked.connect(lambda: self.export_package_list(self.arcolinux_iso_dict))
        self.pushButton_exportPkgList.setShortcut("Ctrl+S")

        self.actionExit_Downloader.triggered.connect(lambda: sys.exit(0))
        self.actionExit_Downloader.setShortcut("Ctrl+Q")
        self.actionExit_Downloader.setIcon(QtGui.QIcon(":/app_images/images/close.png"))

        self.actionAbout.triggered.connect(lambda: self.display_about_dialog())
        self.actionAbout.setShortcut("Ctrl+H")
        self.actionAbout.setIcon(QtGui.QIcon(":/app_images/images/info.png"))

        self.actionSearch_remote_pkg.triggered.connect(lambda: self.display_search_dialog("remote"))
        self.actionSearch_remote_pkg.setShortcut("Ctrl+R")
        self.actionSearch_remote_pkg.setIcon(QtGui.QIcon(":/app_images/images/search.png"))

        self.actionExport_local_pkglist.triggered.connect(lambda: self.generate_local_pkg_list())

        self.actionSearch_local_pkg_list.triggered.connect(lambda: self.display_search_dialog("local"))
        self.actionSearch_local_pkg_list.setShortcut("Ctrl+L")
        self.actionSearch_local_pkg_list.setIcon(QtGui.QIcon(":/app_images/images/search.png"))

        self.actionView_local_pkglist_view.triggered.connect(lambda: self.display_local_pkg_list())
        self.actionView_local_pkglist_view.setIcon(QtGui.QIcon(":/app_images/images/view.png"))

        self.actionCheck_for_package_updates.triggered.connect(lambda: self.pkg_updates())
        self.actionCheck_for_package_updates.setIcon(QtGui.QIcon(":/app_images/images/update.png"))

    def pkg_updates(self):
        yay_cmd = "/usr/bin/yay"
        if os.path.exists(yay_cmd):
            process_pkg_update = 1
            print("Running %s -%s" %(yay_cmd, "Sy"))
            process_pkg_update = subprocess.check_call([yay_cmd, "-Sy"])

            if process_pkg_update == 0:

                process_pkg_updates =  subprocess.check_output([yay_cmd, '-Qu'])

                if process_pkg_updates is not None:
                    pkg_updates_len = len(process_pkg_updates.decode("utf-8").strip().split("\n"))


                    self.statusbar.setStyleSheet("font-weight: bold")

                    self.statusbar.showMessage(str("Package update(s) available = %s"% pkg_updates_len),5000)

    def display_local_pkg_list(self):

        self.local_pkg_t = PackageThread()
        self.local_pkg_t.start()
        self.local_pkg_t.join()

        if len(self.local_pkg_t.local_pkg_list) > 0:
            self.dialog_local_pkglist = QDialog(self)
            self.dialog_local_pkglist.setWindowTitle("Local packages list")
            self.dialog_local_pkglist.setFixedSize(605, 492)
            self.treeWidget_local_pkg_list = QtWidgets.QTreeWidget(self.dialog_local_pkglist)
            self.treeWidget_local_pkg_list.setGeometry(QtCore.QRect(10, 40, 585, 341))
            self.treeWidget_local_pkg_list.setObjectName("treetWidget_local_pkg_list")

            self.treeWidget_local_pkg_list.setColumnCount(4)

            self.treeWidget_local_pkg_list.setHeaderLabels(["Package","Size","Version","Install Date"])

            self.treeWidget_local_pkg_list.setColumnWidth(0,240)

            for pkg in self.local_pkg_t.local_pkg_list:
                treewidget_item_pkg = QTreeWidgetItem(self.treeWidget_local_pkg_list)
                treewidget_item_pkg.setText(0, pkg.name)
                treewidget_item_pkg.setText(1, pkg.size)
                treewidget_item_pkg.setText(2,pkg.version)
                treewidget_item_pkg.setText(3,pkg.install_date)
                treewidget_item_pkg.setToolTip(0,pkg.name)

            self.treeWidget_local_pkg_list.setSortingEnabled(False)


            self.label_local_pkg_x86_64 = QtWidgets.QLabel(self.dialog_local_pkglist)
            self.label_local_pkg_x86_64.setGeometry(QtCore.QRect(20, 20, 421, 17))
            self.label_local_pkg_x86_64.setObjectName("label_local_pkg_x86_64")
            self.label_local_pkg_x86_64.setText("Showing explicitly locally installed packages (pacman -Qiqe)")

            self.label_local_pkg_count = QtWidgets.QLabel(self.dialog_local_pkglist)
            self.label_local_pkg_count.setGeometry(QtCore.QRect(20, 390, 321, 17))
            self.label_local_pkg_count.setObjectName("label_local_pkg_count")
            self.label_local_pkg_count.setText("Package Count: %s" % len(self.local_pkg_t.local_pkg_list))

            self.pushButton_local_pkg_export = QtWidgets.QPushButton(self.dialog_local_pkglist)
            self.pushButton_local_pkg_export.setText("Export")
            self.pushButton_local_pkg_export.setGeometry(QtCore.QRect(200, 430, 90, 39))
            self.pushButton_local_pkg_export.setObjectName("pushButton_local_pkg_export")
            self.pushButton_local_pkg_export.setIcon(QtGui.QIcon(":/app_images/images/export.png"))
            self.pushButton_local_pkg_export.clicked.connect(lambda: self.export_local_pkg_list())

            self.pushButton_local_pkg_cancel = QtWidgets.QPushButton(self.dialog_local_pkglist)
            self.pushButton_local_pkg_cancel.setText("Cancel")
            self.pushButton_local_pkg_cancel.setIcon(QtGui.QIcon(":/app_images/images/cancel.png"))

            self.pushButton_local_pkg_cancel.setGeometry(QtCore.QRect(290, 430, 90, 39))
            self.pushButton_local_pkg_cancel.setObjectName("pushButton_local_pkg_cancel")
            self.pushButton_local_pkg_cancel.clicked.connect(lambda: self.cancel_pkglist())
            self.dialog_local_pkglist.setModal(True)
            self.dialog_local_pkglist.exec_()
            self.destroy_local_pkg_thread()


    def cancel_pkglist(self):
        self.dialog_local_pkglist.close()
        self.show()

    # Arch Linux only method, export local package list
    def export_local_pkg_list(self):

        filename = format("%s/%s-local-packages.x86_64.txt" % (str(pathlib.Path.home()),datetime.datetime.now().strftime("%Y%m%d")))


        if len(self.local_pkg_t.local_pkg_list) > 0:

            pkg_txt_save_filename = QFileDialog.getSaveFileName(self,
                                        str("Save packages.x86_64 file"), filename,str("TXT Files (*.txt)"))

            if len(pkg_txt_save_filename[0]) > 0:
                with open(pkg_txt_save_filename[0], mode="w") as f:
                    f.write("#####################################################################\n")
                    f.write("# Auto Generated by ArcoLinux ISO Downloader on %s\n"% datetime.datetime.now().strftime("%Y-%m-%d"))
                    f.write("#####################################################################\n")

                    for pkg in self.local_pkg_t.local_pkg_list:

                        f.write("%s\n" % (pkg.name))

            if os.path.exists(pkg_txt_save_filename[0]):
                self.statusbar.setStyleSheet("font-weight: bold")
                self.statusbar.showMessage(str("Package Export Completed"),5000)

    # Display search dialog box
    def display_search_dialog(self,search):
        self.search_dialog = QDialog(self)
        self.search_dialog.setFixedSize(493, 119)
        self.pushButton_find_pkg = QtWidgets.QPushButton(self.search_dialog)
        self.pushButton_find_pkg.setGeometry(QtCore.QRect(100, 50, 90, 39))
        self.pushButton_find_pkg.setObjectName("pushButton_find_pkg")
        self.pushButton_find_pkg.setText("Find")
        self.pushButton_find_pkg.setIcon(QtGui.QIcon(":/app_images/images/search.png"))
        self.pushButton_cancel_find = QtWidgets.QPushButton(self.search_dialog)
        self.pushButton_cancel_find.setGeometry(QtCore.QRect(200, 50, 90, 39))
        self.pushButton_cancel_find.setObjectName("pushButton_cancel_find")
        self.pushButton_cancel_find.setText("Cancel")

        if search == "local":
            self.search_dialog.setWindowTitle("Search local packages")
        elif search == "remote":
            self.search_dialog.setWindowTitle("Search remote packages: %s" % self.comboBox_ISO.currentText())

        self.pushButton_cancel_find.clicked.connect(lambda: self.cancel_find())
        self.pushButton_cancel_find.setIcon(QtGui.QIcon(":/app_images/images/cancel.png"))

        self.pushButton_find_pkg.clicked.connect(lambda: self.find(search))

        self.label_search = QtWidgets.QLabel(self.search_dialog)
        self.label_search.setGeometry(QtCore.QRect(10, 20, 91, 17))
        self.label_search.setObjectName("label_search")
        self.label_search.setText("Package Name:")
        self.lineEdit_search_pkg = QtWidgets.QLineEdit(self.search_dialog)
        self.lineEdit_search_pkg.setGeometry(QtCore.QRect(100, 10, 391, 39))
        self.lineEdit_search_pkg.setObjectName("lineEdit_search_pkg")

        self.label_search_status = QtWidgets.QLabel(self.search_dialog)
        self.label_search_status.setGeometry(QtCore.QRect(10, 90, 421, 17))
        self.label_search_status.setObjectName("label_search_status")
        self.label_search_status.setVisible(False)

        self.search_dialog.setModal(True)
        self.lineEdit_search_pkg.setFocus()
        self.search_dialog.exec_()

    # Find method, if searching remote package list search through the listwidget items

    def find(self,search):

        if len(self.lineEdit_search_pkg.text()) > 0 and self.lineEdit_search_pkg.text().isspace() == False:
            search_term = self.lineEdit_search_pkg.text()
            self.listWidget_pkglist_find = QListWidget(self.search_dialog)
            self.listWidget_pkglist_find.setObjectName("listWidget_pkglist_find")
            self.listWidget_pkglist_find.setGeometry(QRect(0, 110, 490, 200))
            self.listWidget_pkglist_find.setSortingEnabled(True)
            self.listWidget_pkglist_find.setVisible(False)

            if search == "remote":


                matches = self.listWidget_pkglist.findItems(search_term,Qt.MatchContains)
                if len(matches) > 0:

                    self.label_search_status.setText("%s packages found" % len(matches))
                    self.label_search_status.setVisible(True)

                    self.listWidget_pkglist_find.setSortingEnabled(True)
                    self.search_dialog.setFixedSize(493, 330)
                    self.listWidget_pkglist_find.setVisible(True)


                    row = 0

                    for m in matches:

                        self.listWidgetItem = QListWidgetItem()

                        self.listWidgetItem.setText(m.text())
                        self.listWidget_pkglist_find.insertItem(row,self.listWidgetItem)
                        row +=1

                else:
                    self.search_dialog.setFixedSize(493, 114)
                    self.label_search_status.setText("%s packages found" % len(matches))
                    self.label_search_status.setVisible(True)


            elif search == "local":
                self.local_pkg_t = PackageThread()
                self.local_pkg_t.start()
                self.local_pkg_t.join()

                if len(self.local_pkg_t.local_pkg_list) > 0:

                    search_res = []
                    for pkg in self.local_pkg_t.local_pkg_list:
                        if search_term in pkg.name:
                            search_res.append(pkg.name)

                    self.destroy_local_pkg_thread()
                    if len(search_res) > 0:
                        self.label_search_status.setText("%s packages found" % len(search_res))
                        self.label_search_status.setVisible(True)

                        self.search_dialog.setFixedSize(493, 330)
                        self.listWidget_pkglist_find.setVisible(True)

                        row = 0

                        for s in search_res:

                            self.listWidgetItem = QListWidgetItem()

                            self.listWidgetItem.setText(s)
                            self.listWidget_pkglist_find.insertItem(row,self.listWidgetItem)
                            row +=1

                        self.label_search_status.setText("%s packages found" % len(search_res))
                        self.label_search_status.setVisible(True)
                    else:
                        self.search_dialog.setFixedSize(493, 114)
                        self.label_search_status.setText("%s packages found" % len(search_res))
                        self.label_search_status.setVisible(True)
        else:
            self.lineEdit_search_pkg.setText("")
            self.lineEdit_search_pkg.setFocus(True)

    # Attached to cancel find button
    def cancel_find(self):
        self.search_dialog.close()
        self.show()

    # display about dialog
    def display_about_dialog(self):
        self.about_dialog = QDialog(self)
        self.about_dialog.setFixedSize(432, 420)
        self.label_about = QtWidgets.QLabel(self.about_dialog)
        self.label_about.setGeometry(QtCore.QRect(30, 30, 381, 400))
        self.label_about.setObjectName("label_about")
        self.label_about.setText("<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"</style></head><body style=\" font-family:\'Noto Sans\'; font-size:9pt; font-weight:400; font-style:normal;\">\n"
"<p align=\"center\" dir=\'rtl\' style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:10pt; font-weight:600;\">ArcoLinux ISO Downloader</span></p>\n"
"<p align=\"center\" style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">An unofficial ArcoLinux application</p>\n"
"<p align=\"center\" style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><img src=\":/app_images/images/arcolinux.png\" /></p>\n"
"<p align=\"center\" style=\"-qt-paragraph-type:empty; margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p>\n"
"<p align=\"center\" style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">* Explore/Export package lists from GitHub</p>\n"
"<p align=\"center\" style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">* Explore/Download ISOs from SourceForge</p>\n"
"<p align=\"center\" style=\"-qt-paragraph-type:empty; margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p>\n"
"<p align=\"center\" style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">* ArcoLinux GitHub: <a href=\"https://github.com/arcolinux\"><span style=\" text-decoration: underline; color:#00aaff;\">https://github.com/arcolinux</span></a></p>\n"
"<p align=\"center\" style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">* ArcoLinuxB  GitHub: <a href=\"https://github.com/arcolinuxb\"><span style=\" text-decoration: underline; color:#00aaff;\">https://github.com/arcolinuxb</span></a></p>\n"
"<p align=\"center\" style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">* Website: <a href=\"https://arcolinux.com\"><span style=\" text-decoration: underline; color:#00aaff;\">https://arcolinux.com</span></a></p></body></html>")

        self.label_about.setOpenExternalLinks(True)
        self.label_about.setTextInteractionFlags(Qt.LinksAccessibleByMouse)
        self.about_dialog.setModal(True)
        self.about_dialog.exec_()

    # When a user selects an ISO name from the combo-box, update the ISO description with it
    def update_ISO_Desc(self):
        self.plainTextEdit_ISO_Desc.clear()
        selected_iso_name = str(self.comboBox_ISO.currentText())
        found = False

        for x in ArcoMetadata.metadata:
            if x == selected_iso_name:
                found = True

                description = ArcoMetadata.metadata[x]

                for d in description:
                    if "GitHub Repository = " in d:

                        self.label_iso_github.setText('<a href="%s">%s</a>' %(d.replace("GitHub Repository =","").strip(),d.replace("GitHub Repository =","").strip()))

                        self.label_iso_github.setOpenExternalLinks(True)
                        self.label_iso_github.setTextInteractionFlags(Qt.LinksAccessibleByMouse)

                    else:
                        self.plainTextEdit_ISO_Desc.appendPlainText(" - %s"%d)

                break


        if found == False:

            arcolinuxb_iso_desc = ArcoMetadata.metadata['arcolinuxb-iso']

            for d in arcolinuxb_iso_desc:
                print("desc = %s" %d)
                if "GitHub Repository = " in d:
                    self.label_iso_github.setText('<a href="%s">%s</a>' %(d.replace("GitHub Repository =","").strip()+"/"+selected_iso_name,d.replace("GitHub Repository =","").strip()+"/"+selected_iso_name))

                    self.label_iso_github.setOpenExternalLinks(True)
                    self.label_iso_github.setTextInteractionFlags(Qt.LinksAccessibleByMouse)

                else:
                    self.plainTextEdit_ISO_Desc.appendPlainText(" - %s"%d)

    # Export package list, using the cached contents and save to disk
    def export_package_list(self,arcolinux_iso_dict):
        selected_iso_name = str(self.comboBox_ISO.currentText())

        md5_hash = hashlib.md5(selected_iso_name.encode('utf-8')).hexdigest()

        cache_file = self.settings.cache_path + "/" + md5_hash

        if len(cache_file) > 0:

            with open(cache_file, mode="rb") as f:
                cached_content = tomli.load(f)

            if cached_content['content'] is not None:

                filename = str(pathlib.Path.home()) + "/" + selected_iso_name + "-" + datetime.datetime.now().strftime("%Y%m%d")+"-packages.x86_64.txt"

                pkg_txt_save_filename = QFileDialog.getSaveFileName(self,
                                                str("Save packages.x86_64 file"), filename,str("TXT Files (*.txt)"))

                if len(pkg_txt_save_filename[0]) > 0:

                    with open(pkg_txt_save_filename[0], mode="w") as f:
                        f.write("#####################################################################\n")
                        f.write("# Generated by ArcoLinux ISO Downloader on: %s\n" % datetime.datetime.now().strftime("%Y-%m-%d"))
                        f.write("# ISO: %s\n" % selected_iso_name)
                        f.write("# Source: %s\n" % self.arcolinux_iso_dict[selected_iso_name])
                        f.write("#####################################################################\n")
                        f.write(cached_content['content']+"\n")

                    if os.path.exists(pkg_txt_save_filename[0]):
                        self.statusbar.setStyleSheet("font-weight: bold")
                        self.statusbar.showMessage(str("Package Export Completed"),5000)
                    else:
                        self.statusbar.setStyleSheet("font-weight: bold")
                        self.statusbar.showMessage(str("Package Export Failed"),5000)
        else:
            self.statusbar.setStyleSheet("font-weight: bold")
            self.statusbar.showMessage(str("Package Export Failed"),5000)

    # Generate a dict which stores the associated github raw package list url for each ISO
    def get_arcolinux_iso_dict(self):
        arcolinux_iso_dict = {}
        for arcolinux_iso in self.settings.arcolinux:

            arcolinux_iso_dict[arcolinux_iso] = RAW_PACKAGE_LIST_ARCOLINUX.replace("${ISO}",arcolinux_iso)

        for arcolinuxb_iso in self.settings.arcolinuxb:
            arcolinux_iso_dict[arcolinuxb_iso] = RAW_PACKAGE_LIST_ARCOLINUXB.replace("${ISO}",arcolinuxb_iso)


        return arcolinux_iso_dict

    # Update the package list view on the form
    def update_pkg_list_view(self,arcolinux_iso_dict):
        print("[User] Selected ISO = %s" % self.comboBox_ISO.currentText())
        self.listWidget_pkglist.clear()

        packages = self.get_package_list(arcolinux_iso_dict)

        if len(packages) > 0:
            self.pushButton_exportPkgList.setDisabled(False)
            self.actionSearch_remote_pkg.setDisabled(False)
            self.pushButton_download_ISO.setDisabled(False)
            self.label_iso_pkgcount.setText(str("Package Count: %s" % len(packages)))

            row = 0
            for pkg in packages:
                self.listWidgetItem = QListWidgetItem()
                self.listWidgetItem.setText(str(pkg))
                self.listWidget_pkglist.insertItem(row,self.listWidgetItem)
                row+=1
        else:
            self.listWidgetItem = QListWidgetItem()
            self.listWidgetItem.setText("Error fetching packages.\nGitHub repository doesn't exist or no internet connection.")
            self.listWidget_pkglist.insertItem(0,self.listWidgetItem)
            self.pushButton_download_ISO.setDisabled(True)
            self.pushButton_exportPkgList.setDisabled(True)
            self.actionSearch_remote_pkg.setDisabled(True)
            self.label_iso_pkgcount.setText("Package Count: 0")

    # Display the download ISO dialog box
    def display_download_dialog(self):
        self.download_dialog = QDialog(self)
        self.download_dialog.setWindowTitle("Download ISO")
        self.download_dialog.setFixedSize(438, 283)
        self.download_dialog.setModal(True)

        self.label_download_ISO = QtWidgets.QLabel(self.download_dialog)
        self.label_download_ISO.setGeometry(QtCore.QRect(20, 60, 71, 17))
        self.label_download_ISO.setObjectName("label_download_ISO")
        self.label_download_ISO.setText("Version:")

        self.comboBox_download_ISO = QtWidgets.QComboBox(self.download_dialog)
        self.comboBox_download_ISO.setGeometry(QtCore.QRect(80, 50, 321, 39))
        self.comboBox_download_ISO.setObjectName("comboBox_download_ISO")

        self.populate_download_comboBox(self.comboBox_ISO.currentText())

        self.label_dialog_download_size = QtWidgets.QLabel(self.download_dialog)
        self.label_dialog_download_size.setGeometry(QtCore.QRect(20, 100, 381, 17))
        self.label_dialog_download_size.setObjectName("label_dialog_download_size")
        self.label_dialog_download_size.setVisible(True)

        self.label_download_provider = QtWidgets.QLabel(self.download_dialog)
        self.label_download_provider.setGeometry(QtCore.QRect(20, 20, 121, 17))
        self.label_download_provider.setObjectName("label_download_Provider")
        self.label_download_provider.setText("Download Provider:")

        self.label_download_Provider_update = QtWidgets.QLabel(self.download_dialog)
        self.label_download_Provider_update.setGeometry(QtCore.QRect(140, 20, 251, 17))
        self.label_download_Provider_update.setObjectName("label_download_Provider_update")
        self.label_download_Provider_update.setText(self.settings.provider['name'] + " | " + "Mirror = %s" % self.settings.mirror)


        self.label_dialog_publish = QtWidgets.QLabel(self.download_dialog)
        self.label_dialog_publish.setGeometry(QtCore.QRect(20, 140, 371, 17))
        self.label_dialog_publish.setObjectName("label_dialog_publish")
        self.label_dialog_publish.setVisible(False)
        self.label_dialog_publish.setText("Published:")

        self.buttonBox_dialog_download = QtWidgets.QDialogButtonBox(self.download_dialog)
        self.buttonBox_dialog_download.setGeometry(QtCore.QRect(10, 170, 200, 39))

        self.pushButton_dialog_download_ok = QPushButton(self)
        self.pushButton_dialog_download_ok.setGeometry(QRect(330, 480, 151, 39))
        self.pushButton_dialog_download_ok.setText("Download")
        self.pushButton_dialog_download_ok.setIcon(QtGui.QIcon(":/app_images/images/download.png"))

        self.pushButton_dialog_download_cancel = QPushButton(self)
        self.pushButton_dialog_download_cancel.setText("Cancel")
        self.pushButton_dialog_download_cancel.setIcon(QtGui.QIcon(":/app_images/images/cancel.png"))



        self.buttonBox_dialog_download.addButton(self.pushButton_dialog_download_ok,QDialogButtonBox.AcceptRole)
        self.buttonBox_dialog_download.addButton(self.pushButton_dialog_download_cancel,QDialogButtonBox.RejectRole)

        self.buttonBox_dialog_download.setObjectName("buttonBox_dialog_download")
        self.buttonBox_dialog_download.rejected.connect(self.download_cancel)
        self.buttonBox_dialog_download.accepted.connect(lambda: self.save_iso_disk())


        self.progressBar = QtWidgets.QProgressBar(self.download_dialog)
        self.progressBar.setGeometry(QtCore.QRect(10, 220, 421, 23))
        self.progressBar.setObjectName("progressBar")
        self.progressBar.setValue(0)
        self.progressBar.setVisible(False)

        self.label_dialog_download_status = QtWidgets.QLabel(self.download_dialog)
        self.label_dialog_download_status.setGeometry(QtCore.QRect(20, 250, 341, 17))
        self.label_dialog_download_status.setObjectName("label_dialog_download_status")

        self.label_dialog_download_status.setVisible(False)

        self.comboBox_download_ISO.currentTextChanged.connect(lambda:self.update_download_dialog_labels())

        QtCore.QMetaObject.connectSlotsByName(self.download_dialog)

        self.download_dialog.setWindowFlags(Qt.Dialog)

        if self.comboBox_download_ISO.currentData() != None:

            self.label_dialog_publish.setVisible(True)
            self.label_dialog_download_size.setText("Filesize:        %s" % self.comboBox_download_ISO.currentData().filesize)
            self.label_dialog_publish.setText("Published:   %s" % self.comboBox_download_ISO.currentData().pub_date.strip())
        else:
            self.pushButton_dialog_download_ok.setEnabled(False)


        self.download_dialog.exec_()

        self.download_cancel()

    # Attached to cancel button on the download ISO dialog box,
    # sends interrupt to download thread if download is currently in progress
    def download_cancel(self):
        # interrupt download thread if user clicks cancel
        print("[Thread-Main] Download canceled")
        try:
            if hasattr(self,'downloader_iso_t'):
                print("[DownloaderThread] Requesting ISO download interruption")
                self.download_binary_in_progress().requestInterruption()
                self.download_dialog.close()
                self.show()
            elif hasattr(self,'downloader_iso_sha256_t'):
                print("[DownloaderThread] Requesting sha256 download interruption")
                self.download_sha256_in_progress().requestInterruption()
                self.download_dialog.close()
                self.show()
            else:
                self.download_dialog.close()
                self.show()
        except Exception:
            print(traceback.format_exc())
            sys.exit(1)


    # Update the labels on the download dialog box, filesize, publish date
    def update_download_dialog_labels(self):
        if self.comboBox_download_ISO.currentData() != None:
            self.label_dialog_download_size.setVisible(True)
            self.label_dialog_download_size.setText("Filesize:        %s" % self.comboBox_download_ISO.currentData().filesize)
            self.label_dialog_publish.setVisible(True)
            self.label_dialog_publish.setText("Published:   %s" % self.comboBox_download_ISO.currentData().pub_date)

    # Prompt user for the filename to save the ISO to disk
    # Run download thread, start download of ISO, update progress bar, and update file download status
    def save_iso_disk(self):

        if str(self.comboBox_download_ISO.currentText()) != "No ISO's found":
            iso_filename = self.comboBox_download_ISO.currentText()

            iso_save_filename = QFileDialog.getSaveFileName(self,
    str("Save ISO file"), str(pathlib.Path.home())+"/"+iso_filename, str("ISO Files (*.iso)"))

        if len(iso_save_filename[0]) > 0:
            self.iso_filename = iso_save_filename[0]
            self.download_iso = False
            self.download_sha256 = False
            self.inProgress = False
            self.size = 0
            self.dest_dir = os.path.dirname(self.iso_filename)

            self.selected_iso = self.comboBox_download_ISO.currentData()
            self.pushButton_dialog_download_ok.setEnabled(False)
            self.comboBox_download_ISO.setEnabled(False)

            self.progressBar.setVisible(True)
            self.label_dialog_download_status.setVisible(False)

            # Save the main iso file

            self.downloader_iso_t = DownloadThread(self.selected_iso.link,self.iso_filename,"application/x-iso9660-image")
            self.downloader_iso_t.name = "ArcoLinuxSaveISO_Thread"

            self.downloader_iso_t.setTotalProgress.connect(self.bytes_total)
            self.downloader_iso_t.setTotalProgress.connect(self.progressBar.setMaximum)
            self.downloader_iso_t.setCurrentProgress.connect(self.bytes_recv)
            self.downloader_iso_t.setCurrentProgress.connect(self.progressBar.setValue)

            self.downloader_iso_t.inProgress.connect(self.download_binary_in_progress)
            self.downloader_iso_t.succeeded.connect(self.download_binary_success)

            print("[DownloadThread] Starting ISO download thread")
            print("[Filename] %s" % self.iso_filename)

            self.downloader_iso_t.start()


            #print("inProgress - iso download: %s" % int(self.downloader_iso_t.currentProgress))


            # Save the sha25 file
            self.iso_sha256_filename = self.dest_dir+"/"+self.selected_iso.sha256_name
            self.downloader_iso_sha256_t = DownloadThread(self.selected_iso.sha256_link,self.iso_sha256_filename,"text/html")
            self.downloader_iso_sha256_t.name = "ArcoLinuxSaveISO_sha256_Thread"
            self.downloader_iso_sha256_t.inProgress.connect(self.download_sha256_in_progress)

            self.downloader_iso_sha256_t.succeeded.connect(self.download_sha256_success)

            print("[DownloadThread] Starting ISO sha256 download thread")
            print("[Filename] %s" % self.iso_sha256_filename)


            self.downloader_iso_sha256_t.start()

            #self.pushButton_dialog_download_ok.setEnabled(True)

    # pyqtSlot all signals used for the download thread
    @pyqtSlot(int)
    def bytes_total(self,bytes_t):
        self.size = ISO.get_readable_file_size(bytes_t*10)

    @pyqtSlot(int)
    def bytes_recv(self,bytes_r):
        self.label_dialog_download_status.setVisible(True)
        self.label_dialog_download_status.setText(str(ISO.get_readable_file_size(bytes_r*10)) + "/%s" % self.size)

    @pyqtSlot(bool)
    def download_binary_in_progress(self):
        self.download_iso = False
        if hasattr(self,'downloader_iso_t'):
            return self.downloader_iso_t

    @pyqtSlot(bool)
    def download_sha256_in_progress(self):
        self.download_sha256 = False
        if hasattr(self,'downloader_iso_sha256_t'):
            return self.downloader_iso_sha256_t

    @pyqtSlot()
    def download_sha256_success(self):
        self.download_sha256 = True
        if hasattr(self,'downloader_iso_sha256_t'):
            print("[DownloaderThread] sha256 file downloaded")
            self.destroy_download_sha256_thread()

    @pyqtSlot()
    def download_binary_success(self):
        self.download_iso = True
    # Set the progress at 100%.
        print("[DownloaderThread] ISO file downloaded")

        if hasattr(self,'downloader_iso_t'):
            self.progressBar.setValue(self.progressBar.maximum())
            self.comboBox_download_ISO.setEnabled(True)

            self.pushButton_dialog_download_ok.setEnabled(True)
            self.destroy_download_binary_thread()

    # Destroy the local pkg thread
    def destroy_local_pkg_thread(self):
        if hasattr(self,'local_pkg_t'):
            print("[PackageThread] Delete PackageThread thread")
            del self.local_pkg_t

    # Destroy the sha256 download thread
    def destroy_download_sha256_thread(self):
        if hasattr(self,'downloader_iso_sha256_t'):
            print("[DownloaderThread] Delete ISO sha256 download thread")
            del self.downloader_iso_sha256_t

    # Destroy the ISO download thread
    def destroy_download_binary_thread(self):
        # Restore the button.
        # Delete the thread when no longer needed.
        if hasattr(self,'downloader_iso_t'):
            print("[DownloaderThread] Delete ISO download thread")
            del self.downloader_iso_t


        if self.download_sha256 == True \
            and self.download_iso == True \
            and os.path.exists(self.iso_filename) \
            and os.path.exists(self.iso_sha256_filename):
            print("[ValidateThread] Starting thread")
            self.validate_iso_t = ValidateThread(self.iso_filename, self.iso_sha256_filename)
            self.validate_iso_t.start()
            self.validate_iso_t.join()

            if self.validate_iso_t.is_download_ok:
                self.label_dialog_download_status.setVisible(True)
                self.label_dialog_download_status.setText("sha256 validation completed, download = OK")
            else:
                self.label_dialog_download_status.setVisible(True)
                self.label_dialog_download_status.setText("Error: ISO file download failed, sha256 validation error")
        else:
            self.label_dialog_download_status.setVisible(True)
            self.label_dialog_download_status.setText("Error: ISO file download failed, sha256 validation error")
            self.progressBar.setValue(0)

        if hasattr(self,'validate_iso_t'):
            print("[ValidateThread] Delete Validate ISO thread")
            del self.validate_iso_t


    # Destroy the package list download thread
    def destroy_download_pkg_thread(self):
        print("[ResponseThread] Delete text/plain thread")
        if hasattr(self,'downloader_pkg_t'):
            del self.downloader_pkg_t

    # Spawn a new response thread to request an ISO package list
    def get_package_list(self,arcolinux_iso_dict):
        self.downloader_pkg_t = ResponseThread(arcolinux_iso_dict[self.comboBox_ISO.currentText()],"text/plain",self.comboBox_ISO.currentText(), self.settings.cache_path)

        print("[ResponseThread] Starting thread")
        self.downloader_pkg_t.start()
        self.downloader_pkg_t.join()

        packages = []

        if self.downloader_pkg_t.content is not None:
            self.listWidget_pkglist.clear()
            for line in self.downloader_pkg_t.content.splitlines():

                if len(line) > 0 and line[0] != '#':
                    packages.append(line.strip())


        self.destroy_download_pkg_thread()
        return packages[::-1]

    # Adds ISO filenames into the download ISO combo-box, taken from SourceForge
    def populate_download_comboBox(self,selected_iso_name):
        if len(selected_iso_name) > 0:
            if selected_iso_name in self.settings.arcolinux:
                if self.settings.provider['name'].lower() == "sourceforge":
                    provider = Sourceforge(self.settings)
                    iso_list = provider.get_ISO("arcolinux-iso",selected_iso_name)

                    if len(iso_list) > 0:
                        self.comboBox_download_ISO.setDisabled(False)
                        for iso in iso_list:
                            self.comboBox_download_ISO.addItem(iso.name,userData=iso)
                    else:
                        self.comboBox_download_ISO.addItem("No ISO's found")
                        self.comboBox_download_ISO.setDisabled(True)

            elif selected_iso_name in self.settings.arcolinuxb:
                if self.settings.provider['name'].lower() == "sourceforge":
                    provider = Sourceforge(self.settings)
                    iso_list = provider.get_ISO("arcolinuxb-iso",selected_iso_name)

                    if len(iso_list) > 0:
                        self.comboBox_download_ISO.setDisabled(False)
                        for iso in iso_list:
                            self.comboBox_download_ISO.addItem(iso.name,userData=iso)
                    else:
                        self.comboBox_download_ISO.addItem("No ISO's found")
                        self.comboBox_download_ISO.setDisabled(True)
        else:
            self.comboBox_download_ISO.setDisabled(True)
