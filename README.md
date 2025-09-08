# 🎰 Slot Machine Probability Model & Simulation

本專案展示了 **老虎機（Slot Machine）的數學建模與模擬**，結合 **Excel 機率模型** 與 **Python 程式**，分析不同遊戲設計下的 **期望值、RTP（Return to Player）、中獎率、以及破產風險**。  

- 在 **Excel** 中，建立了三台不同型態老虎機的機率模型，計算轉輪組合、Paytable 期望值與遊戲平衡性。  
- 在 **Python** 中，撰寫模擬程式進行大量 Spins，產生 **RTP 曲線、獲利分布、資金曲線**，驗證數學模型的正確性。   

---

## 📂 專案架構
```bash
├── 老虎機python模擬
│ ├── configs.py # 遊戲設定、轉輪組合、Paytable、模擬核心函數
│ ├── linegame1.py # 單線老虎機 (Line Game 1)
│ ├── linegame2.py # 單線老虎機 (Line Game 2, 含 Free Game)
│ ├── waygame.py # 多路老虎機 (Way Game)
│ ├── simulate.py # 大量模擬與統計圖表
├── 老虎機機率模型/
│ └── 機率模型設置.xlsx # 各老虎機數學模型
└── README.md
```

---

## ▶️ 使用方式
```bash
🎲 單次 Spin
linegame1.py
linegame2.py
waygame.py
⚙️ 遊戲參數設定
configs.py

```

## 📊 模擬與統計分析
```bash
simulate.py
模擬完成後會輸出：
資金曲線 (Bankroll Curve)
單次獲利分布 (Profit Histogram)
RTP 隨 Spin 變化圖 (RTP over Spins)
```
---

## 🧮 Excel 模型 (數學建模)
```bash
在 models/ 資料夾中，包含三台不同老虎機的數學模型：
Reel 配置
Paytable 設定
PayLines 設定
理論 RTP 計算
Free Game 與 Scatter 概率設計
模型使用Python模擬結果二次驗證，並用於遊戲平衡性分析。
```
---

## 🚀 重點
```bash
組合機率與期望值計算：驗證遊戲公平性與平衡性
數據模擬與視覺化：大量 Spins 測試，輸出 RTP 曲線與狀態分布
Excel + Python 整合：理論建模與程式模擬互相驗證
```
---

## 📌 未來期望擴充
```
更多 Paylines 組合與複雜 Bonus 遊戲模式
運用假設檢定來驗證模擬結果是否符合模型機率假設
透過轉移矩陣計算遊玩時在各個狀態間的轉移情形和各個狀態下至吸收前的暫態期望停留步數
```
---

## ⚙️ 
```bash
建議使用 Python 3.9+  
requirements : 
numpy
pandas
matplotlib
seaborn
```



