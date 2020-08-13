'''
Author: gtwell
Date: 2020-08-13 17:09:01
LastEditTime: 2020-08-13 19:31:42
'''
import baostock as bs
import pandas as pd
import datetime 
from chinese_calendar import is_workday
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
    close_data = data['close'].astype('float')
    today_five_mean = np.mean(close_data[-5:])
    today_twenty_mean = np.mean(close_data[-20:])

    yest_five_mean = np.mean(close_data[-6:-1])
    yest_twenty_mean = np.mean(close_data[-21:-1])

    if ((today_five_mean / today_twenty_mean) > 1.001) and ((yest_five_mean / yest_twenty_mean) < 0.999):
        buy_point = True
        
    return buy_point, np.array([today_five_mean, today_twenty_mean, yest_five_mean, yest_twenty_mean])

def get_hist_data(code, start, end):
    rs_stock_info = bs.query_history_k_data_plus(code,
        "date,code,open,high,low,close,preclose,volume,amount,adjustflag,turn,tradestatus,pctChg,isST",
        start_date=start, end_date=end,
        frequency="d", adjustflag="3")

    # print('query_history_k_data_plus respond error_code:'+rs_stock_info.error_code)
    # print('query_history_k_data_plus respond  error_msg:'+rs_stock_info.error_msg)

    #### 打印结果集 ####
    data_list = []
    while (rs_stock_info.error_code == '0') & rs_stock_info.next():
        # 获取一条记录，将记录合并在一起
        data_list.append(rs_stock_info.get_row_data())
    rs_stock_info_result = pd.DataFrame(data_list, columns=rs_stock_info.fields)

    return rs_stock_info_result

# 获取沪深A股历史K线数据 
# 详细指标参数，参见“历史行情指标参数”章节；“分钟线”参数与“日线”参数不同。
# 分钟线指标：date,time,code,open,high,low,close,volume,amount,adjustflag
def get_hs300_zz500_data():
    # 获取沪深300和中证500成分股
    rs_hs300 = bs.query_hs300_stocks()
    rs_zz500 = bs.query_zz500_stocks()
    print('query_hs300 error_code:' + rs_hs300.error_code)
    print('query_hs300  error_msg:' + rs_hs300.error_msg)
    print('query_zz500 error_code:' + rs_zz500.error_code)
    print('query_zz500  error_msg:' + rs_zz500.error_msg)

    # 打印结果集
    hs300_stocks = []
    zz500_stocks = []
    while (rs_hs300.error_code == '0') & rs_hs300.next():
        # 获取一条记录，将记录合并在一起
        hs300_stocks.append(rs_hs300.get_row_data())
    while (rs_zz500.error_code == '0') & rs_zz500.next():
        # 获取一条记录，将记录合并在一起
        zz500_stocks.append(rs_zz500.get_row_data())

    stocks_result = pd.DataFrame(hs300_stocks+zz500_stocks, columns=rs_hs300.fields)

    # stocks_result.to_csv("./hs300_zz500_stocks.csv", encoding="gbk", index=False)

    return stocks_result

if __name__ == '__main__':
    #### 登陆系统 ####
    lg = bs.login()
    # 显示登陆返回信息
    print('login respond error_code:'+lg.error_code)
    print('login respond  error_msg:'+lg.error_msg)

    twentyone_days_ago, now = days_of_twentyone(datetime.datetime.now())
    stocks_result = get_hs300_zz500_data()

    # bonds_code = ["000625", "002739"]
    bonds_code = stocks_result['code']
    f = open('20200813.txt','w')

    for i, code in enumerate(bonds_code):
        data = get_hist_data(code, start=twentyone_days_ago, end=now)
        is_buy_point, mean_info = buy_point_info(data)
        if is_buy_point:
            print(code, stocks_result["code_name"][i],
                "今5日均线:", np.array([mean_info[0]]),
                "今20日均线:", np.array([mean_info[1]]),
                "昨5日均线:", np.array([mean_info[2]]),
                "昨20日均线:", np.array([mean_info[3]]),
                file=f)
            
    f.close()

    #### 登出系统 ####
    bs.logout()