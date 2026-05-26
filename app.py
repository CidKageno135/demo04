from flask import Flask, render_template, jsonify
import time
import requests
import urllib3
import pandas as pd
from io import StringIO
from requests.exceptions import RequestException, SSLError

app = Flask(__name__)

# 數據網址
DATA_URL = "https://data.ntpc.gov.tw/api/datasets/781b822e-214a-4b9a-b4db-32c9f4626d98/csv/file"
url = DATA_URL
REQUEST_HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) FlaskDataDemo/1.0",
}


def request_csv(verify=True):
    """下載 CSV，短暫網路錯誤時重試。"""
    last_error = None

    for attempt in range(3):
        try:
            response = requests.get(
                DATA_URL,
                headers=REQUEST_HEADERS,
                timeout=30,
                verify=verify,
            )
            response.raise_for_status()
            return response
        except SSLError:
            raise
        except RequestException as exc:
            last_error = exc
            if attempt < 2:
                time.sleep(1)

    raise last_error

def fetch_data():
    """從網址下載並處理資料"""
    try:
        try:
            response = request_csv()
        except SSLError:
            urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
            response = request_csv(verify=False)
        
        # 以 UTF-8-SIG 編碼讀取 (自動移除 BOM)
        df = pd.read_csv(StringIO(response.content.decode('utf-8-sig')))
        
        # 清理欄位名稱（移除任何殘留的 BOM）
        df.columns = [col.lstrip('\ufeff').strip() for col in df.columns]

        # 新北資料欄位名稱目前是 nddate，這裡正規化成 enddate 方便前端使用。
        if 'nddate' in df.columns and 'enddate' not in df.columns:
            df = df.rename(columns={'nddate': 'enddate'})
        
        return df, None
    except Exception as e:
        return None, f"{type(e).__name__}: {e}"


def unique_text_values(df, column):
    """取得指定欄位的非空唯一文字值。"""
    if column not in df.columns:
        return []

    values = df[column].dropna().astype(str).str.strip()
    return sorted(value for value in values.unique() if value)


def date_range(df, column):
    """回傳指定日期欄位的最小與最大日期。"""
    if column not in df.columns:
        return {'min': None, 'max': None}

    dates = pd.to_datetime(df[column], errors='coerce').dropna()
    if dates.empty:
        return {'min': None, 'max': None}

    return {
        'min': dates.min().strftime('%Y-%m-%d'),
        'max': dates.max().strftime('%Y-%m-%d'),
    }


def records_from_df(df):
    """轉成可被 JSON/Jinja 正確處理的 records。"""
    clean_df = df.astype(object).where(pd.notna(df), None)
    return clean_df.to_dict(orient='records')


def build_stats(df):
    """準備新北公告資料的統計信息。"""
    type_values = unique_text_values(df, 'type')
    author_values = unique_text_values(df, 'author')

    return {
        'total_rows': len(df),
        'total_columns': len(df.columns),
        'columns': df.columns.tolist(),
        'unique_authors': len(author_values),
        'author_values': author_values,
        'type_values': type_values,
        'startdate_range': date_range(df, 'startdate'),
        'enddate_range': date_range(df, 'enddate'),
        'pubdate_range': date_range(df, 'pubdate'),
        'source_url': DATA_URL,
    }

@app.route('/')
def index():
    """主頁 - 顯示所有數據"""
    df, error = fetch_data()
    
    if error:
        return render_template(
            'index.html',
            error=error,
            data_list=[],
            columns=[],
            stats=None,
            source_url=DATA_URL,
        )
    
    # 準備統計信息
    stats = build_stats(df)
    
    # 準備資料列表
    data_list = records_from_df(df)
    
    return render_template('index.html', 
                         data_list=data_list,
                         columns=df.columns.tolist(),
                         stats=stats,
                         source_url=DATA_URL,
                         error=None)

@app.route('/api/data')
def api_data():
    """API 端點 - 返回 JSON 格式數據"""
    df, error = fetch_data()
    
    if error:
        return jsonify({'error': error}), 400
    
    return jsonify(records_from_df(df))

@app.route('/api/summary')
def api_summary():
    """API 端點 - 返回數據摘要"""
    df, error = fetch_data()
    
    if error:
        return jsonify({'error': error}), 400
    
    summary = build_stats(df)
    
    return jsonify(summary)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
