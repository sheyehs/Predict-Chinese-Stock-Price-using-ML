import pandas as pd
import numpy as np
from tqdm import tqdm
import os
import warnings
warnings.filterwarnings('ignore')

'''
Data Extraction
定义函数，用来从存放数据的文件夹中提取所需变量。
原始数据格式要为带表头的表格，而结果数据格式是关于某一变量pivot table，
准确地说，是横轴为样本、纵轴为日期、内容为变量取值的二维表格。
并且会把日期转换为pandas.DatetimeIndex类型
'''


# 从原始数据中提取出数据透视表，并且会把index转化为pandas的日期索引
def extract_variable(path: str = "", fileType: str = "csv", variable: str = "", time_col: str = "",
                     code_col: str = "", print_fileName: bool = False):
    """
    path: fold address
    fileType: default: csv
    variable: about the target variable, the column name of the target variable in raw data
    index: column name of the target index in raw data
    columns: column name of the target columns in raw data
    移植时要修改“只选沪深A股“部分，该部分针对CSMAR股市数据
    """
    # collect all data needed in the fold and print their names
    filePathList = []
    for root, dirs, files in os.walk(path):
        for name in files:
            if name.endswith("." + fileType):
                filePath = os.path.join(root, name)
                filePathList.append(filePath)
                if print_fileName == True:
                    print(filePath)

    # read files into DataFrame one by one
    dfList = []
    for filePath in filePathList:
        if fileType == 'csv':
            df = pd.read_csv(filePath)
        # other types left to supplement
        dfList.append(df)

    # concatenate the DFs into one large table
    all_df = pd.concat(dfList)

    # 只选沪深A股，若原始数据中有"Markettype"列
    # flag = False
    if "Markettype" in all_df.columns:
        all_df = all_df[all_df.loc[:, "Markettype"].isin([1, 4])]  # 1，4在csmar中代表沪深主板
        # flag = True
    else:
        f = lambda x: True if (x >= 0 and x <= 9999) or (x >= 600000 and x <= 609999) else False
        all_df = all_df[all_df[code_col].map(f)]

    pivot_df = pd.pivot_table(all_df, values=variable, index=time_col, columns=code_col)

    '''# 只选沪深A股，若若原始数据中无"Markettype"列，只能靠股票代码的数据(是int)来区分。不知两种方法快慢
    if flag == False:
        df1 = pivot_df.loc[:, 0:9999]
        df2 = pivot_df.loc[:, 600000:609999]
        pivot_df = pd.concat([df1, df2], axis=1)'''

    # 转换日期类型
    pivot_df.index = pd.DatetimeIndex(pivot_df.index)

    return pivot_df


def extract_variable_oneFile(filePath: str = "", fileType="csv", variable: str = "", time_col: str = "",
                             code_col: str = ""):
    if fileType == 'csv':
        df = pd.read_csv(filePath)

    # 只选沪深A股
    # flag = False
    if "Markettype" in df.columns:
        df = df[df.loc[:, "Markettype"].isin([1, 4])]
        # flag = True
    else:
        f = lambda x: True if (x >= 0 and x <= 9999) or (x >= 600000 and x <= 609999) else False
        df = df[df[code_col].map(f)]

    pivot_df = pd.pivot_table(df, values=variable, index=time_col, columns=code_col)

    pivot_df.index = pd.DatetimeIndex(pivot_df.index)

    return pivot_df

"""
定义一个函数用来做等权重均值作差的行业调整，适用于全部以_ia结尾的因子
"""
def industry_adjust_ewa(value_df: pd.DataFrame, industry_df: pd.DataFrame, showprocess:bool=False):
    """
    equally-weighted average industry adjustment:
    x_ia_it = x_it − x_It

    params:
    value_df: a 2-dimension(index are dates,cols are codes) table of target values
    industry_df: classification, index is the implement date and 2 columns by order are stock code and industry classification
    """
    industry_df.sort_index(inplace=True)
    symbols = value_df.columns
    for day in tqdm(value_df.index):
        if showprocess:
            print(day)
        value_sec = value_df.loc[day]
        group = []
        for sym in symbols:
            cls = industry_df[industry_df.iloc[:, 0] == sym].iloc[:, 1]
            cls = cls[cls.index <= day]
            if cls.empty:
                cls = np.nan
                value_df.loc[day, sym] = np.nan
            else:
                cls = cls[-1]
            group.append(cls)
        means = value_sec.groupby(group).mean().reindex(group)
        means.index = symbols
        value_df.loc[day] = value_df.loc[day] - means

    return value_df

def industry_proportion(value_df: pd.DataFrame, industry_df: pd.DataFrame, showprocess:bool=False):
    """
    calculate the percentage in the industry of one's value

    params:
    value_df: a 2-dimension(rows are dates,cols are codes) table of target values
    industry_df: classification, index is implement date and 2 columns by order are stock code and industry classification
    """
    industry_df.sort_index(inplace=True)
    symbols = value_df.columns
    for day in tqdm(value_df.index):
        if showprocess:
            print(day)
        value_sec = value_df.loc[day]
        group = []
        for sym in symbols:
            cls = industry_df[industry_df.iloc[:, 0] == sym].iloc[:, 1]
            cls = cls[cls.index <= day]
            if cls.empty:
                cls = np.nan
                value_df.loc[day, sym] = np.nan
            else:
                cls = cls[-1]
            group.append(cls)
        sums = value_sec.groupby(group).sum().reindex(group)
        sums.index = symbols
        value_df.loc[day] = value_df.loc[day] / sums

    return value_df
