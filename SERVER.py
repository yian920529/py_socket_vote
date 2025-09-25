# web
import socket
import threading
import time

# gui
from PyQt6 import QtWidgets, QtGui
from PyQt6.QtCore import QEvent, Qt 
from PyQt6.QtWidgets import QApplication, QListWidget, QLineEdit, QVBoxLayout, QWidget
import sys

# gui
class MyWidget(QtWidgets.QWidget): # 建立投票
    w_size = 500
    h_size = 600
    voteli = ['選項 1 (右鍵編輯或刪除)', '選項 2'] # 預設選項
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle('POLL')
        self.current_item = None
        self.resize(self.w_size, self.h_size)
        self.style()
        self.ui()
        self.w_size = 500
        self.h_size = 600

    def ui(self): # 視窗程式畫面與元件事件綁定
        self.box = QtWidgets.QWidget(self)
        self.box.setGeometry(10, 10, self.w_size - 20, self.h_size - 100)     # 設定位置
        self.v_layout = QtWidgets.QVBoxLayout(self.box)
        self.h_layout = QtWidgets.QHBoxLayout()

        self.question_inp = QtWidgets.QPlainTextEdit(self)  # 投票主題輸入框
        self.question_inp.setPlainText('投票主題 : （最多 100 字）')
        self.question_inp.installEventFilter(self)  # 字數限制
        self.question_inp.setFixedHeight(100)
    
        self.listwidget = QtWidgets.QListWidget(self)  # 建立列表選擇框元件
        self.listwidget.addItems(self.voteli)    # 加入選項
        self.listwidget.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu) # 選項右鍵事件綁定（修改、刪除）
        self.listwidget.customContextMenuRequested.connect(self.on_context_menu)
        
        self.senddata = QtWidgets.QLineEdit(self) # 新增選項輸入框
        self.senddata.setMaxLength(30) # 字數限制

        self.add_button = QtWidgets.QPushButton("添加") # 新增選項按鈕
        self.add_button.clicked.connect(self.add_item)  # 按鈕事件綁定

        self.subm_button = QtWidgets.QPushButton("建立投票") # 建立投票按鈕
        self.subm_button.clicked.connect(self.createp) # 按鈕事件綁定

        self.v_layout.addWidget(self.question_inp) # 排版以上元件
        self.v_layout.addWidget(self.listwidget)
        self.h_layout.addWidget(self.senddata)
        self.h_layout.addWidget(self.add_button)
        self.v_layout.addLayout(self.h_layout)
        self.v_layout.addWidget(self.subm_button)
        
    def style(self): # QSS
        self.setStyleSheet('''
            font-size: 15px;
            QListWidget{
                color:#00f;
            }
            QListWidget::item{
                width:30px;
            }
            QListWidget::item:selected{
                color:#f00;
                background:#000;
            }
            
        ''')

    def eventFilter(self, obj, event): # 投票主題輸入框字數限制
        if obj == self.question_inp and event.type() == QEvent.Type.KeyPress: # 輸入內容
            text = self.question_inp.toPlainText()
            key = event.key()
            if key == Qt.Key.Key_Backspace or key == Qt.Key.Key_Left or key == Qt.Key.Key_Right or key == Qt.Key.Key_Up or key == Qt.Key.Key_Down:
                return super().eventFilter(obj, event)  # 只允許刪除和移動
            elif len(text) >= 100:
                return True  # 超過限制字數就忽略輸入內容
        return super().eventFilter(obj, event)

    def on_context_menu(self, pos): # 選項右鍵事件綁定（修改、刪除）
        item = self.listwidget.itemAt(pos) # 透過點擊位置取得欲操作的選項

        if item:
            context = QtWidgets.QMenu(self) # 建立選單

            ac_edit = QtGui.QAction("編輯", self) # 選項
            ac_dele = QtGui.QAction("刪除", self)

            ac_edit.triggered.connect(lambda: self.onContextAction(item, "編輯")) # 綁定事件
            ac_dele.triggered.connect(lambda: self.onContextAction(item, "刪除"))

            context.addAction(ac_edit) # 選項加入選單
            context.addAction(ac_dele)

            context.exec(self.listwidget.mapToGlobal(pos))

    def onContextAction(self, item, action): # 綁定的事件
        print(f"Selected item: {item.text()}, Action: {action}")
        match action:
            case '編輯':
                self.startEditing(item)
            case '刪除':
                row = self.listwidget.row(item) # 選擇
                self.listwidget.takeItem(row) # 刪除

    
    def startEditing(self, item): # 開始編輯選項內容
        if self.current_item is not None:
            self.closeEditor()

        self.current_item = item

        editor = QLineEdit(item.text()) # 欲編輯的選項上開啟編輯器
        self.listwidget.setItemWidget(item, editor)
        editor.setMaxLength(30)

        editor.editingFinished.connect(self.finishEditing) # 完成編輯後呼叫的事件
        
        editor.setFocus()

    def finishEditing(self): # 關閉編輯器
        if self.current_item is not None:
            editor = self.listwidget.itemWidget(self.current_item)
            if editor:
                self.current_item.setText(editor.text()) # 套用文字
                self.listwidget.removeItemWidget(self.current_item)
                editor.deleteLater()

                self.current_item = None

    def add_item(self): # 新增項目
        try:
            text = self.senddata.text() 
            if text:
                self.listwidget.addItem(text) # 加入新項目內容
                self.senddata.clear()
                self.senddata.setFocus()
        except:
            pass
        
    def createp(self): # 建立投票
        self.voteli = []
        strt = self.question_inp.toPlainText() # 取得投票主題
        for index in range(self.listwidget.count()): # 將所有選項加入列表
            self.voteli.append(self.listwidget.item(index).text())
        self.nw = newWindow(self.voteli, strt) # 傳送至新視窗
        self.nw.show()
        self.close()
        
class newWindow(QtWidgets.QWidget): # 正式投票
    w_size = 500
    h_size = 600
    voteli = []
    votecnt = []
    tit = ''

    def __init__(self, votel, subj): # 設定傳入的投票項目
        self.current_item = None
        self.voteli = votel
        super().__init__()
        self.setWindowTitle(subj)
        self.resize(self.w_size, self.h_size)
        self.ui(subj)
        self.tit = subj

        #web
        start = threading.Thread(target=self.startChat) # 收送資料
        start.start()

    def ui(self, subj): # 視窗程式畫面與元件事件綁定
        self.box = QtWidgets.QWidget(self)
        self.box.setGeometry(10, 10, self.w_size - 20, self.h_size - 100)     # 設定位置
        self.v_layout = QtWidgets.QVBoxLayout(self.box)

        self.showquestion = QtWidgets.QLabel(subj + ' ( 請勿關閉此視窗 )')
        self.showquestion.setWordWrap(True)

        self.listwidget = QtWidgets.QListWidget(self)  # 建立列表選擇框元件
        self.listwidget.setSelectionMode( # 僅供檢視
            QtWidgets.QAbstractItemView.SelectionMode.NoSelection
        )
        self.listwidget.addItems(self.voteli)    # 建立選單
        for i in range(len(self.voteli)): #　設定初始票數及顯示選項
            self.votecnt.append(0)
            self.listwidget.item(i).setText('　' + str(self.votecnt[i]) + '　|　　' + self.voteli[i])

        self.v_layout.addWidget(self.showquestion)        
        self.v_layout.addWidget(self.listwidget)

        self.subm_button = QtWidgets.QPushButton("結束投票")
        self.subm_button.clicked.connect(self.finip)
        self.showvote = QtWidgets.QLabel("Client: ")

        self.v_layout.addWidget(self.subm_button)
        self.v_layout.addWidget(self.showvote)
        self.style()
        self.v_layout.setSpacing(20)

    def style(self):
        self.setStyleSheet("""
                font-size: 15px;
                QListWidget::item{
                    padding-top: 10px;
                }
        """)

    def show_item(self, i): # 更新 index 為 i 的選項文字
        self.listwidget.item(i).setText('　' + str(self.votecnt[i]) + '　|　　' + self.voteli[i])
    
    #web
    def finip(self):
        self.showvote.setText("~~~結束投票~~~")
        while len(clients) != 0:  # 斷線
            for client in clients:
                try:
                    client.send("pollover".encode())
                    client.close()
                except:
                    print("client自行斷線")
                    pass
                clients.remove(client)
        s.close()

    def startChat(self):
        def handle(conn, addr):
            self.showvote.setText(f"New connection : {addr}")
            print(f"New connection : {addr}")
            connected = True
            while connected:
                try:
                    message = conn.recv(1024).decode() # 接收被投票的選項 index
                    print(message)
                    ind = int(message)
                    self.votecnt[ind] += 1 # 增加票數
                    broadcastMessage(message.encode()) # 傳送給所有 client
                    self.show_item(ind) # 更新被投票的選項
                except:
                    break
            conn.close()
            
        self.showvote.setText("Server is working on " + HOST)
        print("Server is working on " + HOST)
        
        s.listen()
 
        while True:
            try:
                conn, addr = s.accept()
            except:
                break
            conn.send(self.tit.encode())
            time.sleep(0.5)

            conn.send(str(len(self.voteli)).encode()) #　傳送主題

            for i in range(len(self.voteli)): # 傳送選項及其當前票數
                conn.send(self.voteli[i].encode())
                time.sleep(0.2)
                conn.send(str(self.votecnt[i]).encode())
                time.sleep(0.2)

            clients.append(conn) 
            conn.send('Connection successful!'.encode(FORMAT))

            # Start the handling thread
            thread = threading.Thread(target=handle, args=(conn, addr))
            thread.start()
     
def broadcastMessage(message): # 通知所有 client 有新投票
    for client in clients:
        outdata = message.decode()
        print(outdata)
        try:
            client.send(outdata.encode(FORMAT))
        except:
            client.close()
            clients.remove(client)
    
if __name__ == '__main__':
    # web
    PORT = 7000
    HOST = "127.0.0.1"
    FORMAT = "utf-8"
    clients = []

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # tcp
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    s.bind((HOST, PORT))
    s.listen(5)

    app = QtWidgets.QApplication(sys.argv)
    Form = MyWidget()
    Form.show()
    sys.exit(app.exec())
