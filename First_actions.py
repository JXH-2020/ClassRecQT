from PyQt5.QtCore import Qt
import Second_actions
from login_resgister import Ui_MainWindow as loginUI
from Main_Show import Ui_MainWindow as MainUI
from PyQt5.QtWidgets import QMessageBox, QMainWindow, QApplication

import sys

from predictImage import loadModel


class loginLogic(QMainWindow, loginUI):
    def __init__(self):
        super(loginLogic, self).__init__()
        self.model = None
        self.another_window = None
        self.setupUi(self)
        self.run()

    # 按钮绑定事件
    def run(self):
        # 登录
        self.pushButton.clicked.connect(self.login_)
        # 注册
        self.pushButton_2.clicked.connect(self.register_)
        self.model = loadModel('test-best-origin.onnx')
    # 登录事件
    def login_(self):
        name = self.lineEdit.text()
        password = self.lineEdit_2.text()
        with open('person.txt', 'r') as file:
            lines = file.readlines()
            for line in lines:
                p_name = line.split('\t')[0]
                p_password = line.split('\t')[-1].split('\n')[0]

                if p_name == name and p_password == password:
                    self.another_window = Second_actions.AnotherWindowActions()
                    self.another_window.show()
                    self.another_window.model = self.model
                    self.close()

        pass

    # 注册事件
    def register_(self):
        name = self.lineEdit.text()
        password = self.lineEdit_2.text()
        Tag = 0
        with open('person.txt', 'r') as file:
            lines = file.readlines()
            print(lines)
            for line in lines:
                p_name = line.split('\t')[0]
                if name == p_name:
                    Tag = 1
        if Tag == 0:
            with open('person.txt', 'a+') as file:
                file.write(name + '\t' + password + '\n')
                file.close()
                msg_box = QMessageBox(QMessageBox.Question, '注册', '恭喜您注册成功！')
        else:
            msg_box = QMessageBox(QMessageBox.Question, '注册', '数据库中已有该昵称！')
        msg_box.exec_()
        pass

    # 重新启动界面
    def reshow(self):
        self.show()


# 运行界面循环
def main_():
    app = QApplication(sys.argv)
    login_ = loginLogic()
    login_.show()
    login_.setStyleSheet("#MainWindow{border-image:url(background.jpg)}")
    sys.exit(app.exec_())


if __name__ == '__main__':
    main_()
