"""
author: tianxu

description:
  通过baostock库获取股票等财经信息
"""

import logging
import csv
import os
import atexit
import signal
from enum import IntEnum, auto
from datetime import datetime, timedelta

import baostock as bs
import pandas as pd

from QuantDataCollector.abstract_data_collector import AbstractDataCollector
from QuantDataCollector.abstract_data_collector import DataCollectorError
from QuantDataCollector.data_collector_config import cache_config, log_config, default_config

from QuantDataCollector.cache_util.cache_util import CacheUtil
from QuantDataCollector.cache_util.cache_util_config import log_config

from QuantDataCollector.Utils.file_utils import mkdir
from QuantDataCollector.Utils.utils import get_date, date_decrease
from QuantDataCollector.Global.settings import LOGGING_FILE_DIR, LOGGING_FILE_NAME

from QuantDataCollector.type import RequestFrequency, AdjustFlag

frequency2fields= {
    RequestFrequency.MonthK: "date,code,open,high,low,close,volume,amount,adjustflag,turn,pctChg",
    RequestFrequency.WeekK: "date,code,open,high,low,close,volume,amount,adjustflag,turn,pctChg",
    RequestFrequency.DayK: "date,code,open,high,low,close,preclose,volume,amount,adjustflag,turn,tradestatus,pctChg,peTTM, psTTM,pcfNcfTTM,pbMRQ,isST",
    RequestFrequency.FiveMinutsK: "date,time,code,open,high,low,close,volume,amount,adjustflag",
    RequestFrequency.FifteenMinutsK: "date,time,code,open,high,low,close,volume,amount,adjustflag",
    RequestFrequency.ThirtyMinutsK: "date,time,code,open,high,low,close,volume,amount,adjustflag",
    RequestFrequency.HourK: "date,time,code,open,high,low,close,volume,amount,adjustflag"
}
frequency2keys =  {
    RequestFrequency.MonthK: ["date", "code", "open", "high", "low", "close", 
          "volume", "amount", "adjustflag", "turn", "pctChg"],
    RequestFrequency.WeekK: ["date", "code", "open", "high", "low", "close", 
          "volume", "amount", "adjustflag", "turn", "pctChg"],
    RequestFrequency.DayK: ["date", "code", "open", "high", "low", "close", 
          "preclose", "volume", "amount", "adjustflag", "turn", "tradestatus", "pctChg", 
          "peTTM", "psTTM", "pcfNcfTTM", "pbMRQ","isST"],
    RequestFrequency.FiveMinutsK: ["date", "time", "code", "open", "high", "low", "close", 
          "volume", "amount", "adjustflag"],
    RequestFrequency.FifteenMinutsK: ["date", "time", "code", "open", "high", "low", "close", 
          "volume", "amount", "adjustflag"],
    RequestFrequency.ThirtyMinutsK: ["date", "time", "code", "open", "high", "low", "close", 
          "volume", "amount", "adjustflag"],
    RequestFrequency.HourK: ["date", "time", "code", "open", "high", "low", "close", 
          "volume", "amount", "adjustflag"],
}


"""
------------------------------------------ 枚举类 --------------------------------------------

baostock库返回的数据结构基本都是pandas的DataFrame，本文件列出baostock各接口返回的DataFrame中，列对应的数据是什么。
"""

STOCK_TYPE_SHARE = '1'
"""baostock库中STOCK类型中，1代表股票"""
STOCK_TYPE_INDEX = '2'
"""baostock库中STOCK类型中，2代表指数"""
STOCK_TYPE_OTHER = '3'
"""baostock库中STOCK类型中，3代表其他"""

class ALL_STOCK(IntEnum):
    """
    baostock.query_all_stock接口返回的DataFrame数据对应的结构，原始结构如下：

    |-----------|-------------|--------------|
    |   code    | tradeStatus |   code_name  |
    | sh.000001 |      1      | 上证综合指数 |
    |-----------|-------------|--------------|
    """
    code = 0 # 证券代码
    tradeStatus = 1 # 交易状态（1: 正常交易 0:停牌）
    code_name = 2 # 证券名称

class STOCK_BASIC(IntEnum):
    """
    baostock.query_stock_basic接口返回的DataFrame数据对应的结构，原始结构如下：

    |-----------|-----------|------------|---------|------|--------|
    |   code    | code_name |   ipoDate  | outDate | type | status |
    | sh.600000 |  浦发银行 | 1999-11-10 |         |  1   |   1    |
    |-----------|-----------|------------|---------|------|--------|
    
    """
    code = 0 # 证券代码
    code_name = 1 # 证券名称
    ipoDate = auto() # 首次公开募股日期
    outDate = auto() # 退市日期
    type = auto() # 证券类型（1:股票 2:指数 3:其他）
    status = auto() # 上市状态（1: 上市 2: 退市）

class BaostockError(Exception):
    """baostock专用异常"""
    pass

class BaostockDataCollector(AbstractDataCollector):
    __login = False
    __config = {}

    def __init__(self, config_dict = default_config):
        self.__config = config_dict
        signal.signal(signal.SIGINT, self.signal_exit)
        atexit.register(self.cleanUp)
        if "log" in config_dict:
            self.__config_logging(int(config_dict["log"]))
        else:
            self.__config_logging()

        self.__cache_util = None
        if "cache" in config_dict:
            try:
                self.__cache_util = CacheUtil(config_dict = config_dict)
            except Exception as e:
                self.__cache_util = None
                self.__logger.error("Instantiate CacheUtil failed, error: " + str(e))

        lg = bs.login()
        if lg.error_code == '0':
            self.__login = True
        else:
            print("baostock 登陆失败")
            self.__logger.critical("baostock 登陆失败")
            exit()

    def __del__(self):
        if (self.__login):
            try:
                lg = bs.logout()
            except Exception as e:
                self.__logger.warning("__del__: logout 出错，" + str(e))
            else:
                if (lg.error_code == 0):
                    self.__login = False
                else:
                    self.__logger.warning("__del__: logout 出错")

    def signal_exit(self,signum,frame):
        self.__logger.info("my_exit: interrupted by ctrl+c")
        self.cleanUp()
        exit()

    def cleanUp(self):
        # baostock实现有问题，在析构函数中调用会报错
        if (self.__login):
            try:
                lg = bs.logout()
            except Exception as e:
                self.__logger.warning("cleanUp: logout 出错，" + str(e))
            else:
                if (lg.error_code == 0):
                    self.__login = False
                else:
                    self.__logger.warning("cleanUp: logout 出错")

    def __config_logging(self, level = logging.WARNING):
        if level == logging.DEBUG:
            print("================= data collector info ==================")
            print(self.get_data_collector_info())
            print("================= end of collector info ==================")
        self.__logger = logging.getLogger('baostock_data_collector')
        
        if not os.path.exists(LOGGING_FILE_DIR):
            mkdir(LOGGING_FILE_DIR)
        ch = logging.FileHandler(LOGGING_FILE_NAME)
        formatter = logging.Formatter(fmt='%(asctime)s.%(msecs)03d - %(name)s - %(levelname)s - %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
        ch.setFormatter(formatter)
        self.__logger.addHandler(ch)
        self.__logger.setLevel(level)

    def get_all_stock_code(self, day = None):
        """获取所有证券代码(包括股票、指数和其他)
        
        获取交易日day时，股市上所有证券代码，包括股票、指数和其他。

        Args:
          day: String，交易日，如果不是交易日，会导致失败。可省略，默认为离今天最近的交易日。

        Returns:
          Number: 错误码，0表示成功，否则表示失败，1表示非交易日
          list: 内容为表示证券代码的字符串

        Raises:
          DataCollectorError:
        """
        if not self.__login:
            self.__logger.error("get_all_stock_code: baostock未登陆")
            raise DataCollectorError("you dont't login.")
        
        result = []
        
        if not self.is_trade_day(day):
            self.__logger.warning("get_all_stock_code: 输入日期不是交易日")
            day = self.get_recent_trade_day(day)

        rs = bs.query_all_stock(day=day) # 获取证券信息
        
        if rs.error_code != '0':
            self.__logger.error("get_all_stock_code: baostock query_all_stock函数调用失败")
            return int(rs.error_code), []
        
        while (rs.error_code == '0') & rs.next(): # 获取每个股票的历史k线数据
            try:
                code = rs.get_row_data()[ALL_STOCK.code]
            except Exception as e:
                self.__logger.error("get_all_stock_code: index错误")
                raise DataCollectorError("index error")

            result.append(code)

        return 0, result

    def get_all_share_code(self, day = None):
        """获取所有股票代码
        
        获取交易日day时，股市上所有股票代码，不包括指数和其他。

        Args:
          day: String，交易日，如果不是交易日，会导致失败。可省略，默认为离今天最近的交易日。

        Returns:
          Number: 错误码，0表示成功，否则表示失败，1表示非交易日
          list: 内容为表示股票代码的字符串

        Raises:
          DataCollectorError:
        """
        if not self.__login:
            self.__logger.error("get_all_share_code: baostock未登陆")
            raise DataCollectorError("you dont't login.")


        if not self.is_trade_day(day):
            self.__logger.warning("get_all_share_code: 输入日期不是交易日")
            day = self.get_recent_trade_day(day)

        rs = bs.query_all_stock(day=day) # 获取证券信息
        
        if rs.error_code != '0':
            self.__logger.error("get_all_stock_code: baostock query_all_stock函数调用失败")
            return int(rs.error_code), []
        
        result = []
        while (rs.error_code == '0') & rs.next(): # 获取每个股票的历史k线数据
            try:
                code = rs.get_row_data()[ALL_STOCK.code]
            except Exception as e:
                self.__logger.error("get_all_stock_code: index错误")
                raise DataCollectorError("index error")
            if self.__is_share(code):
                self.__logger.info("get_all_stock_code: {} is share".format(code))
                result.append(code)
            else:
                self.__logger.info("get_all_stock_code: {} is not share".format(code))
        return 0, result

    def __is_share(self, stock_code):
        """判断指定代码是否为股票"""
        err_code, basic_data = self.get_stock_basic_data(stock_code)
        if err_code == 0:
            try:
                is_share = basic_data["type"] == "1"
            except:
                return False
            if is_share:
                self.__logger.info("__is_share: {} is a share".format(stock_code))
            else:
                self.__logger.info("__is_share: {} is not a share".format(stock_code))
            return is_share

        self.__logger.info("__is_share: {} get stock basic data failed".format(stock_code))
        return False

    def get_stock_basic_data(self, stock_code):
        """获取某证券的基本信息

        通过stock_code指定某证券，获取该股票的基本信息。主要包括：名称、上市日期、退市日期、证券类型、上市状态

        Args:
          stock_code: String，证券代码，比如"sh.600000"

        Returns:
          Number: 错误码，0表示获取成功
          dict: 字典

        Raises:
          DataCollectorError
        """
        if self.__has_stock_basic_cache(stock_code):
            self.__logger.info("get_stock_basic_data: 从缓存读取数据")
            return self.__get_stock_basic_data_from_local_cache(stock_code)
        else:
            self.__logger.info("get_stock_basic_data: 从线上读取数据")
            return self.__get_stock_basic_data_from_online(stock_code)

    def __has_stock_basic_cache(self, stock_code):
        if not self.__cache_util:
            return False
        return self.__cache_util.has_stock_basic_cache(stock_code)

    def __get_stock_basic_data_from_local_cache(self, stock_code):
        if not self.__cache_util:
            return -1, {}
        basic_stock_data = self.__cache_util.get_stock_basic_data(stock_code)
        if self.__verify_basic_data_cache(basic_stock_data):
            return 0, basic_stock_data
        else:
            return -1, {}

    def __verify_basic_data_cache(self, local_data_from_cache):
        """验证cache中basic data结构的正确性"""
        try:
            tmp = local_data_from_cache["code"];
            tmp = local_data_from_cache["code_name"];
            tmp = local_data_from_cache["ipoDate"];
            tmp = local_data_from_cache["outDate"];
            tmp = local_data_from_cache["type"];
            tmp = local_data_from_cache["status"];
        except:
            return False
        return True

    def __get_stock_basic_data_from_online(self, stock_code):
        if not self.__login:
            self.__logger.error("__get_stock_basic_data_from_online: baostock未登陆")
            raise DataCollectorError("you dont't login.")

        rs_b = bs.query_stock_basic(code=stock_code)
        if rs_b.error_code != '0':
            self.__logger.error("__get_stock_basic_data_from_online: baostock query_stock_basic调用失败")
            return int(rs_b.error_code), {}
        
        stock_basic_data = rs_b.get_row_data()
        keys = ["code", "code_name", "ipoDate", "outDate", "type", "status"]
        dicts = {}
        for i in range(len(stock_basic_data)):
            dicts[keys[i]] = stock_basic_data[i]

        # 保存在本地
        if self.__cache_util:
            try:
                self.__cache_util.save_stock_basic_data(stock_code, dicts)
            except Exception as e:
                self.__logger.warning("__get_stock_basic_data_from_online: 写cache失败, err: " + str(e))

        return 0, dicts

    def get_stock_type(self, stock_code):
        """获取证券类型

        获取code对应证券的类型

        Args:
          stock_code: String，证券代码，比如"sh.600000"

        Returns:
          Number: 错误码，0表示成功，否则表示失败
          String:
            '1'表示股票
            '2'表示指数
            '3'表示其他

        Raises:
          DataCollectorError
        """
        error_code, stock_basic_data = self.get_stock_basic_data(stock_code)
        if error_code != 0 or not stock_basic_data:
            self.__logger.error("get_stock_type: get_stock_basic_data失败")
            return error_code, '0'
        
        try:
            result = stock_basic_data["type"]
        except Exception as e:
            self.__logger.error("get_stock_type: index错误, dict is %s", stock_basic_data)
            raise DataCollectorError("index error")
        else:
            return 0, result

    def get_stock_data_period(self, stock_code_list, start=None, end=None, frequency=RequestFrequency.DayK, adjust_flag=AdjustFlag.NoAdjust):
        """获取某股票一段时期内的数据
        
        获取股票代码为stock_code的股票，从startDay到endDay的数据，主要OHLC、成交量、成交额、换手率、市盈、市净、市销等
        
        Args:
          stock_code: String，证券代码，比如"sh.600000"
          start: 以字符串形式表示的日期，比如'2008-1-1'，默认为ipo日期
          end: 以字符串形式表示的日期，比如'2008-1-1'。默认为最新交易日
          
        Returns:
          Number: 错误码，0表示获取成功
          dict: 每个日期一个key，对应value为字典

        Raises:
          DataCollectorError:

        --------------------------------------------------------
        Override Notes:
          不限实现方式，为了性能，最好存储在数据库或者本地缓存
        """
        res = {}
        if not start:
            self.__logger.info("get_stock_data_period: 未输入起始日期")
            try:
                start = stock_basic_data["ipoDate"]
            except:
                return -1, res
        
        if not end:
            self.__logger.info("get_stock_data_period: 未输入结束日期")
            try:
                end = self.get_recent_trade_day()
            except:
                return -1, res
        for stock_code in stock_code_list:
            _, stock_basic_data = self.get_stock_basic_data(stock_code)
            if len(stock_basic_data) == 0:
                res[stock_code] = None
                continue
            
            if self.__has_local_cache_data(stock_code, start, end):
                self.__logger.info("get_stock_data_period: 从缓存读取数据")
                _, res[stock_code] = self.__get_stock_data_from_local_cache_period(stock_code, start, end, frequency)
            else:
                self.__logger.info("get_stock_data_period: 从线上读取数据")
                _, res[stock_code] = self.__get_stock_data_from_online_period(stock_code, start, end, frequency, adjust_flag)
        return 0, res

    def get_stock_data(self, stock_code_list, day=None, frequency=RequestFrequency.DayK, adjust_flag=AdjustFlag.NoAdjust):
        """获取某股票某个交易日的数据
        
        获取股票代码为stock_code的股票，在交易日day的数据，主要OHLC、成交量、成交额、换手率、市盈、市净、市销等
        
        Args:
          stock_code: String，证券代码，比如"sh.600000"
          day: 以字符串形式表示的日期，比如'2008-1-1'。默认为最新交易日
          
        Returns:
          Number: 错误码，0表示获取成功
          pandas DataFrame: 至少应该包括以下17列:date,code,status,ipoDate,code_name,open,high,low,close,preclose,volume,amount,adjustflag,turn,tradestatus,pctChg,isST

        Raises:
          DataCollectorError:

        --------------------------------------------------------
        Override Notes:
          不限实现方式，为了性能，最好存储在数据库或者本地缓存
        """
        return self.get_stock_data_period(stock_code_list, day, day, frequency, adjust_flag)

    def is_trade_day(self, day=None):
        """判断day是否为交易日
        
        Args:
          day: String，需要查询的日期，格式为:"2021-3-23"

        Returns:
          bool: 是否为交易日

        Raise:
          DataCollectorError
        """
        if not self.__login:
            self.__logger.error("is_trade_day: baostock未登录")
            raise DataCollectorError("you dont't login.")

        if not day:
            self.__logger.warning("is_trade_day: 输入日期None，直接返回False")
            return False

        rs = bs.query_trade_dates(start_date=day, end_date=day)

        if rs.error_code != '0':
            self.__logger.error("is_trade_day: baostock query_trade_date调用失败")
            raise DataCollectorError("baostock: query_trade_dates error:" + rs.error_msg)

        trade_dates = rs.get_row_data()
        try:
            res = bool(int(trade_dates[1]))
        except:
            self.__logger.error("is_trade_day: index error")
            raise DataCollectorError("index error")

        return res

    def get_recent_trade_day(self, day=None):
        """获取day之前最接近day的交易日
        
        获取当前日期之前，最近的交易日期

        Args:
          day: String，日期，格式为："2022-1-20"。如果省略，则day为运行时日期

        Returns:
          String: 离day最近的交易日
        Raises:
        """
        if not day:
            self.__logger.warning("get_recent_trade_day: 未输入日期，默认找距离今天最近的交易日")
            day = get_date()
            
        for i in range(40000): # 为了避免死循环，设置最大循环次数
            try:
                if self.is_trade_day(day):
                    return day
            except DataCollectorError as e:
                raise e
            day = date_decrease(day)

        self.__logger.critical("get_recent_trade_day: 出现死循环")

    def get_data_collector_info(self):
        res = ""
        res += "log path:" + LOGGING_FILE_NAME + "\n"
        res += "data source: baostock\n"
        res += "config: " + str(self.__config)
        return res

    #
    # ----------------------- 本地缓存获取数据 -------------------------
    #
    def __has_local_cache_data(self, stock_code, start, end):
        if not self.__cache_util:
            self.__logger.info("__has_local_cache_data：没有cache util")
            return False
        return self.__cache_util.has_batch_cache(stock_code, start, end)
        
    def __get_stock_data_from_local_cache_period(self, stock_code, start, end, frequency):
        """从本地或者数据库获取数据
        """
        if not self.__cache_util:
            return -1, {}
        return 0, self.__cache_util.get_stock_data_batch(stock_code, start, end, frequency)

    def __get_stock_data_from_local_cache(self, stock_code, date):
        if not self.__cache_util:
            return -1,{}
        return 0, self.__cache_util.get_stock_data(stock_code, date)

    #
    # ----------------------- 从线上获取数据 -------------------------
    #
    def __get_stock_data_from_online_period(self, stock_code, start, end, frequency, adjust_flag):
        """从网上获取数据
        """
        return self.__get_stock_data_from_baostock(stock_code,start,end, frequency, adjust_flag)

    def __get_stock_data_from_baostock(self, stock_code, start, end, frequency, adjust_flag):
        """从baostock获取某股票一段时期内的k线数据
        
        获取股票代码为code的股票，从startDay到endDay的k线数据
        
        Args:
          code: String，证券代码，比如"sh.600000"
          startDay: 以字符串形式表示的日期，比如'2008-1-1'
          endDay: 以字符串形式表示的日期，比如'2008-1-1'。默认为当日交易日
          
        Returns:
          Number:error_code
          pandas DataFrame: 至少包含17列:date,code,type,ipoDate,code_name,open,high,low,close,preclose,volume,amount,adjustflag,turn,tradestatus,pctChg,isST

        Raises:
          DataCollectorError
        """
        if not self.__login:
            self.__logger.error("__get_stock_data_from_baostock: baostock未登录")
            raise DataCollectorError("you dont't login.")

        self.__logger.info("getting %s ...", stock_code)
        rs_k = bs.query_history_k_data_plus(
            stock_code,
            frequency2fields[frequency],
            start_date=start,
            end_date=end,
            frequency=frequency.value,
            adjustflag=adjust_flag.value)
        
        if rs_k.error_code != '0': 
            self.__logger.error("__get_stock_data_from_baostock: baostock query_history_k_data_plus调用失败, stock_code = " + stock_code)
            return int(rs_k.error_code), {}
        
        stock_datas = []
        
        while (rs_k.error_code == '0') & rs_k.next():
            stock_single_day_data = rs_k.get_row_data()

            keys = frequency2keys[frequency]
            dicts = {}
            for i in range(len(stock_single_day_data)):
                dicts[keys[i]] = stock_single_day_data[i]

            try:
                if self.__cache_util:
                    self.__cache_util.save_stock_data(stock_code, dicts['date'], dicts)
                stock_datas.append(dicts)
            except Exception as e:
                self.__logger.error("__get_stock_data_from_baostock: index error")
                raise DataCollectorError("dicts index error")

        return 0, stock_datas


if __name__ == '__main__':
    #print(str(default_config))
    data_collector = BaostockDataCollector(config_dict = {"log":log_config.DEBUG_LOG, "cache":cache_config.NO_CACHE})
    err, all_stock_code = data_collector.get_all_stock_code()
    for code in all_stock_code:
        #data_collector.get_stock_basic_data(code)
        err, data = data_collector.get_stock_data_period(code)
    #print(data_collector.get_stock_type("bj.430047"))
    #print(data)
    #print(data_collector.get_stock_data("sz.399996", day="2022-01-20"))
    #print(data_collector.get_recent_trade_day("2022-01-01"))
