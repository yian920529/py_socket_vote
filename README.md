# 網路程式設計 
組員:邱翊銨 顏莉諭
## 介紹
python投票系統
[DEMO影片連結](https://www.youtube.com/watch?v=zr6ayi5nYOs) (若寫無法撥放請f5重新整理)

### 簡介
使用 Python實作的投票系統，Server 建立投票（投票主題、投票選項）<br>
Clients 加入投票。其中透過PyQt6 實作 GUI、Socket 進行 TCP連線<br>
Threading 服務各 Client<br>
與一般投票系統不同之處在於不限制 Clients投票次數<br>
因此相較之下是個較自由的投票系統，適合日常使用

### 構想
架構：Client / Server<br>
語言：Python<br>
GUI：PyQt6

### 設計重點
1.自訂主題、選項、手動結束的投票系統 <br>
2.不限制 Clients各選項的投票次數<br>

## 操作說明
主要以滑鼠鍵盤來操作。  
## 操作方法
請參考影片

## 作品大致模樣:
<img width="569" height="393" alt="image" src="https://github.com/user-attachments/assets/5fe66d7b-937e-4138-a2fe-0881d8515223" />

