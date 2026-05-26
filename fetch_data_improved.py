import sys

from app import DATA_URL, build_stats, fetch_data, records_from_df

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")


def display_range(range_info):
    start = range_info.get('min') or '---'
    end = range_info.get('max') or '---'
    return f"{start} ~ {end}"


print("📥 正在下載資料...\n")
print(f"資料網址： {DATA_URL}\n")

df, error = fetch_data()
if error:
    print(f"❌ 錯誤: {error}")
    sys.exit(1)

stats = build_stats(df)
records = records_from_df(df)

print("✓ 資料讀取成功\n")

print("📊 資料摘要:")
print(f"   - 總筆數: {stats['total_rows']}")
print(f"   - 欄位數: {stats['total_columns']}")
print(f"   - 發布單位數: {stats['unique_authors']}")
print(f"   - 類型數: {len(stats['type_values'])}")
print(f"   - 活動日期: {display_range(stats['startdate_range'])}")
print(f"   - 發布日期: {display_range(stats['pubdate_range'])}\n")

print("欄位清單:")
print("-" * 60)
for index, column in enumerate(stats['columns'], 1):
    print(f"   {index:2d}. {column}")

print("\n資料類型:")
print("-" * 60)
for type_name in stats['type_values']:
    print(f"   - {type_name}")

print("\n前 5 筆資料:")
print("=" * 80)
for index, row in enumerate(records[:5], 1):
    print(f"\n【資料 {index}】")
    print(f"  標題：     {row.get('title') or '---'}")
    print(f"  類型：     {row.get('type') or '---'}")
    print(f"  發布單位： {row.get('author') or '---'}")
    print(f"  活動日期： {row.get('startdate') or '---'} ~ {row.get('enddate') or '---'}")
    print(f"  發布日期： {row.get('pubdate') or '---'}")
    print(f"  連結：     {row.get('link') or '---'}")
    print(f"  說明：     {(row.get('description') or '---')[:160]}")
    print("-" * 80)
