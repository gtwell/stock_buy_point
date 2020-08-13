'''
Author: gtwell
Date: 2020-08-13 17:09:01
LastEditTime: 2020-08-13 19:31:42
'''
import datetime 
from chinese_calendar import is_workday
import tushare as ts
import numpy as np

np.set_printoptions(precision=3, suppress=True)

# 获得距离当日前二十一日的日期（周末，节假日剔除）
def days_of_twentyone(today_date):
    cnt = 0
    prev = today_date

    while (cnt < 20):
        if is_workday(prev):
            cnt += 1
        prev -= datetime.timedelta(days=1)
    while not is_workday(prev):
        prev -= datetime.timedelta(days=1)
        
    return prev.strftime('%Y-%m-%d'), today_date.strftime('%Y-%m-%d')

# 分析是否是买点，五日均线向上穿越二十日线，为买点
def buy_point_info(data):
    buy_point = False
    close_data = data['close']
    today_five_mean = np.mean(close_data[:5])
    today_twenty_mean = np.mean(close_data[:20])

    yest_five_mean = np.mean(close_data[1:6])
    yest_twenty_mean = np.mean(close_data[1:21])

    if ((today_five_mean / today_twenty_mean) > 1.001) and ((yest_five_mean / yest_twenty_mean) < 0.999):
        buy_point = True
        
    return buy_point, today_five_mean, today_twenty_mean, yest_five_mean, yest_twenty_mean

if __name__ == '__main__':
    twentyone_days_ago, now = days_of_twentyone(datetime.datetime.now())
    print(twentyone_days_ago)
    print(now)

    bonds_info = ts.get_hs300s()
    bonds_code = bonds_info["code"]

    print(bonds_code)

    # bonds_code = ["000625", "002739"]
    f = open('20200813.txt','w')

    for i, code in enumerate(bonds_code):
        data = ts.get_hist_data(code, start=twentyone_days_ago, end=now)
        is_buy_point, today_five_mean, today_twenty_mean, yest_five_mean, yest_twenty_mean = buy_point_info(data)
        if is_buy_point:
            print(data)
            print(code, bonds_info["name"][i], "今5日均线:", today_five_mean, "今20日均线:", today_twenty_mean, "昨5日均线:", yest_five_mean, "昨20日均线:", yest_twenty_mean, file=f)
            
    f.close()