'''
Author: gtwell
Date: 2020-08-13 17:09:01
LastEditTime: 2020-10-31 16:40:19
'''
import baostock as bs
import pandas as pd
import datetime 
from chinese_calendar import is_workday
import numpy as np
from get_stocks import get_better_stocks, get_hs300_zz500_data
from tqdm import tqdm
import os

np.set_printoptions(precision=3, suppress=True)

# 获得距离当日前五十日的日期（周末，节假日剔除）
def days_of_twentyone(today_date):
    cnt = 0
    prev = today_date

    while (cnt < 50):
        if is_workday(prev):
            cnt += 1
        prev -= datetime.timedelta(days=1)
    while not is_workday(prev):
        prev -= datetime.timedelta(days=1)
        
    return prev.strftime('%Y-%m-%d'), today_date.strftime('%Y-%m-%d')

# 分析是否是买点，五日均线向上穿越二十日线，为买点
def buy_point_info(data):
    buy_point = False
    low_level = False
    close_data = data['close'].astype('float')
    today_five_mean = np.mean(close_data[-5:])
    today_twenty_mean = np.mean(close_data[-20:])

    yest0_five_mean = np.mean(close_data[-6:-1])
    yest0_twenty_mean = np.mean(close_data[-21:-1])

    yest1_five_mean = np.mean(close_data[-7:-2])
    yest1_twenty_mean = np.mean(close_data[-22:-2])

    yest2_five_mean = np.mean(close_data[-8:-3])
    yest2_twenty_mean = np.mean(close_data[-23:-3])

    if ((today_five_mean / today_twenty_mean) > 1.000) and \
        ((yest0_five_mean / yest0_twenty_mean) < 1.000) and \
        ((yest1_five_mean / yest1_twenty_mean) < 1.000) and \
        ((yest2_five_mean / yest2_twenty_mean) < 1.000):
        buy_point = True

    if (today_five_mean < today_twenty_mean):
        low_level = True
        
    return buy_point, np.array([today_five_mean, today_twenty_mean, yest0_five_mean, yest0_twenty_mean]), low_level

def get_hist_data(code, start, end):
    rs_stock_info = bs.query_history_k_data_plus(code,
        "date,code,open,high,low,close,preclose,volume,amount,adjustflag,turn,tradestatus,pctChg,isST",
        start_date=start, end_date=end,
        frequency="d", adjustflag="2")

    # print('query_history_k_data_plus respond error_code:'+rs_stock_info.error_code)
    # print('query_history_k_data_plus respond  error_msg:'+rs_stock_info.error_msg)

    #### 打印结果集 ####
    data_list = []
    while (rs_stock_info.error_code == '0') & rs_stock_info.next():
        # 获取一条记录，将记录合并在一起
        data_list.append(rs_stock_info.get_row_data())
    rs_stock_info_result = pd.DataFrame(data_list, columns=rs_stock_info.fields)

    return rs_stock_info_result

if __name__ == '__main__':
    #### 登陆系统 ####
    lg = bs.login()
    # 显示登陆返回信息
    print('login respond error_code:'+lg.error_code)
    print('login respond  error_msg:'+lg.error_msg)

    twentyone_days_ago, now = days_of_twentyone(datetime.datetime.now())

    if not os.path.exists(now.replace("-", "/")):
        os.makedirs(now.replace("-", "/"))

    # 机构重仓 + 北上50 + 隐形冠军 + 自选
    stocks_result = get_better_stocks() # get_hs300_zz500_data(), get_better_stocks()
    bonds_code = stocks_result['code']
    f = open(os.path.join(now.replace("-", "/"), '精选-buy-{}.txt'.format(now)), 'w')

    for i in tqdm(range(len(bonds_code)), ncols=80):
        data = get_hist_data(bonds_code[i], start=twentyone_days_ago, end=now)
        is_buy_point, mean_info, _ = buy_point_info(data)
        close_data = data['close'].astype('float').values.tolist()[-1] # 当日收盘价
        if is_buy_point and close_data < 200:
            print(bonds_code[i], stocks_result["code_name"][i], "收盘价:", close_data, file=f)          
        # if is_buy_point:
        #     print(np.mean(data['close'][-20:].astype('float').values))
        #     print(bonds_code[i], stocks_result["code_name"][i],
        #         "今收:", data['close'].astype('float').values.tolist()[-1],
        #         "今5日均线:", np.around(mean_info[0], decimals=2),
        #         "今20日均线:", np.around(mean_info[1], decimals=2),
        #         "昨5日均线:", np.around(mean_info[2], decimals=2),
        #         "昨20日均线:", np.around(mean_info[3], decimals=2),
        #         file=f)  
    f.close()

    # hs300 + zz500
    stocks_result = get_hs300_zz500_data() # get_hs300_zz500_data(), get_ins148_north50_data()
    # bonds_code = ["000625", "002739"]
    bonds_code = stocks_result['code']
    f = open(os.path.join(now.replace("-", "/"), 'hs300-zz500-buy-{}.txt'.format(now)), 'w')

    for i in tqdm(range(len(bonds_code)), ncols=80):
        data = get_hist_data(bonds_code[i], start=twentyone_days_ago, end=now)
        is_buy_point, mean_info, _ = buy_point_info(data)
        close_data = data['close'].astype('float').values.tolist()[-1] # 当日收盘价
        if is_buy_point and close_data < 200:
            print(bonds_code[i], stocks_result["code_name"][i], "收盘价:", close_data, file=f)           
    f.close()

    #### 登出系统 ####
    bs.logout()


# if __name__ == '__main__':
#     #### 登陆系统 ####
#     lg = bs.login()
#     # 显示登陆返回信息
#     print('login respond error_code:'+lg.error_code)
#     print('login respond  error_msg:'+lg.error_msg)

#     twentyone_days_ago, now = days_of_twentyone(datetime.datetime.now())
#     stocks_result = get_ins148_north50_data()  # get_hs300_zz500_data(), get_ins148_north50_data()

#     # bonds_code = ["000625", "002739"]
#     cnt = 0
#     bonds_code = stocks_result['code']

#     for i, code in enumerate(bonds_code):
#         data = get_hist_data(code, start=twentyone_days_ago, end=now)
#         _, mean_info, low_level = buy_point_info(data)
#         if low_level:
#             cnt += 1
#             print(code, stocks_result["code_name"][i])

#     print("股票池有：{}支股票".format(len(bonds_code)))
#     print("5日均线低于20日均线股票有：{}支".format(cnt))
#     #### 登出系统 ####
#     bs.logout()