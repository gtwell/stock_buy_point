<!--
 * @Author: gtwell
 * @Date: 2020-10-08 18:01:26
 * @LastEditTime: 2021-01-31 23:44:27
-->
从沪深300和中证500寻找股票买点，**机构重仓150和北上资金前50**优先   
买点确定：**5日均线向上穿20日均线**   
`fly_bs.py`: `baostock`库接口获取股票信息   
`fly_ts.py`: `tushare`库接口获取股票信息   
每日运行一次可得到代码和股票名字  

[实盘交易链接(周更)](https://www.yuque.com/gtwell/freedom)  

----2020-09-05----   
更新机构重仓150支股票，并将每天生成的结果分成每个文件夹，便于管理   
----2020-09-17----   
更新买点，当日前三日**5日均线均处于20日均线下方**，当日**5日均线向上穿20日均线**  
----2020-11-01----   
更新机构重仓150支股票和北上重仓50支股票   
----2020-12-03----   
新增运行完后自动发送结果至邮箱，`send_email`参数设定为`True`为开启;  
----2021-01-05----   
更新北上重仓50支股票   
----2021-01-31----  
更新机构重仓150支股票 


### 参考
机构重仓150和北上50数据来自搬砖小组