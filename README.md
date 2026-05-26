# Flask 活動資料展示平台

將原始的數據獲取腳本轉換成 Flask Web 應用程序。

## 項目結構

```
demo04/
├── app.py                    # Flask 主應用
├── requirements.txt          # 依賴包列表
├── fetch_data_improved.py    # 原始腳本 (參考)
└── templates/
    └── index.html            # 主頁模板
```

## 快速開始

### 1. 安裝依賴
```bash
pip install -r requirements.txt
```

### 2. 運行應用
```bash
python app.py
```

### 3. 訪問應用
打開瀏覽器，訪問：`http://localhost:5000`

## 功能特性

✅ **主頁 (`/`)** 
- 顯示所有活動資料
- 展示統計信息 (總行數、欄位數等)
- 地理位置範圍 (經緯度)
- 完整的資料表格

✅ **API 端點**
- `/api/data` - 返回所有資料 (JSON)
- `/api/summary` - 返回資料摘要 (JSON)

## 改進點

相比原始腳本：
- 🌐 提供 Web 界面而不是控制台輸出
- 📊 美觀的數據可視化展示
- 🔌 提供 REST API 端點
- ♻️ 可重複使用的 `fetch_data()` 函數
- 🎨 使用 Bootstrap 5 美化 UI

## 依賴包

- **flask** - Web 框架
- **requests** - HTTP 請求
- **pandas** - 數據處理
