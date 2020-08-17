import baostock as bs
import pandas as pd
import datetime 
from chinese_calendar import is_workday
import numpy as np

# 机构重仓
Institutions148 = ['长电科技', '卫宁健康', '东山精密', '上海机场', '中炬高新', '沃森生物', '潍柴动力', '华测检测', '健帆生物', '中国建筑',
                   '汇川技术', '冀东水泥', '天坛生物', '康泰生物', '美年健康', '药明康德', '三七互娱', '智飞生物', '益丰药房', '歌尔股份',
                   '北方华创', '海螺水泥', '爱尔眼科', '华域汽车', '先导智能', '光环新网', '上汽集团', '南极电商', '华天科技', '深南电路',
                   '东方雨虹', '三安光电', '永辉超市', '太阳纸业', '生物股份', '圣邦股份', '中国中免', '泰格医药', '浪潮信息', '格力电器',
                   '宁德时代', '海大集团', '普洛药业', '中国中车', '中国铁建', '洋河股份', '中国神华', '用友网络', '兆易创新', '立讯精密',
                   '海康威视', '山西汾酒', '晨光文具', '海天味业', '顺网科技', '生益科技', '晶方科技', '东华软件', '海尔智家', '迈瑞医疗',
                   '科大讯飞', '山东药玻', '牧原股份', '洽洽食品', '通策医疗', '美亚柏科', '安井食品', '韦尔股份', '中航光电', '分众传媒',
                   '芒果超媒', '长春高新', '美的集团', '温氏股份', '中国石化', '复星医药', '绝味食品', '山东黄金', '三一重工', '闻泰科技',
                   '北新建材', '万华化学', '顺鑫农业', '华兰生物', '我武生物', '光威复材', '通威股份', '扬农化工', '华鲁恒升', '双汇发展',
                   '赣锋锂业', '中公教育', '国瓷材料', '烽火通信', '沪电股份', '中科曙光', '紫金矿业', '京沪高铁', '亿联网络', '中信特钢',
                   '宇通客车', '长江电力', '金风科技', '宋城演艺', '东方财富', '隆基股份', '乐普医疗', '古井贡酒', '安图生物', '壹网壹创',
                   '恒立液压', '伊利股份', '金山办公', '中环股份', '视源股份', '国电南瑞', '顺丰控股', '启明星辰', '金域医学', '完美世界',
                   '贵州茅台', '汇顶科技', '信维通信', '高德红外', '中国软件', '中顺洁柔', '亿纬锂能', '泸州老窖', '恒生电子', '康弘药业',
                   '比亚迪', '健友股份', '三花智控', '中兴通讯', '恒瑞医药', '深信服', '吉比特', '大参林', '新希望', '家家悦',
                   '凯莱英', '广联达', '五粮液', '欣旺达', '老百姓',   '苏泊尔', '京东方A', '卓胜微']

# 北上资金前50
North50 = ['牧原股份', '顺丰控股', '韦尔股份', '潍柴动力', '三七互娱', '隆基股份', '宁德时代', '东方雨虹', '华兰生物', '国电南瑞',
           '药明康德', '生物股份', '三一重工', '迈瑞医疗', '立讯精密', '汇川技术', '保利地产', '泰格医药', '恒生电子', '中信证券',
           '恒立液压', '海天味业', '海康威视', '美的集团', '伊利股份', '贵州茅台', '长江电力', '招商银行', '华测检测', '万华化学',
           '工商银行', '分众传媒', '格力电器', '中国平安', '方正证券', '恒瑞医药', '云南白药', '上海机场', '海螺水泥', '上汽集团',
           '平安银行', '海尔智家', '万科A', '五粮液', '广联达', '洋河股份', '中国中免', '兴业银行', '爱尔眼科', '京东方A']

ZiXuan = ['同花顺', '美亚光电', '大华股份', '宝信软件', '中科创达', '福耀玻璃', '中信建投', '上海新阳', '苏州固锝', '老板电器', '上海贝岭']

# 北上前50 + 机构重仓集合
Ins148_North50 = list(set(Institutions148 + North50 + ZiXuan)) # 158
# print(len(Ins148_North50))

def get_all_data():
    # 获取沪深300和中证500成分股
    rs_all = bs.query_all_stock(day="2020-06-30")
    print('query_all error_code:' + rs_all.error_code)
    print('query_all  error_msg:' + rs_all.error_msg)

    # 打印结果集
    all_stocks = []
    while (rs_all.error_code == '0') & rs_all.next():
        # 获取一条记录，将记录合并在一起
        all_stocks.append(rs_all.get_row_data())

    stocks_result = pd.DataFrame(all_stocks, columns=rs_all.fields)

    # stocks_result.to_csv("./all_stocks.csv", encoding="gbk", index=False)
    return stocks_result

def get_ins148_north50_data():
    # 获取沪深300和中证500成分股
    rs_all = bs.query_all_stock("2020-06-30")
    print('query_all error_code:' + rs_all.error_code)
    print('query_all  error_msg:' + rs_all.error_msg)

    # 打印结果集
    all_stocks = []
    while (rs_all.error_code == '0') & rs_all.next():
        # 获取一条记录，将记录合并在一起
        code_info = rs_all.get_row_data()
        if code_info[2] in Ins148_North50:
            all_stocks.append(code_info)

    stocks_result = pd.DataFrame(all_stocks, columns=rs_all.fields)

    # stocks_result.to_csv("./ins148_north50_stocks.csv", encoding="gbk", index=False)
    return stocks_result

# 沪深300 + 中证500
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

    data = get_ins148_north50_data()
    print(data)
    # data = pd.read_csv("./all_stocks.csv", encoding='gbk')
    print(data['code_name'].values.tolist())
    # for i in Institutions148:
    #     if i not in data['code_name'].values.tolist():
    #         print(i)

    #### 登出系统 ####
    bs.logout()