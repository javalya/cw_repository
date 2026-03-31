import tushare as ts
import os
from datetime import datetime, timedelta

# 从环境变量获取 Tushare Token
# 使用前需要设置: export TUSHARE_TOKEN="your_token"
TOKEN = os.environ.get('TUSHARE_TOKEN', '')

if not TOKEN:
    print("⚠️  请先设置 TUSHARE_TOKEN 环境变量")
    print("获取方式: https://tushare.pro/register")
    exit(1)

# 初始化 Tushare Pro
pro = ts.pro_api(TOKEN)

print("=" * 50)
print("📊 A股指数行情获取演示")
print("=" * 50)

# 获取今日日期
today = datetime.now().strftime('%Y%m%d')

# 1. 获取上证指数日线数据
print("\n📈 上证指数 (000001.SH)")
print("-" * 50)
try:
    df = pro.index_daily(ts_code='000001.SH', start_date=today, end_date=today)
    if not df.empty:
        row = df.iloc[0]
        print(f"日期: {row['trade_date']}")
        print(f"开盘: {row['open']:.2f}")
        print(f"收盘: {row['close']:.2f}")
        print(f"涨跌: {row['pct_chg']:.2f}%")
        print(f"成交量: {row['vol'] / 10000:.2f}万手")
    else:
        print("今日数据暂未更新")
except Exception as e:
    print(f"获取失败: {e}")

# 2. 获取深证成指
print("\n📈 深证成指 (399001.SZ)")
print("-" * 50)
try:
    df = pro.index_daily(ts_code='399001.SZ', start_date=today, end_date=today)
    if not df.empty:
        row = df.iloc[0]
        print(f"日期: {row['trade_date']}")
        print(f"收盘: {row['close']:.2f}")
        print(f"涨跌: {row['pct_chg']:.2f}%")
    else:
        print("今日数据暂未更新")
except Exception as e:
    print(f"获取失败: {e}")

# 3. 获取创业板指数
print("\n📈 创业板指 (399006.SZ)")
print("-" * 50)
try:
    df = pro.index_daily(ts_code='399006.SZ', start_date=today, end_date=today)
    if not df.empty:
        row = df.iloc[0]
        print(f"日期: {row['trade_date']}")
        print(f"收盘: {row['close']:.2f}")
        print(f"涨跌: {row['pct_chg']:.2f}%")
    else:
        print("今日数据暂未更新")
except Exception as e:
    print(f"获取失败: {e}")

print("\n" + "=" * 50)
print("✅ 演示完成")
print("=" * 50)
