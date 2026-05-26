import requests
import pandas as pd
from io import StringIO

# 網址
url = "https://data.kcg.gov.tw/File/DirectDownload/80bbbbd3-9ee4-4244-98e9-b4c08deda91b"

try:
    print("📥 正在下載資料...\n")
    response = requests.get(url, timeout=30)
    response.raise_for_status()
    
    print(f"📋 檔案資訊:")
    print(f"   - HTTP 狀態碼: {response.status_code}")
    print(f"   - Content-Type: {response.headers.get('content-type', '未知')}\n")
    
    # 以 UTF-8-SIG 編碼讀取 (自動移除 BOM)
    df = pd.read_csv(StringIO(response.content.decode('utf-8-sig')))
    print(f"✓ 資料讀取成功\n")
    
    # 清理欄位名稱（移除任何殘留的 BOM）
    df.columns = [col.lstrip('\ufeff') for col in df.columns]
    
    print(f"📊 資料摘要:")
    print(f"   - 總行數: {len(df)}")
    print(f"   - 欄位數: {len(df.columns)}\n")
    
    print(f"欄位清單:")
    print("-" * 60)
    for i, col in enumerate(df.columns, 1):
        print(f"   {i:2d}. {col}")
    
    print(f"\n前 5 個活動詳細資訊:")
    print("=" * 80)
    
    # 顯示前 5 筆詳細資料
    for idx, row in df.head(5).iterrows():
        print(f"\n【活動 {idx + 1}】")
        print(f"  活動名稱： {row['Name']}")
        print(f"  活動ID：   {row['Id']}")
        print(f"  說明：     {row['Description']}")
        print(f"  參與對象： {row['Particpation']}")
        print(f"  地點：     {row['Location']}")
        print(f"  詳細地址： {row['Add']}")
        print(f"  電話：     {row['Tel']}")
        print(f"  主辦單位： {row['Org']}")
        print(f"  開始時間： {row['Start']}")
        print(f"  結束時間： {row['End']}")
        print(f"  經度：     {row['Px']:.5f}")
        print(f"  緯度：     {row['Py']:.5f}")
        print(f"  最後更新： {row['Changetime']}")
        print("-" * 80)
    
    print(f"\n📊 資料統計:")
    print("-" * 60)
    print(f"   - 唯一 ID 數: {df['Id'].nunique()}")  
    print(f"   - 所有 Status 值: {df['Status'].unique()}")
    
    # 顯示坐標範圍
    print(f"\n🗺️  地理位置範圍 (經緯度):")
    print(f"   - 經度 (Px): {df['Px'].min():.5f} ~ {df['Px'].max():.5f}")
    print(f"   - 緯度 (Py): {df['Py'].min():.5f} ~ {df['Py'].max():.5f}")
    
    # 非空欄位統計
    print(f"\n非空欄位統計:")
    print("-" * 60)
    for col in df.columns:
        non_null = df[col].notna().sum()
        pct = (non_null / len(df)) * 100
        if non_null > 0:
            print(f"   {col}: {non_null:3d} 筆 ({pct:5.1f}%)")
    
except Exception as e:
    print(f"❌ 錯誤: {type(e).__name__}: {e}")
    import traceback
    traceback.print_exc()
