import torch 
import torch.nn.functional as F
from abc import ABC, abstractmethod
import torch.nn as nn
import random

import pandas as pd
from pandas import Series,DataFrame
import numpy as np
from ..stockcalendar import CALENDAR_TOOL
from torch.utils.data import TensorDataset, DataLoader

trade_dates = CALENDAR_TOOL.trade_date_in_range(start_date='20010101',end_date='20261201').copy(deep=True)

class ByTimeDataLoader:
    """
    每回遍历不重复的从data_set中跳出一个数据点
    """
    def __init__(self, data_set, data_range=None):
        """
        初始化迭代器
        :param data_set: 数据集，列表形式
        :param data_range: 生成随机数据的范围，默认为data_set的列表长度
        """
        self.data_set = data_set
        if data_range == None:
            self.data_range = len(data_set)
        else:
            self.data_range = data_range
        self.current_batch = 0
        self.random_shuffle = [_ for _ in range(self.data_range)]
        random.shuffle(self.random_shuffle)
    
    def reset(self):
        random.shuffle(self.random_shuffle)
        self.current_batch = 0

    def __iter__(self):
        """返回迭代器对象本身"""
        return self

    def __next__(self):
        """生成下一个随机批量的数据"""
        if self.current_batch < self.data_range:
            batch_data = self.data_set[self.random_shuffle[self.current_batch]]
            self.current_batch += 1
            return batch_data
        else:
            self.reset()
            raise StopIteration  # 如果所有批次都已经生成，则停止迭代


class DLmodel(ABC):
    """
    深度学习模型的抽象类, 子类要实现必要的方法.
    
    基类功能:
    - self.__init__():
        -- self.check: 检查GPU资源可用性
        -- self.class_model: DL模型架构
        -- self._model_params(dict): DL模型参数设定
        -- self._dtype: 模型精度，默认float
        -- self.set_params: 设定模型参数，每次调用都会重置模型
    
    - self.check: 检查GPU资源可用性
    - self.set_params: 设定模型参数，每次调用都会重置模型
    - self.save: 存储模型
    
    子类功能:
    - self.train(): 子类必须实现模型的训练功能   
    - self.test(): 子类必须实现模型的测试功能 
    
    """
    
    def __init__(self,model_params:dict,class_model,dtype='float') -> None:
        self.check()
        
        self.class_model = class_model
        self._model_params:dict = model_params
        self._dtype = dtype
        self.set_params()
    
    def check(self):
        print('CUDA is available:{}'.format(torch.cuda.is_available()))
        print('GPU device count:{}'.format(torch.cuda.device_count()))
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        if not torch.cuda.is_available():
            print('Use CPU!!!')
        else:
            print('GPU device name_0:{}'.format(torch.cuda.get_device_name(0)))
        
    def set_params(self):
        if self._dtype == 'float':
            self.model = self.class_model(**self._model_params).float().to(self.device)
        else:
            self.model = self.class_model(**self._model_params).to(self.device)
    
    def r2_score(self,target:torch.tensor,output:torch.tensor):
        # 计算总平方和 (SStot)
        mean_target = torch.mean(target,dim=0)
        total_sum_squares = torch.sum((target - mean_target) ** 2,dim=0)

        # 计算残差平方和 (SSres)
        residual_sum_squares = torch.sum((target - output) ** 2,dim=0)

        # 计算R² score
        r2score = 1 - (residual_sum_squares / total_sum_squares)
        return r2score
    
    def precision(self,pred,actu):
        result = torch.mean((pred == actu).float())
        return result
    
    def recall(self,pred,actu,typenum):
        recall_per_class = []
        for class_id in range(typenum):
            TP = ((pred == class_id) & (actu == class_id)).sum()
            FN = ((pred != class_id) & (actu == class_id)).sum()
            recall = TP / (TP + FN) if TP + FN > 0 else torch.tensor(0.0)
            recall_per_class.append(recall)

        # 计算宏观平均召回率
        macro_recall = sum(recall_per_class) / len(recall_per_class)
        return macro_recall
        
    def f1_score(self,pred,actu,typenum):

        prec = self.precision(pred,actu)
        rec = self.recall(pred,actu,typenum)
        # 计算F1分数
        # F1分数是精确率和召回率的调和平均
        f1_score = 2 * (prec * rec) / (prec + rec)

        return f1_score,prec,rec
    
    def reload_model(self,path):
        self.model = torch.load(path)
            
    
    @abstractmethod
    def train(self):
        raise NotImplementedError("should implement in the derived class")
    
    
    def save(self,path,device='GPU'):
        if device == 'GPU':
            self.model.eval()
            torch.save(self.model,path)
        else:
            self.model.eval()
            torch.save(self.model.cpu(),path)
            
            
class WeightedMSE(nn.Module):
    def __init__(self, w=2):
        super(WeightedMSE, self).__init__()
        self.w = w
        
    def forward(self, y_pred, y_true):
        # weights = torch.where(y_true > 0, self.w, 1.0)
        weights = 100*torch.abs(y_true)+1
        loss = torch.mean(weights * (y_true - y_pred) ** 2)
        return loss
    

class GenDataSet:
    """
    用于生成各种类型数据集的类函数
    """
    
    @staticmethod
    def base_train_dataset(factor,price,dates,seq_len,forward,dropmid=None,dtype='float',assets=None):
        """
        Params:
        -factor: pd.DataFrame. index=pd.MultiIndex, level0 = asset, level1 = date;
        -price: pd.DataFrame. index=date, columns = asset
        -dates: list(datetime). 提供你要生成数据点的时间点，将逐次生成训练数据，可通过控制这个参数防止偷看未来数据
        -seq_len: int. 获取的因子矩阵的时序长度
        -forward: int. 获取的未来收益率长度
        -dropmid=None: float. 在进行标签筛选时是否扔掉中间的部分数据
        -dtype='float': str. 生成的数据集数据类型
        
        Return:
        (index,dataset): 与dataset相对应的index, 方便直接使用训练集输出测试预测因子
        
        Attention: 
        - 建议你提供的数据相对于时间点来说要足够长, 否则会丢弃很多长度不够的数据点。
        - 对于时间点前seqlen长度的数据，若空缺比例超过0.1会丢弃该数据点，所以请在因子输入时dropna
        """
        seek_backward_dates = Series(trade_dates,index=trade_dates).shift(seq_len).dropna()
        if assets is None:
            assets = list(set(list(factor.index.get_level_values(0))) & set(list(price.columns)))
        else:
            assets = list(set(list(assets)) & set(list(factor.index.get_level_values(0))) & set(list(price.columns)))
        price = price[assets]
        
        
        def single_point(asset,date,seq_len):
            pre_date = seek_backward_dates.loc[date]
            df = factor.loc[asset].loc[pre_date:date]
            
            if len(df) < seq_len*0.9:
                return None
            else:
                df = factor.loc[asset].loc[:date].iloc[-seq_len:].values
                if len(df) != seq_len:
                    return None
                return ((asset,date),df)
        
        X_ = []
        y_ = []
        
        index = []
        
        def drop_mid_Series(sr:Series,dropmid):
            sr = sr.sort_values()
            l = len(sr)
            if l < 100:
                return sr
            return pd.concat([sr.iloc[:int(l*(1/2-dropmid/2))],sr.iloc[int(l*(1/2+dropmid/2)):]])
        
        forward_returns = (price.shift(-forward)/price - 1)
        for date in dates:
            y:Series = forward_returns.loc[date].dropna()
            if len(y) == 0:
                continue
            if dropmid is not None:
                y = drop_mid_Series(y,dropmid)
            for asset in y.index:
                dv = single_point(asset,date,seq_len)
                if dv is None:
                    continue
                
                X_.append(dv[1])
                y_.append(y.loc[asset])
                index.append(dv[0])

        if dtype == 'float':
            X_ = torch.tensor(np.array(X_)).float()
            y_ = torch.tensor(np.array(y_)).reshape(len(y_),-1).float()
        else:
            X_ = torch.tensor(np.array(X_))
            y_ = torch.tensor(np.array(y_)).reshape(len(y_),-1)
            
        index = pd.MultiIndex.from_tuples(index,names=['asset','date'])
        
        return (index,TensorDataset(X_,y_))
    
    
    @staticmethod
    def market_train_dataset(factor,price,market,dates,seq_len,forward,dropmid=None,dtype='float',droptop=None):
        """
        Params:
        -factor: pd.DataFrame. index=pd.MultiIndex, level0 = asset, level1 = date;
        -price: pd.DataFrame. index=date, columns = asset
        -market: pd.Series. index=date, 你需要额外提供一个市场数据(收盘价)，标签将会是超市场收益
        -dates: list(datetime). 提供你要生成数据点的时间点，将逐次生成训练数据，可通过控制这个参数防止偷看未来数据
        -seq_len: int. 获取的因子矩阵的时序长度
        -forward: int. 获取的未来收益率长度
        -dropmid=None: float. 在进行标签筛选时是否扔掉中间的部分数据
        -dtype='float': str. 生成的数据集数据类型
        
        Return:
        (index,dataset): 与dataset相对应的index, 方便直接使用训练集输出测试预测因子
        """
        seek_backward_dates = Series(trade_dates,index=trade_dates).shift(seq_len).dropna()
        def single_point(asset,date,seq_len):
            pre_date = seek_backward_dates.loc[date]
            df = factor.loc[asset].loc[pre_date:date]
            if len(df) < seq_len*0.9:
                return None
            else:
                df = factor.loc[asset].loc[:date].iloc[-seq_len:].values
                if len(df) != seq_len:
                    return None
                return ((asset,date),df)
        
        X_ = []
        y_ = []
        
        index = []
        
        def drop_mid_Series(sr:Series,dropmid):
            sr = sr.sort_values()
            l = len(sr)
            if l < 100:
                return sr
            return pd.concat([sr.iloc[:int(l*(1/2-dropmid/2))],sr.iloc[int(l*(1/2+dropmid/2)):]])
        
        def drop_top_Series(sr:Series,droptop):
            sr = sr.sort_values()
            l = len(sr)
            if l < 100:
                return sr
            return sr.iloc[:int(l*(1-droptop))]
        
        forward_returns:DataFrame = (price.shift(-forward)/price - 1)
        forward_market = (market.shift(-forward)/market - 1)
        forward_exceed = forward_returns.subtract(forward_market,axis=0)
        for date in dates:
            y:Series = forward_exceed.loc[date].dropna()
            if len(y) == 0:
                continue
            if dropmid is not None:
                y = drop_mid_Series(y,dropmid)
            if droptop is not None:
                y = drop_top_Series(y,droptop)
            for asset in y.index:
                dv = single_point(asset,date,seq_len)
                if dv is None:
                    continue
                
                X_.append(dv[1])
                y_.append(y.loc[asset])
                index.append(dv[0])

        if dtype == 'float':
            X_ = torch.tensor(np.array(X_)).float()
            y_ = torch.tensor(np.array(y_)).reshape(len(y_),-1).float()
        else:
            X_ = torch.tensor(np.array(X_))
            y_ = torch.tensor(np.array(y_)).reshape(len(y_),-1)
            
        index = pd.MultiIndex.from_tuples(index,names=['asset','date'])
        
        return (index,TensorDataset(X_,y_))
    
    
    @staticmethod
    def seq_train_dataset(factor,price,dates,seq_len,forward,assets=None,dtype='float'):
        """
        Params:
        -factor: pd.DataFrame. index=pd.MultiIndex, level0 = asset, level1 = date;
        -price: pd.DataFrame. index=date, columns = asset
        -dates: list(datetime). 提供你要生成数据点的时间点，将逐次生成训练数据，可通过控制这个参数防止偷看未来数据
        -seq_len: int. 获取的因子矩阵的时序长度
        -forward: int. 获取的未来收益率长度
        -dtype='float': str. 生成的数据集数据类型
        
        Return:
        (index,dataset): 你得到的标签将会是forward长度的收益率序列，而非单个收益率.与dataset相对应的index, 方便直接使用训练集输出测试预测因子.
        """
        if assets is None:
            assets = list(set(list(factor.index.get_level_values(0))) & set(list(price.columns)))
        else:
            assets = list(set(list(assets)) & set(list(factor.index.get_level_values(0))) & set(list(price.columns)))
        price = price[assets]
        
        
        seek_backward_dates = Series(trade_dates,index=trade_dates).shift(seq_len).dropna()
        def single_point(asset,date,seq_len):
            pre_date = seek_backward_dates.loc[date]
            df = factor.loc[asset].loc[pre_date:date]
            if len(df) < seq_len*0.9:
                return None
            else:
                df = factor.loc[asset].loc[:date].iloc[-seq_len:].values
                if len(df) != seq_len:
                    return None
                return ((asset,date),df)
        
        X_ = []
        y_ = []
        
        index = []
        returns = price/price.shift(1)-1
        forward_returns = (price.shift(-forward)/price - 1)
        for date in dates:
            y = returns.loc[date:].iloc[1:forward+1].T.dropna()
            if len(y) == 0:
                continue
            for asset in y.index:
                dv = single_point(asset,date,seq_len)
                if dv is None:
                    continue
                
                X_.append(dv[1])
                y_.append(y.loc[asset].values)
                index.append(dv[0])

        if dtype == 'float':
            X_ = torch.tensor(np.array(X_)).float()
            y_ = torch.tensor(np.array(y_)).float()
        else:
            X_ = torch.tensor(np.array(X_))
            y_ = torch.tensor(np.array(y_))
            
        index = pd.MultiIndex.from_tuples(index,names=['asset','date'])
        
        return (index,TensorDataset(X_,y_))
    
    @staticmethod
    def Seq_train_dataset(factor,price,dates,seq_len,forward:int=7,dtype='float',assets=None):
        """
        Introduce:
        获得标签为未来forward日的数据序列的数据集，要保证factor已经dropna，空缺日期比例超过10%则丢弃该数据点
        
        Params:
        -factor: pd.DataFrame. index=pd.MultiIndex, level0 = asset, level1 = date;
        -price: pd.DataFrame. index=date, columns = asset
        -dates: list(datetime). 提供你要生成数据点的时间点，将逐次生成训练数据，可通过控制这个参数防止偷看未来数据
        -seq_len: int. 获取的因子矩阵的时序长度
        -forward: int. 获取的未来收益率长度, 输出的标签为未来forward天的收益率序列，可以构造夏普比等特殊标签
        -dropmid=None: float. 在进行标签筛选时是否扔掉中间的部分数据
        -dtype='float': str. 
        -assets=None: list. 提供你筛选后的股票，如果没有则默认为price表提供的股票
        
        Return:
        (index,dataset): 与dataset相对应的index, 方便直接使用训练集输出测试预测因子
        
        Attention: 
        - 建议你提供的数据相对于时间点来说要足够长, 否则会丢弃很多长度不够的数据点。
        - 对于时间点前seqlen长度的数据，若空缺比例超过0.1会丢弃该数据点，所以请在因子输入时dropna
        """
        seek_backward_dates = Series(trade_dates,index=trade_dates).shift(seq_len).dropna()
        if assets is None:
            assets = list(set(list(factor.index.get_level_values(0))) & set(list(price.columns)))
        else:
            assets = list(set(list(assets)) & set(list(factor.index.get_level_values(0))) & set(list(price.columns)))
        price:DataFrame = price[assets]
        returns = price.pct_change()
        
        def single_point(asset,date,seq_len):
            pre_date = seek_backward_dates.loc[date]
            
            df = factor.loc[asset].loc[:date]
            test_df = df.loc[pre_date:]
            if len(test_df) < seq_len*0.9:
                return None
            else:
                df = df.iloc[-seq_len:].values
                if np.isnan(df).sum() > 0:
                    return None
                if len(df) != seq_len:
                    return None
                return ((asset,date),df)
        
        X_ = []
        label = []

        index = []
        forward_returns = []
        for i in range(forward):
            forward_returns.append(returns.shift(-i-1).stack(dropna=False))
        forward_returns = pd.concat(forward_returns,axis=1).sort_index()
        for date in dates:
            y_ = forward_returns.loc[date].dropna()
            if len(y_) == 0:
                continue
            for asset in y_.index:
                dv = single_point(asset,date,seq_len)
                if dv is None:
                    continue
                
                X_.append(dv[1])
                label.append(y_.loc[asset].values)
                index.append(dv[0])

        if dtype == 'float':
            X_ = torch.tensor(np.array(X_)).float()
            label = torch.tensor(np.array(label)).float()
        else:
            X_ = torch.tensor(np.array(X_)).float()
            label = torch.tensor(np.array(label)).float()
            
        index = pd.MultiIndex.from_tuples(index,names=['asset','date'])
        
        return (index,TensorDataset(X_,label))
    
    
    def None_train_dataset(factor,price,dates,seq_len,forward,none_num=None,dropmid=None,dtype='float',assets=None):
        """
        Introduce:
        主要添加了空缺值的处理逻辑，同时尽量不损失数据，空缺比例高于10%则丢弃，否则用ffill填补空缺值.
        
        Params:
        -factor: pd.DataFrame. index=pd.MultiIndex, level0 = asset, level1 = date;
        -price: pd.DataFrame. index=date, columns = asset
        -dates: list(datetime). 提供你要生成数据点的时间点，将逐次生成训练数据，可通过控制这个参数防止偷看未来数据
        -seq_len: int. 获取的因子矩阵的时序长度
        -forward: int. 获取的未来收益率长度
        -dropmid=None: float. 在进行标签筛选时是否扔掉中间的部分数据
        -dtype='float': str. 
        -assets=None: list. 提供你筛选后的股票，如果没有则默认为price表提供的股票
        -none_num: Serier. 提供因子每一行是否有空缺值的bool值Series，不提供会内部计算，有点慢.
        
        Return:
        (index,dataset): 与dataset相对应的index, 方便直接使用训练集输出测试预测因子
        
        Attention: 
        - 建议你提供的数据相对于时间点来说要足够长, 否则会丢弃很多长度不够的数据点。
        """
        seek_backward_dates = Series(trade_dates,index=trade_dates).shift(seq_len).dropna()
        if assets is None:
            assets = list(set(list(factor.index.get_level_values(0))) & set(list(price.columns)))
        else:
            assets = list(set(list(assets)) & set(list(factor.index.get_level_values(0))) & set(list(price.columns)))
        price = price[assets]
        if none_num is None:
            none_num = factor.isna().sum(axis=1)>0
        
        
        def single_point(asset,date,seq_len):
            pre_date = seek_backward_dates.loc[date]
            n = none_num.loc[asset].loc[pre_date:date]
            
            if n.sum() > seq_len*0.1:
                return None
            else:
                df = factor.loc[asset].loc[:date].ffill().iloc[-seq_len:].values
                if np.isnan(df).sum() > 0:
                    return None
                if len(df) != seq_len:
                    return None
                return ((asset,date),df)
        
        X_ = []
        y_ = []
        
        index = []
        
        def drop_mid_Series(sr:Series,dropmid):
            sr = sr.sort_values()
            l = len(sr)
            if l < 100:
                return sr
            return pd.concat([sr.iloc[:int(l*(1/2-dropmid/2))],sr.iloc[int(l*(1/2+dropmid/2)):]])
        
        forward_returns = (price.shift(-forward)/price - 1)
        for date in dates:
            y:Series = forward_returns.loc[date].dropna()
            if len(y) == 0:
                continue
            if dropmid is not None:
                y = drop_mid_Series(y,dropmid)
            for asset in y.index:
                dv = single_point(asset,date,seq_len)
                if dv is None:
                    continue
                
                X_.append(dv[1])
                y_.append(y.loc[asset])
                index.append(dv[0])

        if dtype == 'float':
            X_ = torch.tensor(np.array(X_)).float()
            y_ = torch.tensor(np.array(y_)).reshape(len(y_),-1).float()
        else:
            X_ = torch.tensor(np.array(X_))
            y_ = torch.tensor(np.array(y_)).reshape(len(y_),-1)
            
        index = pd.MultiIndex.from_tuples(index,names=['asset','date'])
        
        return (index,TensorDataset(X_,y_))
    
    
    @staticmethod
    def Multi_None_train_dataset(factor,price,dates,seq_len,forward=(1,3,5,10),none_num=None,dtype='float',assets=None):
        """
        Introduce:
        主要添加了空缺值的处理逻辑，同时尽量不损失数据，空缺比例高于10%则丢弃，否则用ffill填补空缺值. 得到的标签则是多个未来区间的收益率，用于不同长度的预测。
        
        Params:
        -factor: pd.DataFrame. index=pd.MultiIndex, level0 = asset, level1 = date;
        -price: pd.DataFrame. index=date, columns = asset
        -dates: list(datetime). 提供你要生成数据点的时间点，将逐次生成训练数据，可通过控制这个参数防止偷看未来数据
        -seq_len: int. 获取的因子矩阵的时序长度
        -forward: tuple. 获取的未来收益率长度, 可接受多个时间按长度，最后输出的标签每一列都是不同forward的数据
        -dropmid=None: float. 在进行标签筛选时是否扔掉中间的部分数据
        -dtype='float': str. 
        -assets=None: list. 提供你筛选后的股票，如果没有则默认为price表提供的股票
        -none_num: Serier. index=pd.MultiIndex, level0 = asset, level1 = date. 提供因子每一行是否有空缺值的bool值Series，不提供会内部计算，有点慢.
        
        Return:
        (index,dataset): 与dataset相对应的index, 方便直接使用训练集输出测试预测因子
        
        Attention: 
        - 建议你提供的数据相对于时间点来说要足够长, 否则会丢弃很多长度不够的数据点。
        """
        seek_backward_dates = Series(trade_dates,index=trade_dates).shift(seq_len).dropna()
        if assets is None:
            assets = list(set(list(factor.index.get_level_values(0))) & set(list(price.columns)))
        else:
            assets = list(set(list(assets)) & set(list(factor.index.get_level_values(0))) & set(list(price.columns)))
        price = price[assets]
        if none_num is None:
            none_num = factor.isna().sum(axis=1)>0
        
        
        def single_point(asset,date,seq_len):
            pre_date = seek_backward_dates.loc[date]
            n = none_num.loc[asset].loc[pre_date:date]
            
            if n.sum() > seq_len*0.1:
                return None
            else:
                df = factor.loc[asset].loc[:date].ffill().iloc[-seq_len:].values
                if np.isnan(df).sum() > 0:
                    return None
                if len(df) != seq_len:
                    return None
                return ((asset,date),df)
        
        X_ = []
        label = []

        index = []
        
        forward_returns = []
        for fw in forward:
            forward_returns.append((price.shift(-fw)/price - 1))
        
        for date in dates:
            y_ = []
            for i in range(len(forward_returns)):
                y_.append(forward_returns[i].loc[date])
            y_ = pd.concat(y_,axis=1).dropna()
            if len(y_) == 0:
                continue
            for asset in y_.index:
                dv = single_point(asset,date,seq_len)
                if dv is None:
                    continue
                
                X_.append(dv[1])
                label.append(y_.loc[asset].values)
                index.append(dv[0])

        if dtype == 'float':
            X_ = torch.tensor(np.array(X_)).float()
            label = torch.tensor(np.array(label)).float()
        else:
            X_ = torch.tensor(np.array(X_)).float()
            label = torch.tensor(np.array(label)).float()
            
        index = pd.MultiIndex.from_tuples(index,names=['asset','date'])
        
        return (index,TensorDataset(X_,label))
    
    @staticmethod
    def Seq_None_train_dataset(factor,price,dates,seq_len,forward:int=7,none_num=None,dtype='float',assets=None):
        """
        Introduce:
        主要添加了空缺值的处理逻辑，同时尽量不损失数据，空缺比例高于10%则丢弃，否则用ffill填补空缺值. 得到的标签是未来forward日的收益率序列，用于更加复杂的标签构造分析。
        
        Params:
        -factor: pd.DataFrame. index=pd.MultiIndex, level0 = asset, level1 = date;
        -price: pd.DataFrame. index=date, columns = asset
        -dates: list(datetime). 提供你要生成数据点的时间点，将逐次生成训练数据，可通过控制这个参数防止偷看未来数据
        -seq_len: int. 获取的因子矩阵的时序长度
        -forward: int. 获取的未来收益率长度, 输出的标签为未来forward天的收益率序列，可以构造夏普比等特殊标签
        -dropmid=None: float. 在进行标签筛选时是否扔掉中间的部分数据
        -dtype='float': str. 
        -assets=None: list. 提供你筛选后的股票，如果没有则默认为price表提供的股票
        -none_num: Serier. index=pd.MultiIndex, level0 = asset, level1 = date. 提供因子每一行是否有空缺值的bool值Series，不提供会内部计算，有点慢.
        
        Return:
        (index,dataset): 与dataset相对应的index, 方便直接使用训练集输出测试预测因子
        
        Attention: 
        - 建议你提供的数据相对于时间点来说要足够长, 否则会丢弃很多长度不够的数据点。
        - 对于时间点前seqlen长度的数据，若空缺比例超过0.1会丢弃该数据点，所以请在因子输入时dropna
        """
        seek_backward_dates = Series(trade_dates,index=trade_dates).shift(seq_len).dropna()
        if assets is None:
            assets = list(set(list(factor.index.get_level_values(0))) & set(list(price.columns)))
        else:
            assets = list(set(list(assets)) & set(list(factor.index.get_level_values(0))) & set(list(price.columns)))
        price:DataFrame = price[assets]
        returns = price.pct_change()
        if none_num is None:
            none_num = factor.isna().sum(axis=1)>0
        
        
        def single_point(asset,date,seq_len):
            pre_date = seek_backward_dates.loc[date]
            n = none_num.loc[asset].loc[pre_date:date]
            
            if n.sum() > seq_len*0.1:
                return None
            else:
                df = factor.loc[asset].loc[:date].ffill().iloc[-seq_len:].values
                if np.isnan(df).sum() > 0:
                    return None
                if len(df) != seq_len:
                    return None
                return ((asset,date),df)
        
        X_ = []
        label = []

        index = []
        forward_returns = []
        for i in range(forward):
            forward_returns.append(returns.shift(-i-1).stack(dropna=False))
        forward_returns = pd.concat(forward_returns,axis=1).sort_index()
        for date in dates:
            y_ = forward_returns.loc[date].dropna()
            if len(y_) == 0:
                continue
            for asset in y_.index:
                dv = single_point(asset,date,seq_len)
                if dv is None:
                    continue
                
                X_.append(dv[1])
                label.append(y_.loc[asset].values)
                index.append(dv[0])

        if dtype == 'float':
            X_ = torch.tensor(np.array(X_)).float()
            label = torch.tensor(np.array(label)).float()
        else:
            X_ = torch.tensor(np.array(X_)).float()
            label = torch.tensor(np.array(label)).float()
            
        index = pd.MultiIndex.from_tuples(index,names=['asset','date'])
        
        return (index,TensorDataset(X_,label))
        



class ClassifyModelFrame(DLmodel):
    """
    Introduce:
        基于分类DL模型的训练和测试框架
    
    Function:
    - __init__:提供你的模型设计和模型参数设定，会自动帮你生成和存储模型，继承DLmodel方法
    - train: 提供你的训练数据集，批次大小，训练轮次，早停条件，学习率等，分类模型设定为F1score达标早停，函数内部会对你的非分类标签依据gap变化为分类标签，故你不需要做标签预处理
    - test: 提供你的测试集数据，和同样顺序的index
    """
    def __init__(self, model_params: dict, class_model, dtype='float') -> None:
        super().__init__(model_params, class_model, dtype)
    
    def train(self,dataset,EPOCHS,batch_size=512,scale=100,shuffle=True,lr=0.001,stop = 100,gap=[-0.005,0.005]):
        typenum = len(gap)+1
        gap = torch.tensor(gap).cuda()*scale
        dataloader = DataLoader(dataset, batch_size=batch_size, shuffle=shuffle)
        loss_func = nn.CrossEntropyLoss()
        optim = torch.optim.Adam(self.model.parameters(),lr=lr)
        
        for epoch in range(EPOCHS):
            self.model.train()
            epoch_f1score = []
            epoch_precision = []
            epoch_recall = []
            epoch_loss = []
            for batch_idx, (data,target) in enumerate(dataloader):
                data = data.float().cuda()
                target = target.float().cuda()*scale
                label = target.reshape(-1)
                label = torch.bucketize(label,gap)
                
                optim.zero_grad()
                output = self.model(data)
                
                l = loss_func(output,label)
                
                pred = torch.argmax(F.softmax(output,dim=1), dim=1)
                score = self.f1_score(pred,label,typenum=typenum)
                
                epoch_f1score.append(score[0])
                epoch_precision.append(score[1])
                epoch_recall.append(score[2])
                epoch_loss.append(l.item())


                l.backward()
                optim.step()
                
                if batch_idx % 50 == 0:
                    print("train epoch:{}, batch_idx:{}, loss: {:.4f}, f1_score:{:.4f}, precision:{:.4f}, recall:{:.4f}".format(epoch+1,batch_idx,l.item(),score[0],score[1],score[2]))
            
            epoch_f1score = sum(epoch_f1score)/len(epoch_f1score)
            epoch_precision = sum(epoch_precision)/len(epoch_precision)
            epoch_recall = sum(epoch_recall)/len(epoch_recall)
            epoch_loss = sum(epoch_loss)/len(epoch_loss)
            
            if epoch_f1score.mean() > stop:
                print("STOP: train epoch:{}, loss:{:.4f}, f1_score:{:.4f}, precision:{:.4f}, recall:{:.4f}".format(epoch+1,epoch_loss,epoch_f1score,epoch_precision,epoch_recall))
                print("")
                break
            
            print("FINISH: train epoch:{}, loss:{:.4f}, f1_score:{:.4f}, precision:{:.4f}, recall:{:.4f}".format(epoch+1,epoch_loss,epoch_f1score,epoch_precision,epoch_recall))
            print("")

        return 1
    
    
    @staticmethod
    def test(data:torch.tensor,index,model,batch_size=1024):
        model = model.cuda()
        result = []
        with torch.no_grad():
            model.eval()
            for i in range(0,data.shape[0],batch_size):
                feature = data[i:i+batch_size].float().cuda()
                label = F.softmax(model(feature),dim=1).cpu().detach().numpy()
                result.append(label)
        result = np.vstack(result)
        factor = DataFrame(result,index=index).sort_index()
        return factor
    
    
    
class RegresionModelFrame(DLmodel):
    
    """
    Introduce:
        基于回归DL模型的训练和测试框架
    
    Function:
    - __init__:提供你的模型设计和模型参数设定，会自动帮你生成和存储模型，继承DLmodel方法
    - train: 提供你的训练数据集，批次大小，训练轮次，早停条件，学习率等，回归训练以R2score达标作为早停条件
    - test: 提供你的测试集数据，和同样顺序的index
    """
    
    def __init__(self, model_params, class_model,dtype='float') -> None:
        super().__init__(model_params, class_model, dtype)
        
    def train(self,dataset,EPOCHS,batch_size=512,scale=100,shuffle=True,loss='Huber', lr=0.001, stop = 100):
        dataloader = DataLoader(dataset, batch_size=batch_size, shuffle=shuffle)
        
        if loss == 'Huber':
            loss_func = nn.HuberLoss()
        elif loss == 'L1':
            loss_func = nn.L1Loss()
        elif loss == 'MSE': 
            loss_func = nn.MSELoss()
        else:
            loss_func = nn.MSELoss()

        
        optim = torch.optim.Adam(self.model.parameters(),lr=lr)
        loss_lst = []
        r2score_lst = []
        for epoch in range(EPOCHS):
            self.model.train()
            epoch_r2score = []
            epoch_loss = []
            for batch_idx, (data,target) in enumerate(dataloader):
                
                data = data.float().cuda()
                target = target.float().cuda()*scale
                optim.zero_grad()
                output = self.model(data)
                
                l = loss_func(output,target)
    
                r2score = self.r2_score(target,output)[0].item()
                epoch_r2score.append(r2score)
                epoch_loss.append(l.item())
                
                l.backward()
                
                optim.step()
                
                if batch_idx % 50 == 0:
                    print("train epoch:{}, batch_idx:{}, loss: {:.4f}, R2_score:{:.4f}".format(epoch+1,batch_idx,l.item(),r2score))
            
            epoch_r2score = np.array(epoch_r2score)
            epoch_loss = np.array(epoch_loss)
            if epoch_r2score.mean() > stop:
                print("STOP: train epoch:{}, loss:{:.4f}, R2_score:{:.4f}".format(epoch+1,epoch_loss.mean(),epoch_r2score.mean()))
                print("")
                break
            print("FINISH: train epoch:{}, loss:{:.4f}, R2_score:{:.4f}".format(epoch+1,epoch_loss.mean(),epoch_r2score.mean()))
            print("")
                
        
        self._r2score_lst = r2score_lst
        self._loss_lst = loss_lst
        
        return 1
    
    @staticmethod
    def test(data:torch.tensor,index,model,batch_size=2048):
        model = model.cuda()
        result = []
        with torch.no_grad():
            model.eval()
            for i in range(0,data.shape[0],batch_size):
                feature = data[i:i+batch_size].float().cuda()
                label = model(feature).cpu().detach().numpy()
                result.append(label)
        result = np.vstack(result)
        factor = DataFrame(result,index=index).sort_index()
        return factor