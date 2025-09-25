# -*- coding: utf-8 -*-
# web
import socket
import threading

# gui
from PyQt6 import QtWidgets, QtGui
from PyQt6.QtCore import QEvent, Qt 
from PyQt6.QtWidgets import QApplication, QListWidget, QLineEdit, QVBoxLayout, QWidget
import sys


class MyWidget(QtWidgets.QWidget):
    w_size = 500 # 視窗大小
    h_size = 600
    voteli = [] # 選項
    votecnt = [] # 選項票數
    tit = '' # 投票主題

    def __init__(self, votecnt, votel, subj): # 設定傳入的投票項目
        self.voteli = votel
        self.tit = subj
        self.votecnt = votecnt
        super().__init__()
        self.setWindowTitle(self.tit)
        self.resize(self.w_size, self.h_size)
        self.ui(subj)
        print(self.voteli)

        rcv = threading.Thread(target = self.receive) # 接收資料
        rcv.start()

    def ui(self, subj): # 視窗程式畫面與元件事件綁定
        self.box = QtWidgets.QWidget(self)
        self.box.setGeometry(10, 10, self.w_size - 20, self.h_size - 100)     # 設定位置
        self.v_layout = QtWidgets.QVBoxLayout(self.box) # 排版

        self.showquestion = QtWidgets.QLabel(subj) # 顯示主題
        self.showquestion.setWordWrap(True)

        self.listwidget = QtWidgets.QListWidget(self)  # 建立列表選擇框元件
        self.listwidget.addItems(self.voteli)    # 建立並顯示選項
        for i in range(len(self.voteli)):
            self.listwidget.item(i).setText('　' + str(self.votecnt[i]) + '　|　　' + self.voteli[i])
        self.listwidget.itemClicked.connect(self.toggle_selection) # 選擇選項點擊事件：投票

        self.showvote = QtWidgets.QLabel("目前選擇 : ") # 顯示目前選擇
        self.showvote.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.showvote.setWordWrap(True) # 允許換行

        self.showc = QtWidgets.QLabel("Client: ") # 顯示提示

        self.v_layout.addWidget(self.showquestion) # 排版以上元件      
        self.v_layout.addWidget(self.listwidget)
        self.v_layout.addWidget(self.showvote)
        self.v_layout.addWidget(self.showc)
    
        self.style() # QSS
        self.v_layout.setSpacing(20)

    def style(self): # QSS
        self.setStyleSheet("""
                font-size: 15px;
                QListWidget::item{
                    padding-top: 10px;
                }
        """)

    def toggle_selection(self, item): # 點擊事件：投票
        ind = self.listwidget.row(item) # 取得點擊項目的 index
        if item.isSelected(): # 選擇項目狀態判斷
            try:
                client.send(str(ind).encode(FORMAT)) # 傳送點擊項目的 index 至 server 表示投此項目
            except:
                self.showc.setText("連線出現問題，中斷連線")
                print("server 中斷連線")
                client.close()
        self.show_vote(ind) # 顯示目前選擇
    
    def show_vote(self, ind): # 顯示目前選擇
        st = "目前選擇 : \n　" + self.voteli[ind] 
        self.showvote.setText(st) # 套用文字
        self.showvote.adjustSize()

    def show_item(self, i): # 更新並顯示選項票數
        self.listwidget.item(i).setText('　' + str(self.votecnt[i]) + '　|　　' + self.voteli[i])
        self.showc.setText('　' +  self.voteli[i]+"  vote successfully") 
    #web
    def receive(self): 
        while True:
            try:
                message = client.recv(1024).decode(FORMAT) # 接收
                if(message=="pollover"): 
                    self.showc.setText("server 已結束投票 中斷連線")
                    print("server 中斷連線")
                    client.close()
                    break
                print(message)
                ind = int(message) # 更新其他人投的票（用 index 辨識）
                self.votecnt[ind] += 1           
                self.show_item(ind)
            except:
                # an error will be printed on the command line or console if there's an error
                self.showc.setText("連線出現問題 中斷連線")
                print("server 中斷連線")
                client.close()
                break

if __name__ == '__main__':
    HOST = "127.0.0.1"
    PORT = 7000
    FORMAT = "utf-8"

    client = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    try:
        client.connect((HOST, PORT))
        print("投票建立中....")
        votelist = []
        votecnt = []
        titlename = client.recv(1024).decode() # 接收主題
        num = int(client.recv(1024).decode()) # 接收選項數

        for i in range(num):
            data = client.recv(1024).decode() # 選項
            votelist.append(data)
            data = int(client.recv(1024).decode()) # 該選項當前的票數
            votecnt.append(data)
            print(data)
        print(client.recv(1024).decode(FORMAT))

        app = QtWidgets.QApplication(sys.argv)
        Form = MyWidget(votecnt, votelist, titlename) # 建立並顯示 GUI
        Form.show()
        sys.exit(app.exec())
    except:
        print("無法連線")

