import cv2
import numpy as np
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPalette

import Main_Show
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QFileDialog, QMessageBox, QGraphicsScene
from PyQt5 import QtWidgets, QtGui

# 业务类需要继承两个类，一个设计的主界面，另一个是QMainWindow
from predictImage import loadModel, predict


class AnotherWindowActions(Main_Show.Ui_MainWindow, QMainWindow):
    def __init__(self):
        """
         特别注意（最容易出错）：
         1.派生新类访问基类需要super(),同时它的参数是基类文件下的类及“ui_home_window.py中的
           Ui_MainWindow类”，
        """

        super(Main_Show.Ui_MainWindow, self).__init__()
        self.model = None
        self.scene = None
        self.setupUi(self)
        self.run()

    # 按钮绑定事件
    def run(self):
        # 选择图片
        self.pushButton_2.clicked.connect(self.select)
        self.label_3.setText('该系统由....制作的，通过2.5w张数据集，按比\n例8：2分为训练集和测试集，主干网络是ResNet\n50，检测层通过全连接预测5个类别，进行农作物识\n别研究。')
        # 识别
        self.pushButton.clicked.connect(self.rec)
        self.label_2.setFrameShape(QtWidgets.QFrame.Box)
        self.showContext()
        self.pushButton_3.clicked.connect(self.showContext)
        self.pushButton_4.clicked.connect(self.showRec)

    # 选择图片
    def select(self):
        imgName, imgType = QFileDialog.getOpenFileName(self, "打开图片", "", "*.jpg;;*.png;;All Files(*)")
        jpg = QtGui.QPixmap(imgName).scaled(self.label_2.width(), self.label_2.height())
        self.label_2.setPixmap(jpg)
        pass

    # 识别事件
    def rec(self):
        imgptr = self.label_2.pixmap().toImage()
        ptr = imgptr.constBits()
        ptr.setsize(imgptr.byteCount())
        mat = np.array(ptr).reshape(imgptr.height(), imgptr.width(), 4)
        mat_img = cv2.cvtColor(mat, cv2.COLOR_BGR2RGB)
        mat_img = cv2.cvtColor(mat_img, cv2.COLOR_BGR2RGB)
        result = predict(mat_img, self.model)
        self.textBrowser.setPlainText(result)
        pass

    def showRec(self):
        self.pushButton.show()
        self.label.show()
        self.label_2.show()
        self.pushButton_2.show()
        self.textBrowser.show()
        self.label_3.close()
        pass

    def showContext(self):
        self.pushButton.close()
        self.label.close()
        self.label_2.close()
        self.pushButton_2.close()
        self.textBrowser.close()
        self.label_3.show()
        pass
