from flask import Flask, render_template, jsonify
import requests
import pandas as pd
from io import StringIO

app = Flask(__name__)

# 數據網址
url = "https://data.kcg.gov.tw/File/DirectDownload/80bbbbd3-9ee4-4244-98e9-b4c08deda91b"

def fetch_data():
    """從網址下載並處理資料"""
    try:
        response = requests.get(url, timeout=30)
        response.raise_for_status()
        
        # 以 UTF-8-SIG 編碼讀取 (自動移除 BOM)
        df = pd.read_csv(StringIO(response.content.decode('utf-8-sig')))
        
        # 清理欄位名稱（移除任何殘留的 BOM）
        df.columns = [col.lstrip('\ufeff') for col in df.columns]
        
        return df, None
    except Exception as e:
        return None, str(e)

@app.route('/')
def index():
    """主頁 - 顯示所有數據"""
    df, error = fetch_data()
    
    if error:
        return render_template('index.html', error=error, data=None, stats=None)
    
    # 準備統計信息
    stats = {
        'total_rows': len(df),
        'total_columns': len(df.columns),
        'unique_ids': int(df['Id'].nunique()),
        'status_values': list(df['Status'].unique()),
        'px_min': float(df['Px'].min()),
        'px_max': float(df['Px'].max()),
        'py_min': float(df['Py'].min()),
        'py_max': float(df['Py'].max()),
    }
    
    # 準備資料列表
    data_list = df.to_dict(orient='records')
    
    return render_template('index.html', 
                         data_list=data_list,
                         columns=df.columns.tolist(),
                         stats=stats,
                         error=None)

@app.route('/api/data')
def api_data():
    """API 端點 - 返回 JSON 格式數據"""
    df, error = fetch_data()
    
    if error:
        return jsonify({'error': error}), 400
    
    return jsonify(df.to_dict(orient='records'))

@app.route('/api/summary')
def api_summary():
    """API 端點 - 返回數據摘要"""
    df, error = fetch_data()
    
    if error:
        return jsonify({'error': error}), 400
    
    summary = {
        'total_rows': len(df),
        'total_columns': len(df.columns),
        'columns': df.columns.tolist(),
        'unique_ids': int(df['Id'].nunique()),
        'status_values': list(df['Status'].unique()),
        'geographic_range': {
            'px': {
                'min': float(df['Px'].min()),
                'max': float(df['Px'].max())
            },
            'py': {
                'min': float(df['Py'].min()),
                'max': float(df['Py'].max())
            }
        }
    }
    
    return jsonify(summary)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
