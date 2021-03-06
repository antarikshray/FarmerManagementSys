# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'first.ui'
#
# Created by: PyQt5 UI code generator 5.15.0
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets
import sqlite3
import uuid



cropCheckBox=[]

class CropMain():
    def __init__(self, ind):
        self.index=ind
    
    def checkboxUpdate(self, state):
        cropCheckBox[self.index]=state

class Ui_Dialog(object):

    def MainTableLoad(self):
        con = sqlite3.connect('FarmerDB.db')
        query="select FarmerDetails.FID, FarmerDetails.FNAME, FarmerDetails.CONTACT, CropDetails.CNAME, CropDetails.SEASON, FarmerCrop.PLOTDATE, FarmerCrop.HARVESTDATE, LandDetails.LANDNAME, LandDetails.ADDRESS from FarmerDetails, CropDetails, FarmerCrop, LandDetails where FarmerDetails.FID=FarmerCrop.FID AND CropDetails.CID=FarmerCrop.CID AND LandDetails.FID=FarmerCrop.FID ORDER BY FarmerCrop.FID"
        result = con.execute(query)
        self.MainFarmerTable.setRowCount(0)
        for row_number, row_data in enumerate(result):
            self.MainFarmerTable.insertRow(row_number)
            for column_number, data in enumerate(row_data):
                self.MainFarmerTable.setItem(row_number, column_number, QtWidgets.QTableWidgetItem(str(data)))
        con.close()


    def FarmerLoad(self):
        con = sqlite3.connect('FarmerDB.db')
        query="select * from FarmerDetails"
        self.all_farmers=[]
        for row in con.execute(query):
            self.all_farmers.append(row)
        con.close()


    def CropsLoad(self):
        con = sqlite3.connect('FarmerDB.db')
        query="select * from CropDetails"
        self.all_crops=[]
        for row in con.execute(query):
            self.all_crops.append(row)
            cropCheckBox.append(0)
        con.close()

    def LandLoad(self):
        con = sqlite3.connect('FarmerDB.db')
        query="select * from landDetails"
        self.all_plots=[]
        for row in con.execute(query):
            self.all_plots.append(row)
        con.close()

    def FarmerRegistration(self):
        con = sqlite3.connect('FarmerDB.db')
        cur = con.cursor()
        self.FarmerLoad()
        self.farmerId=len(self.all_farmers)+1
        cur.execute('insert into FarmerDetails values(?, ?, ?, ?)',(self.farmerId,str(self.farmer_name.toPlainText()), str(self.farmer_dob.toPlainText()), int(self.farmer_contact.toPlainText())))
        cropUpdate=[]
        for i, cropState in enumerate(cropCheckBox):
            if(cropState==2):
                cropUpdate.append((int(self.farmerId), i+1, '2021-04-10', '2021-08-15'))        
        print(cropUpdate)
        cur.executemany('insert into FarmerCrop values (?, ?, ?, ?)', cropUpdate)
        con.commit()
        con.close()
        self.MainTableLoad()

    def Landregistration(self):
        con = sqlite3.connect('FarmerDB.db')
        cur = con.cursor()
        self.plotId=len(self.all_plots)+1
        cur.execute('insert into LandDetails values(?, ?, ?, ?, ?)',(self.plotId,str(self.plot_name.toPlainText()), self.farmerId, str(self.plotable_crops.toPlainText()), str(self.plot_address.toPlainText())))
        con.commit()
        con.close()
        self.MainTableLoad()

    def CropsCheckboxLoader(self):
        self.CropsLoad()
        self.crop = []
        self.checkCrop = []
        for i, cropDetail in enumerate(self.all_crops): 
            self.crop.append(QtWidgets.QCheckBox(self.verticalLayoutWidget_2))
            self.crop[i].setText(str(cropDetail[1]))
            self.crop[i].setObjectName("crop_"+str(i))
            self.checkCrop.append(CropMain(i))
            self.crop[i].stateChanged.connect(self.checkCrop[i].checkboxUpdate)
            self.verticalLayout_2.addWidget(self.crop[i])

    def CropsCheckboxAdder(self):
        self.CropsLoad()
        self.crop.append(QtWidgets.QCheckBox(self.verticalLayoutWidget_2))
        curr_ind=len(self.all_crops)-1
        self.crop[curr_ind].setText(str(self.all_crops[curr_ind][1]))
        self.crop[curr_ind].setObjectName("crop_"+str(curr_ind))
        self.checkCrop.append(CropMain(curr_ind))
        self.crop[curr_ind].stateChanged.connect(self.checkCrop[curr_ind].checkboxUpdate)
        self.verticalLayout_2.addWidget(self.crop[curr_ind])

    def CropRegistration(self):
        con = sqlite3.connect('FarmerDB.db')
        cur = con.cursor()
        self.cropId=len(self.all_crops)+1
        cur.execute('insert into CropDetails values(?, ?, ?)',(self.cropId,str(self.crop_name.toPlainText()), str(self.crop_season.toPlainText())))
        con.commit()
        con.close()
        self.CropsCheckboxAdder()

    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(1394, 899)

        #main farmer table
        self.MainFarmerTable = QtWidgets.QTableWidget(Dialog)
        self.MainFarmerTable.setGeometry(QtCore.QRect(25, 21, 1201, 381))
        self.MainFarmerTable.setRowCount(5)
        self.MainFarmerTable.setColumnCount(9)
        self.MainFarmerTable.setObjectName("MainFarmerTable")
        self.MainTableLoad()


        #farmer registration
        self.verticalLayoutWidget = QtWidgets.QWidget(Dialog)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(20, 430, 431, 201))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        self.farmer_name = QtWidgets.QTextEdit(self.verticalLayoutWidget)
        self.farmer_name.setObjectName("farmer_name")
        self.gridLayout.addWidget(self.farmer_name, 1, 1, 1, 1)
        self.label = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 1, 0, 1, 1)
        self.farmer_dob = QtWidgets.QTextEdit(self.verticalLayoutWidget)
        self.farmer_dob.setObjectName("farmer_dob")
        self.gridLayout.addWidget(self.farmer_dob, 2, 1, 1, 1)
        self.label_4 = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.label_4.setAlignment(QtCore.Qt.AlignCenter)
        self.label_4.setObjectName("label_4")
        self.gridLayout.addWidget(self.label_4, 3, 0, 1, 1)
        self.farmer_contact = QtWidgets.QTextEdit(self.verticalLayoutWidget)
        self.farmer_contact.setObjectName("farmer_contact")
        self.gridLayout.addWidget(self.farmer_contact, 3, 1, 1, 1)

        self.farmer_register_b = QtWidgets.QPushButton(Dialog)
        self.farmer_register_b.setGeometry(QtCore.QRect(360, 640, 89, 25))
        self.farmer_register_b.setObjectName("farmer_register_b")
        self.farmer_register_b.clicked.connect(self.FarmerRegistration)


        #crops check box
        self.label_2 = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.label_2.setAlignment(QtCore.Qt.AlignCenter)
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 2, 0, 1, 1)
        self.label_3 = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.label_3.setAlignment(QtCore.Qt.AlignCenter)
        self.label_3.setObjectName("label_3")
        self.gridLayout.addWidget(self.label_3, 0, 0, 1, 2)
        self.verticalLayout.addLayout(self.gridLayout)
        self.verticalLayoutWidget_2 = QtWidgets.QWidget(Dialog)
        self.verticalLayoutWidget_2.setGeometry(QtCore.QRect(490, 430, 161, 401))
        self.verticalLayoutWidget_2.setObjectName("verticalLayoutWidget_2")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.verticalLayoutWidget_2)
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.CropsCheckboxLoader()

        
        #Plot Details
        self.verticalLayoutWidget_3 = QtWidgets.QWidget(Dialog)
        self.verticalLayoutWidget_3.setGeometry(QtCore.QRect(20, 670, 431, 181))
        self.verticalLayoutWidget_3.setObjectName("verticalLayoutWidget_3")
        self.verticalLayout_4 = QtWidgets.QVBoxLayout(self.verticalLayoutWidget_3)
        self.verticalLayout_4.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.gridLayout_3 = QtWidgets.QGridLayout()
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.plotable_crops = QtWidgets.QTextEdit(self.verticalLayoutWidget_3)
        self.plotable_crops.setObjectName("plotable_crops")
        self.gridLayout_3.addWidget(self.plotable_crops, 2, 1, 1, 1)
        self.plot_name = QtWidgets.QTextEdit(self.verticalLayoutWidget_3)
        self.plot_name.setObjectName("plot_name")
        self.gridLayout_3.addWidget(self.plot_name, 1, 1, 1, 1)
        self.label_11 = QtWidgets.QLabel(self.verticalLayoutWidget_3)
        self.label_11.setAlignment(QtCore.Qt.AlignCenter)
        self.label_11.setObjectName("label_11")
        self.gridLayout_3.addWidget(self.label_11, 2, 0, 1, 1)
        self.label_9 = QtWidgets.QLabel(self.verticalLayoutWidget_3)
        self.label_9.setAlignment(QtCore.Qt.AlignCenter)
        self.label_9.setObjectName("label_9")
        self.gridLayout_3.addWidget(self.label_9, 1, 0, 1, 1)
        self.label_10 = QtWidgets.QLabel(self.verticalLayoutWidget_3)
        self.label_10.setAlignment(QtCore.Qt.AlignCenter)
        self.label_10.setObjectName("label_10")
        self.gridLayout_3.addWidget(self.label_10, 3, 0, 1, 1)
        self.plot_address = QtWidgets.QTextEdit(self.verticalLayoutWidget_3)
        self.plot_address.setObjectName("plot_address")
        self.gridLayout_3.addWidget(self.plot_address, 3, 1, 1, 1)
        self.label_12 = QtWidgets.QLabel(self.verticalLayoutWidget_3)
        self.label_12.setAlignment(QtCore.Qt.AlignCenter)
        self.label_12.setObjectName("label_12")
        self.gridLayout_3.addWidget(self.label_12, 0, 0, 1, 2)
        self.verticalLayout_4.addLayout(self.gridLayout_3)

        self.LandLoad()
        self.land_confirm_b = QtWidgets.QPushButton(Dialog)
        self.land_confirm_b.setGeometry(QtCore.QRect(360, 870, 89, 25))
        self.land_confirm_b.setObjectName("land_confirm_b")
        self.land_confirm_b.clicked.connect(self.Landregistration)


        #crop register form
        self.formLayoutWidget = QtWidgets.QWidget(Dialog)
        self.formLayoutWidget.setGeometry(QtCore.QRect(700, 560, 291, 91))
        self.formLayoutWidget.setObjectName("formLayoutWidget")
        self.formLayout = QtWidgets.QFormLayout(self.formLayoutWidget)
        self.formLayout.setContentsMargins(0, 0, 0, 0)
        self.formLayout.setObjectName("formLayout")
        self.label_13 = QtWidgets.QLabel(self.formLayoutWidget)
        self.label_13.setAlignment(QtCore.Qt.AlignCenter)
        self.label_13.setObjectName("label_13")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.label_13)
        self.label_14 = QtWidgets.QLabel(self.formLayoutWidget)
        self.label_14.setAlignment(QtCore.Qt.AlignCenter)
        self.label_14.setObjectName("label_14")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.label_14)
        self.crop_name = QtWidgets.QPlainTextEdit(self.formLayoutWidget)
        self.crop_name.setObjectName("crop_name")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.crop_name)
        self.crop_season = QtWidgets.QPlainTextEdit(self.formLayoutWidget)
        self.crop_season.setObjectName("crop_season")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.crop_season)
        self.label_15 = QtWidgets.QLabel(Dialog)
        self.label_15.setGeometry(QtCore.QRect(700, 530, 141, 17))
        self.label_15.setObjectName("label_15")

        self.crop_register_b = QtWidgets.QPushButton(Dialog)
        self.crop_register_b.setGeometry(QtCore.QRect(900, 660, 89, 25))
        self.crop_register_b.setObjectName("crop_register_b")
        self.crop_register_b.clicked.connect(self.CropRegistration)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.label.setText(_translate("Dialog", "Farmer\'s Name"))
        self.label_4.setText(_translate("Dialog", "Contact"))
        self.label_2.setText(_translate("Dialog", "Date Of Birth"))
        self.label_3.setText(_translate("Dialog", "Farmer Registration"))
        self.farmer_register_b.setText(_translate("Dialog", "Register"))
        self.label_11.setText(_translate("Dialog", "Plotable Crops"))
        self.label_9.setText(_translate("Dialog", "Plot name"))
        self.label_10.setText(_translate("Dialog", "Address"))
        self.label_12.setText(_translate("Dialog", "Land Registration"))
        self.land_confirm_b.setText(_translate("Dialog", "Confirm"))
        self.label_13.setText(_translate("Dialog", "CROP NAME"))
        self.label_14.setText(_translate("Dialog", "SEASON"))
        self.label_15.setText(_translate("Dialog", "Crop Registration"))
        self.crop_register_b.setText(_translate("Dialog", "Register"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Dialog = QtWidgets.QDialog()
    ui = Ui_Dialog()
    ui.setupUi(Dialog)
    Dialog.show()
    sys.exit(app.exec_())
