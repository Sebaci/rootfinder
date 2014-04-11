# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'design.ui'
#
# Created: Mon Feb 10 17:36:12 2014
#      by: PyQt4 UI code generator 4.10.3
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui
import shelve
import rootfinder

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName(_fromUtf8("MainWindow"))
        MainWindow.resize(791, 569)
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.polysLabel = QtGui.QLabel(self.centralwidget)
        self.polysLabel.setGeometry(QtCore.QRect(10, 10, 91, 17))
        self.polysLabel.setObjectName(_fromUtf8("polysLabel"))
        self.polyList = QtGui.QListWidget(self.centralwidget)
        self.polyList.setGeometry(QtCore.QRect(10, 30, 251, 221))
        self.polyList.setObjectName(_fromUtf8("polyList"))
        self.newPolyBtn = QtGui.QPushButton(self.centralwidget)
        self.newPolyBtn.setGeometry(QtCore.QRect(10, 260, 121, 27))
        self.newPolyBtn.setObjectName(_fromUtf8("newPolyBtn"))
        self.remPolyBtn = QtGui.QPushButton(self.centralwidget)
        self.remPolyBtn.setEnabled(True)
        self.remPolyBtn.setGeometry(QtCore.QRect(140, 260, 121, 27))
        self.remPolyBtn.setObjectName(_fromUtf8("remPolyBtn"))
        self.rootList = QtGui.QListWidget(self.centralwidget)
        self.rootList.setGeometry(QtCore.QRect(10, 330, 251, 201))
        self.rootList.setObjectName(_fromUtf8("listWidget"))
        self.rootsLabel = QtGui.QLabel(self.centralwidget)
        self.rootsLabel.setGeometry(QtCore.QRect(10, 310, 121, 17))
        self.rootsLabel.setObjectName(_fromUtf8("rootsLabel"))
        self.graphicsView = QtGui.QGraphicsView(self.centralwidget)
        self.graphicsView.setGeometry(QtCore.QRect(280, 30, 500, 500))
        self.graphicsView.setObjectName(_fromUtf8("graphicsView"))
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 791, 25))
        self.menubar.setObjectName(_fromUtf8("menubar"))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtGui.QStatusBar(MainWindow)
        self.statusbar.setObjectName(_fromUtf8("statusbar"))
        MainWindow.setStatusBar(self.statusbar)
        self.polysLabel.setBuddy(self.polyList)
        self.rootsLabel.setBuddy(self.rootList)

        self.retranslateUi(MainWindow)
        QtCore.QObject.connect(self.remPolyBtn, QtCore.SIGNAL(_fromUtf8("clicked()")), self.removePoly)
        QtCore.QObject.connect(self.newPolyBtn, QtCore.SIGNAL(_fromUtf8("clicked()")), self.openPolyDialog)
        QtCore.QObject.connect(self.polyList, QtCore.SIGNAL(_fromUtf8("itemClicked(QListWidgetItem*)")), self.polySelected)
        QtCore.QObject.connect(self.rootList, QtCore.SIGNAL(_fromUtf8("itemClicked(QListWidgetItem*)")), self.rootSelected)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
        
        self.plot = QtGui.QGraphicsScene()
        self.plot.setSceneRect(1, 1, 498, 498)
        self.graphicsView.setScene(self.plot)
        
        self.maxCoord = -1.0
        self.scale = 0.0
        self.lastPolySelect = -1
        self.lastRootSelect = 0    
        
        self.window = MainWindow
        self.numSup = ['⁰', '¹', '²', '³', '⁴', '⁵', '⁶', '⁷', '⁸', '⁹',
            '¹⁰', '¹¹', '¹²', '¹³', '¹⁴', '¹⁵', '¹⁶', '¹⁷', '¹⁸', '¹⁹']
        
        self.polynomials = []
        
        dbsucc = False
        db = shelve.open('data.db')
        
        if db:
          dbsucc = True
          self.polynomials = db['polynomials']
          self.maxCoord = db['maxCoord']
          self.scale = db['scale']
        db.close()
        
        self.drawAxis()
        
        for i in range(0, len(self.polynomials)):
          self.polyList.addItem("w"+str(i+1)+"(z)="+self.polynomials[i][0])
        
        if dbsucc: self.drawAllRoots()
        
    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(_translate("MainWindow", "Rootfinder", None))
        self.polysLabel.setText(_translate("MainWindow", "Polynomials", None))
        __sortingEnabled = self.polyList.isSortingEnabled()
        self.polyList.setSortingEnabled(False)
        self.polyList.setSortingEnabled(__sortingEnabled)
        self.newPolyBtn.setText(_translate("MainWindow", "New polynomial", None))
        self.remPolyBtn.setText(_translate("MainWindow", "Remove", None))
        self.rootsLabel.setText(_translate("MainWindow", "Polynomial roots", None))
        
    def openPolyDialog(self):
      self.newPolyDialog = QtGui.QDialog(self.window)
      self.ui = Ui_newPolyDialog()
      self.ui.setupUi(self.newPolyDialog)
      self.newPolyDialog.show()
      QtCore.QObject.connect(self.ui.addPolyBtn, QtCore.SIGNAL(_fromUtf8("clicked()")), self.getData)
      
    def getData(self):
        coef = []
        for i in reversed(range(0,10)):
            control = self.newPolyDialog.findChild(QtGui.QLineEdit, "a"+str(i))
            coef.append(str(control.text()))
        
        self.newPolyDialog.close()
        self.addPolynomial(coef)
        
    def addPolynomial(self, coef):
        polyStr = ''
        
        for i in range(0, 10):
            if coef[i] == '0': continue
            
            if polyStr != '':
                if coef[i][0] != '-': polyStr += '+'
            polyStr += coef[i]
            
            if i != 9:
                polyStr += ("z"+_translate("MainWindow", self.numSup[9-i], None))
            
        fcoef = [float(a) for a in coef]
        rf = rootfinder.Rootfinder(fcoef)
        rf.findRoots()
        
        
        self.polynomials.append([polyStr, rf.roots])
        
        k = len(self.polynomials)
        self.drawRoots(k-1, True);
        
        # save data
        self.saveData()
        
        self.polyList.addItem("w"+str(k)+"(z)="+polyStr)
    
    def polySelected(self):
        self.clearRootList()
        self.lastRootSelect = 0
    
        i = self.polyList.currentRow()
        roots = self.polynomials[i][1]
        
        for k in range(0, len(roots)):
            s = "z"+str(k)+"="
            real = str(round(roots[k].real,6))
            imag = str(round(roots[k].imag,6))
            s += real
            if(imag[0] != '-'): s += '+'
            s += imag
            s += 'i'
            self.rootList.addItem(s)
          
        self.drawRoots(i)
          
    def removePoly(self):
        i = self.polyList.currentRow()
        del self.polynomials[i]
        self.polyList.takeItem(i)
        
        self.clearRootList()
        self.lastPolySelect = 0
        
        self.drawRoots(0, True, True)
        self.saveData()
        
    def rootSelected(self):
        root = self.polynomials[self.lastPolySelect][1][self.lastRootSelect]
        self.drawRoot(root, QtCore.Qt.red)
        
        i = self.rootList.currentRow()
        root = self.polynomials[self.lastPolySelect][1][i]
        self.drawRoot(root, QtCore.Qt.green)
        self.lastRootSelect = i
        
    def clearRootList(self):
        size = self.rootList.count()
        while size != 0:
            self.rootList.takeItem(0)
            size -= 1
        
    def saveData(self):
        db = shelve.open('data.db')
        db['polynomials'] = self.polynomials
        db['maxCoord'] = self.maxCoord
        db['scale'] = self.scale
        db.sync()
        db.close()
        
    # drawing functions
    def drawAxis(self):
        pen = QtGui.QPen(QtCore.Qt.white)
        brush = QtGui.QBrush(QtCore.Qt.white)
        self.plot.addRect(1, 1, 498, 498, pen, brush)
        pen = QtGui.QPen(QtCore.Qt.black)
        self.plot.addLine(1, 250, 498, 250, pen)
        self.plot.addLine(250, 1, 250, 498, pen)
        self.plot.addRect(1, 1, 497, 497, pen)
        
        self.plot.addLine(125, 245, 125, 255, pen)
        self.plot.addLine(375, 245, 375, 255, pen)
        self.plot.addLine(245, 125, 255, 125, pen)
        self.plot.addLine(245, 375, 255, 375, pen)
        
        val = round(125 * self.maxCoord / 200, 2)
        if val <= 0: val = 1
        
        path = QtGui.QPainterPath()
        font = QtGui.QFont()
        
        font.setPixelSize(10)
        font.setBold(False)
        font.setFamily("Courier")
        
        path.addText(122, 242, font, str(-val))
        path.addText(372, 242, font, str(val))
        path.addText(257, 127, font, str(val)+"i")
        path.addText(257, 377, font, str(-val)+"i")
        
        brush = QtGui.QBrush(QtCore.Qt.black)
        pen = QtGui.QPen(brush, 1) 
        
        self.plot.addPath(path, pen, brush)
        
    def drawRoot(self, root, color):
        x = root.real
        y = root.imag
        
        # transform point
        x1 = 250 + int(round(x * self.scale))
        y1 = 250 - int(round(y * self.scale))
        
        pen = QtGui.QPen(color)
        brush = QtGui.QBrush(color)
        #self.plot.addRect(x1-2, y1-2, 4, 4, pen, brush) 
        self.plot.addEllipse(x1-2, y1-2, 4, 4, pen, brush)
        
    def drawRoots(self, polyIndex, redrawAll = False, removal = False):    
        if redrawAll:
            if removal:
                maxCoord = -1
                for poly in self.polynomials:
                    coord = self.getMaxCoord(poly)
                    if coord > maxCoord: maxCoord = coord
                
                self.maxCoord = maxCoord
                if self.maxCoord == 0: self.maxCoord = 1
                self.scale = 200.0/self.maxCoord
                
                self.drawAxis()
                self.drawAllRoots()
                  
            else:
                maxCoord = self.getMaxCoord(self.polynomials[polyIndex]) 
                if maxCoord > self.maxCoord:
                    self.maxCoord = maxCoord
                    if self.maxCoord == 0: self.maxCoord = 1
                    self.scale = 200.0/self.maxCoord

                    self.drawAxis()
                    self.drawAllRoots()
                    
                else:
                    for root in self.polynomials[polyIndex][1]:
                        self.drawRoot(root, QtCore.Qt.blue)        
        else:
            last = self.lastPolySelect
            if last >= 0 and last != polyIndex:
                for root in self.polynomials[self.lastPolySelect][1]:
                    self.drawRoot(root, QtCore.Qt.blue)
            for root in self.polynomials[polyIndex][1]:
                self.drawRoot(root, QtCore.Qt.red)
            self.lastPolySelect = polyIndex
            
    def drawAllRoots(self):
        for poly in self.polynomials:
            for root in poly[1]:
                self.drawRoot(root, QtCore.Qt.blue)
    
    def getMaxCoord(self, polynomial):
        maxCoord = 0;
        for root in polynomial[1]:
          x = abs(root.real)
          y = abs(root.imag)
          if x > maxCoord: maxCoord = x
          if y > maxCoord: maxCoord = y
        return maxCoord

# add polynomial dialog class
class Ui_newPolyDialog(object):
    def setupUi(self, newPolyDialog):
        newPolyDialog.resize(309, 122)
        self.enterPolyLabel = QtGui.QLabel(newPolyDialog)
        self.enterPolyLabel.setGeometry(QtCore.QRect(10, 10, 331, 17))
        self.enterPolyLabel.setObjectName(_fromUtf8("enterPolyLabel"))
        self.label_11 = QtGui.QLabel(newPolyDialog)
        self.label_11.setGeometry(QtCore.QRect(222, 35, 21, 17))
        self.label_11.setObjectName(_fromUtf8("label_11"))
        self.a9 = QtGui.QLineEdit(newPolyDialog)
        self.a9.setGeometry(QtCore.QRect(10, 30, 31, 27))
        self.a9.setObjectName(_fromUtf8("a9"))
        self.label_12 = QtGui.QLabel(newPolyDialog)
        self.label_12.setGeometry(QtCore.QRect(162, 65, 21, 17))
        self.label_12.setObjectName(_fromUtf8("label_12"))
        self.a8 = QtGui.QLineEdit(newPolyDialog)
        self.a8.setGeometry(QtCore.QRect(70, 30, 31, 27))
        self.a8.setObjectName(_fromUtf8("a8"))
        self.a7 = QtGui.QLineEdit(newPolyDialog)
        self.a7.setGeometry(QtCore.QRect(130, 30, 31, 27))
        self.a7.setObjectName(_fromUtf8("a7"))
        self.a6 = QtGui.QLineEdit(newPolyDialog)
        self.a6.setGeometry(QtCore.QRect(190, 30, 31, 27))
        self.a6.setObjectName(_fromUtf8("a6"))
        self.a5 = QtGui.QLineEdit(newPolyDialog)
        self.a5.setGeometry(QtCore.QRect(250, 30, 31, 27))
        self.a5.setObjectName(_fromUtf8("a5"))
        self.a4 = QtGui.QLineEdit(newPolyDialog)
        self.a4.setGeometry(QtCore.QRect(10, 60, 31, 27))
        self.a4.setObjectName(_fromUtf8("a4"))
        self.a3 = QtGui.QLineEdit(newPolyDialog)
        self.a3.setGeometry(QtCore.QRect(70, 60, 31, 27))
        self.a3.setObjectName(_fromUtf8("a3"))
        self.a2 = QtGui.QLineEdit(newPolyDialog)
        self.a2.setGeometry(QtCore.QRect(130, 60, 31, 27))
        self.a2.setObjectName(_fromUtf8("a2"))
        self.label_13 = QtGui.QLabel(newPolyDialog)
        self.label_13.setGeometry(QtCore.QRect(102, 65, 21, 17))
        self.label_13.setObjectName(_fromUtf8("label_13"))
        self.label_14 = QtGui.QLabel(newPolyDialog)
        self.label_14.setGeometry(QtCore.QRect(282, 65, 21, 17))
        self.label_14.setObjectName(_fromUtf8("label_14"))
        self.a1 = QtGui.QLineEdit(newPolyDialog)
        self.a1.setGeometry(QtCore.QRect(190, 60, 31, 27))
        self.a1.setObjectName(_fromUtf8("a1"))
        self.label_15 = QtGui.QLabel(newPolyDialog)
        self.label_15.setGeometry(QtCore.QRect(282, 35, 21, 17))
        self.label_15.setObjectName(_fromUtf8("label_15"))
        self.label_16 = QtGui.QLabel(newPolyDialog)
        self.label_16.setGeometry(QtCore.QRect(222, 65, 21, 17))
        self.label_16.setObjectName(_fromUtf8("label_16"))
        self.label_17 = QtGui.QLabel(newPolyDialog)
        self.label_17.setGeometry(QtCore.QRect(42, 35, 21, 17))
        self.label_17.setObjectName(_fromUtf8("label_17"))
        self.a0 = QtGui.QLineEdit(newPolyDialog)
        self.a0.setGeometry(QtCore.QRect(250, 60, 31, 27))
        self.a0.setObjectName(_fromUtf8("a0"))
        self.label_18 = QtGui.QLabel(newPolyDialog)
        self.label_18.setGeometry(QtCore.QRect(42, 65, 21, 17))
        self.label_18.setObjectName(_fromUtf8("label_18"))
        self.label_19 = QtGui.QLabel(newPolyDialog)
        self.label_19.setGeometry(QtCore.QRect(162, 35, 21, 17))
        self.label_19.setObjectName(_fromUtf8("label_19"))
        self.label_20 = QtGui.QLabel(newPolyDialog)
        self.label_20.setGeometry(QtCore.QRect(102, 35, 21, 17))
        self.label_20.setObjectName(_fromUtf8("label_20"))
        self.addPolyBtn = QtGui.QPushButton(newPolyDialog)
        self.addPolyBtn.setGeometry(QtCore.QRect(180, 90, 121, 27))
        self.addPolyBtn.setObjectName(_fromUtf8("addPolyBtn"))
        self.cancelBtn = QtGui.QPushButton(newPolyDialog)
        self.cancelBtn.setGeometry(QtCore.QRect(50, 90, 121, 27))
        self.cancelBtn.setObjectName(_fromUtf8("cancelBtn"))

        self.retranslateUi(newPolyDialog)
        QtCore.QObject.connect(self.cancelBtn, QtCore.SIGNAL(_fromUtf8("clicked()")), newPolyDialog.reject)
        #QtCore.QObject.connect(self.addPolyBtn, QtCore.SIGNAL(_fromUtf8("clicked()")), newPolyDialog.accept)
        QtCore.QMetaObject.connectSlotsByName(newPolyDialog)

    def retranslateUi(self, newPolyDialog):
        newPolyDialog.setWindowTitle(_translate("newPolyDialog", "New polynomial", None))
        self.enterPolyLabel.setText(_translate("newPolyDialog", "Enter polynomial coefficients", None))
        self.label_11.setText(_translate("newPolyDialog", "x⁶", None))
        self.a3.setText(_translate("newPolyDialog", "0", None))
        self.label_12.setText(_translate("newPolyDialog", "x²", None))
        self.a7.setText(_translate("newPolyDialog", "0", None))
        self.a8.setText(_translate("newPolyDialog", "0", None))
        self.a2.setText(_translate("newPolyDialog", "0", None))
        self.label_13.setText(_translate("newPolyDialog", "x³", None))
        self.a6.setText(_translate("newPolyDialog", "0", None))
        self.label_14.setText(_translate("newPolyDialog", "x⁰", None))
        self.a1.setText(_translate("newPolyDialog", "0", None))
        self.a5.setText(_translate("newPolyDialog", "0", None))
        self.label_15.setText(_translate("newPolyDialog", "x⁵", None))
        self.label_16.setText(_translate("newPolyDialog", "x¹", None))
        self.a9.setText(_translate("newPolyDialog", "0", None))
        self.label_17.setText(_translate("newPolyDialog", "x⁹", None))
        self.a0.setText(_translate("newPolyDialog", "0", None))
        self.a4.setText(_translate("newPolyDialog", "0", None))
        self.label_18.setText(_translate("newPolyDialog", "x⁴", None))
        self.label_19.setText(_translate("newPolyDialog", "x⁷", None))
        self.label_20.setText(_translate("newPolyDialog", "x⁸", None))
        self.addPolyBtn.setText(_translate("newPolyDialog", "Add polynomial", None))
        self.cancelBtn.setText(_translate("newPolyDialog", "Cancel", None))
        
if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    MainWindow = QtGui.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())

