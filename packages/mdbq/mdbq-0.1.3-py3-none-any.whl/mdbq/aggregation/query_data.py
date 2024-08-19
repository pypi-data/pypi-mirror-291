# -*- coding: UTF-8 –*-
from mdbq.mongo import mongo
from mdbq.mysql import s_query
from mdbq.config import get_myconf
import datetime
from dateutil.relativedelta import relativedelta
import pandas as pd
import numpy as np
import platform
import getpass
import json
import os
"""
程序用于下载数据库(调用 s_query.py 下载并清洗), 并对数据进行聚合清洗, 不会更新数据库信息;
"""


class MongoDatasQuery:
    """
    从 数据库 中下载数据
    self.output: 数据库默认导出目录
    self.is_maximize: 是否最大转化数据
    """
    def __init__(self, target_service):
        # target_service 从哪个服务器下载数据
        self.months = 0  # 下载几个月数据, 0 表示当月, 1 是上月 1 号至今
        # 实例化一个下载类
        username, password, host, port = get_myconf.select_config_values(target_service=target_service, database='mongodb')
        self.download = mongo.DownMongo(username=username, password=password, host=host, port=port, save_path=None)

    def tg_wxt(self):
        self.download.start_date, self.download.end_date = self.months_data(num=self.months)
        projection = {
            '日期': 1,
            '场景名字': 1,
            '主体id': 1,
            '花费': 1,
            '展现量': 1,
            '点击量': 1,
            '总购物车数': 1,
            '总成交笔数': 1,
            '总成交金额': 1,
            '自然流量曝光量': 1,
            '直接成交笔数': 1,
            '直接成交金额': 1,
        }
        df = self.download.data_to_df(
            db_name='天猫数据2',
            collection_name='推广数据_宝贝主体报表',
            projection=projection,
        )
        return df

    @staticmethod
    def days_data(days, end_date=None):
        """ 读取近 days 天的数据 """
        if not end_date:
            end_date = datetime.datetime.now()
        start_date = end_date - datetime.timedelta(days=days)
        return pd.to_datetime(start_date), pd.to_datetime(end_date)

    @staticmethod
    def months_data(num=0, end_date=None):
        """ 读取近 num 个月的数据, 0 表示读取当月的数据 """
        if not end_date:
            end_date = datetime.datetime.now()
        start_date = end_date - relativedelta(months=num)  # n 月以前的今天
        start_date = f'{start_date.year}-{start_date.month}-01'  # 替换为 n 月以前的第一天
        return pd.to_datetime(start_date), pd.to_datetime(end_date)


class MysqlDatasQuery:
    """
    从数据库中下载数据
    """
    def __init__(self, target_service):
        # target_service 从哪个服务器下载数据
        self.months = 0  # 下载几个月数据, 0 表示当月, 1 是上月 1 号至今
        # 实例化一个下载类
        username, password, host, port = get_myconf.select_config_values(target_service=target_service, database='mysql')
        self.download = s_query.QueryDatas(username=username, password=password, host=host, port=port)

    def tg_wxt(self):
        start_date, end_date = self.months_data(num=self.months)
        projection = {
            '日期': 1,
            '场景名字': 1,
            '主体id': 1,
            '花费': 1,
            '展现量': 1,
            '点击量': 1,
            '总购物车数': 1,
            '总成交笔数': 1,
            '总成交金额': 1,
            '自然流量曝光量': 1,
            '直接成交笔数': 1,
            '直接成交金额': 1,
        }
        df = self.download.data_to_df(
            db_name='天猫数据2',
            tabel_name='推广数据_宝贝主体报表',
            start_date=start_date,
            end_date=end_date,
            projection=projection,
        )
        return df

    def syj(self):
        start_date, end_date = self.months_data(num=self.months)
        projection = {
            '日期': 1,
            '宝贝id': 1,
            '商家编码': 1,
            '行业类目': 1,
            '销售额': 1,
            '销售量': 1,
            '订单数': 1,
            '退货量': 1,
            '退款额': 1,
            '退货量_发货后_': 1,
        }
        df = self.download.data_to_df(
            db_name='生意经2',
            tabel_name='宝贝指标',
            start_date=start_date,
            end_date=end_date,
            projection=projection,
        )
        return df

    def dplyd(self):
        start_date, end_date = self.months_data(num=self.months)
        projection = {
            '日期': 1,
            '一级来源': 1,
            '二级来源': 1,
            '三级来源': 1,
            '访客数': 1,
            '支付金额': 1,
            '支付买家数': 1,
            '支付转化率': 1,
            '加购人数': 1,
        }
        df = self.download.data_to_df(
            db_name='生意参谋数据2',
            tabel_name='店铺来源_日数据',
            start_date=start_date,
            end_date=end_date,
            projection=projection,
        )
        return df

    @staticmethod
    def months_data(num=0, end_date=None):
        """ 读取近 num 个月的数据, 0 表示读取当月的数据 """
        if not end_date:
            end_date = datetime.datetime.now()
        start_date = end_date - relativedelta(months=num)  # n 月以前的今天
        start_date = f'{start_date.year}-{start_date.month}-01'  # 替换为 n 月以前的第一天
        return pd.to_datetime(start_date), pd.to_datetime(end_date)


class GroupBy:
    """
    数据聚合和导出
    """
    def __init__(self):
        # self.output: 数据库默认导出目录
        if platform.system() == 'Darwin':
            self.output = os.path.join('/Users', getpass.getuser(), '数据中心/数据库导出')
        elif platform.system() == 'Windows':
            self.output = os.path.join('C:\\同步空间\\BaiduSyncdisk\\数据库导出')
        else:
            self.output = os.path.join('数据中心/数据库导出')

    def groupby(self, df, tabel_name, is_maximize=True):
        """
        self.is_maximize: 是否最大转化数据
        """

        if '宝贝主体报表' in tabel_name:
            df.rename(columns={
                '场景名字': '营销场景',
                '主体id': '商品id',
                '总购物车数': '加购量',
                '总成交笔数': '成交笔数',
                '总成交金额': '成交金额'
            }, inplace=True)
            df = df.astype({
                '花费': float,
                '展现量': int,
                '点击量': int,
                '加购量': int,
                '成交笔数': int,
                '成交金额': float,
                '自然流量曝光量': int,
                '直接成交笔数': int,
                '直接成交金额': float,
            }, errors='raise')
            df.fillna(0, inplace=True)
            if is_maximize:
                df = df.groupby(['日期', '营销场景', '商品id', '花费', '展现量', '点击量'], as_index=False).agg(
                    **{'加购量': ('加购量', np.max),
                       '成交笔数': ('成交笔数', np.max),
                       '成交金额': ('成交金额', np.max),
                       '自然流量曝光量': ('自然流量曝光量', np.max),
                       '直接成交笔数': ('直接成交笔数', np.max),
                       '直接成交金额': ('直接成交金额', np.max)
                       }
                )
            else:
                df = df.groupby(['日期', '营销场景', '商品id', '花费', '展现量', '点击量'], as_index=False).agg(
                    **{'加购量': ('加购量', np.min),
                       '成交笔数': ('成交笔数', np.min),
                       '成交金额': ('成交金额', np.min),
                       '自然流量曝光量': ('自然流量曝光量', np.min),
                       '直接成交笔数': ('直接成交笔数', np.max),
                       '直接成交金额': ('直接成交金额', np.max)
                       }
                )
            df.insert(loc=1, column='推广渠道', value='万相台无界版')  # df中插入新列
            return df
        elif '宝贝指标' in tabel_name:
            df.fillna(0, inplace=True)
            df = df[(df['销售额'] != 0) | (df['退款额'] != 0)]
            df = df.groupby(['日期', '宝贝id', '商家编码', '行业类目'], as_index=False).agg(
                **{'销售额': ('销售额', np.min),
                   '销售量': ('销售量', np.min),
                   '订单数': ('订单数', np.min),
                   '退货量': ('退货量', np.max),
                   '退款额': ('退款额', np.max),
                   '退货量_发货后_': ('退货量_发货后_', np.max),
                   }
            )
            df['件均价'] = df.apply(lambda x: x['销售额'] / x['销售量'] if x['销售量'] > 0 else 0, axis=1).round(
                0)  # 两列运算, 避免除以0
            df['价格带'] = df['件均价'].apply(
                lambda x: '2000+' if x >= 2000
                else '1000+' if x >= 1000
                else '500+' if x >= 500
                else '300+' if x >= 300
                else '300以下'
            )
            return df
        elif '店铺来源_日数据' in tabel_name:
            return df
        else:
            print(f'<{tabel_name}>: Groupby 类尚未配置，数据为空')
            return pd.DataFrame({})
    
    def as_csv(self, df, filename, path=None, encoding='utf-8_sig',
               index=False, header=True, st_ascend=None, ascend=None, freq=None):
        """
        path: 默认导出目录 self.output, 这个函数的 path 作为子文件夹，可以不传，
        st_ascend: 排序参数 ['column1', 'column2']
        ascend: 升降序 [True, False]
        freq: 将创建子文件夹并按月分类存储,  freq='Y', 或 freq='M'
        """
        if len(df) == 0:
            return
        if not path:
            path = self.output
        else:
            path = os.path.join(self.output, path)
        if not os.path.exists(path):
            os.makedirs(path)
        if st_ascend and ascend:
            try:
                df.sort_values(st_ascend, ascending=ascend, ignore_index=True, inplace=True)
            except:
                print(f'{filename}: sort_values排序参数错误！')
        if freq:
            if '日期' not in df.columns.tolist():
                return print(f'{filename}: 数据缺少日期列，无法按日期分组')
            groups = df.groupby(pd.Grouper(key='日期', freq=freq))
            for name1, df in groups:
                if freq == 'M':
                    sheet_name = name1.strftime('%Y-%m')
                elif freq == 'Y':
                    sheet_name = name1.strftime('%Y年')
                else:
                    sheet_name = '_未分类'
                new_path = os.path.join(path, filename)
                if not os.path.exists(new_path):
                    os.makedirs(new_path)
                new_path = os.path.join(new_path, f'{filename}{sheet_name}.csv')
                if st_ascend and ascend:  # 这里需要重新排序一次，原因未知
                    try:
                        df.sort_values(st_ascend, ascending=ascend, ignore_index=True, inplace=True)
                    except:
                        print(f'{filename}: sort_values排序参数错误！')

                df.to_csv(new_path, encoding=encoding, index=index, header=header)
        else:
            df.to_csv(os.path.join(path, filename + '.csv'), encoding=encoding, index=index, header=header)

    def as_json(self, df, filename, path=None, orient='records', force_ascii=False, st_ascend=None, ascend=None):
        if len(df) == 0:
            return
        if not path:
            path = self.output
        else:
            path = os.path.join(self.output, path)
        if not os.path.exists(path):
            os.makedirs(path)
        if st_ascend and ascend:
            try:
                df.sort_values(st_ascend, ascending=ascend, ignore_index=True, inplace=True)
            except:
                print(f'{filename}: sort_values排序参数错误！')
        df.to_json(os.path.join(path, filename + '.json'),
                   orient=orient, force_ascii=force_ascii)

    def as_excel(self, df, filename, path=None, index=False, header=True, engine='openpyxl',
                 freeze_panes=(1, 0), st_ascend=None, ascend=None):
        if len(df) == 0:
            return
        if not path:
            path = self.output
        else:
            path = os.path.join(self.output, path)
        if not os.path.exists(path):
            os.makedirs(path)
        if st_ascend and ascend:
            try:
                df.sort_values(st_ascend, ascending=ascend, ignore_index=True, inplace=True)
            except:
                print(f'{filename}: sort_values排序参数错误！')
        df.to_excel(os.path.join(path, filename + '.xlsx'),
                    index=index, header=header, engine=engine, freeze_panes=freeze_panes)
        
        
def data_output():
    sdq = MysqlDatasQuery(target_service='home_lx')
    sdq.months = 0

    # df = sdq.tg_wxt()  # 从数据库中获取数据并转为 df
    # g = GroupBy()  # 数据聚合
    # df = g.groupby(df=df, tabel_name='推广数据_宝贝主体报表', is_maximize=True)
    # g.as_csv(df=df, filename='推广数据_宝贝主体报表')  # 数据导出

    # df = sdq.syj()
    # g = GroupBy()
    # df = g.groupby(df=df, tabel_name='宝贝指标', is_maximize=True)
    # g.as_csv(df=df, filename='宝贝指标')

    df = sdq.dplyd()
    g = GroupBy()
    df = g.groupby(df=df, tabel_name='店铺来源_日数据', is_maximize=True)
    g.as_csv(df=df, filename='店铺来源_日数据')


if __name__ == '__main__':
    main()
