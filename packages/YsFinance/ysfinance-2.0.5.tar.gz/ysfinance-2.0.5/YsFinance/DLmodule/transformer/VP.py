import pandas as pd
from pandas import DataFrame,Series
import numpy as np

import torch 
from torch.utils.data import TensorDataset, DataLoader
import torch.nn as nn
import torch.nn.functional as F
from math import log

from ...stockcalendar import CALENDAR_TOOL
import matplotlib.pyplot as plt


from ..util import DLmodel,ByTimeDataLoader


trade_dates = Series(CALENDAR_TOOL.trade_date_in_range('2001-01-01','2026-01-01'),index = CALENDAR_TOOL.trade_date_in_range('2001-01-01','2026-01-01'))


class PositionalEncoding(nn.Module):
    """
    位置编码
    """
    def __init__(self, d_model, max_len=1000):
        super(PositionalEncoding, self).__init__()
        # 创建一个足够长的P
        pe = torch.zeros(max_len, d_model)
        position = torch.arange(0, max_len, dtype=torch.float).unsqueeze(1)
        div_term = torch.exp(torch.arange(0, d_model, 2).float() * (-log(10000.0) / d_model))
        pe[:, 0::2] = torch.sin(position * div_term)
        pe[:, 1::2] = torch.cos(position * div_term)
        pe = pe.unsqueeze(0).transpose(0, 1)
        self.register_buffer('pe', pe)

    def forward(self, x):
        x = x + self.pe[:x.size(0), :]
        return x
    

class ResidualBlock(nn.Module):
    def __init__(self, in_channels, out_channels, stride=1, downsample=None):
        super(ResidualBlock, self).__init__()
        self.conv1 = nn.Conv2d(in_channels, out_channels, kernel_size=3, stride=stride, padding=1, bias=False)
        # self.bn1 = nn.BatchNorm2d(out_channels)
        self.relu = nn.ReLU(inplace=True)
        self.conv2 = nn.Conv2d(out_channels, out_channels, kernel_size=3, stride=1, padding=1, bias=False)
        # self.bn2 = nn.BatchNorm2d(out_channels)
        self.downsample = downsample

    def forward(self, x):
        identity = x

        out = self.conv1(x)
        out = self.relu(out)
        out = self.conv2(out)

        if self.downsample:
            identity = self.downsample(x)

        out += identity
        out = self.relu(out)

        return out
    

    
class Transformer5(nn.Module):
    """
    实现input_dim * seq_len -> output_dim 的基本的Transformer模型的架构, 不要前馈网络，直接跟编码器，让编码器直接提取数据特征
    """
    def __init__(self, input_dim, d_model, num_heads, num_layers, output_dim, dim_feedforward,drop_rate, backward):
        super(Transformer5, self).__init__()
        
        self.d_model = d_model
        self.backward = backward
        self.aft_dropout = nn.Dropout(drop_rate)
        
        self.pre_layer = nn.Linear(input_dim,d_model)
        
        # 编码器层
        self.pos_encoder = PositionalEncoding(self.d_model, max_len=500)
        self.encoder_layer = nn.TransformerEncoderLayer(
            d_model=self.d_model,
            nhead=num_heads,
            dim_feedforward=dim_feedforward,
            dropout=drop_rate,
            activation='relu',
            batch_first=True,
            # attn_weights_need=attn_weights_need
        )
        
        # 编码器
        self.encoder = nn.TransformerEncoder(self.encoder_layer, num_layers=num_layers)
        
        # 输出层
        self.fc1 = nn.Linear(backward*self.d_model, 500)
        self.fc2 = nn.Linear(500,100)
        self.fc3 = nn.Linear(100,output_dim)
        
        # self.init_weights()
        
    def forward(self, x):
        # x: (batch_size, seq_length, input_dim)
        
        ### 添加位置编码
        x = self.pre_layer(x)
        x = self.pos_encoder(x.transpose(0,1)).transpose(0,1)
        
        x = self.encoder(x)
        
        
        # 拼接最后若干时间步的数据再跟全连接网络
        out = x[:,-self.backward:,:].reshape(-1,self.backward*self.d_model)
        # 通过全连接层得到最终输出
        out = F.relu(self.fc1(out))
        out = self.aft_dropout(out)
        out = F.relu(self.fc2(out))
        out = self.fc3(out)
        
        return out
    


    
    

class FactorTransformer(DLmodel):
    
    def __init__(self, model_params, class_model=Transformer5,dtype='float') -> None:
        super().__init__(model_params, class_model, dtype)
        
    def train(self,dataset,EPOCHS,batch_size=512,scale=100,shuffle=True,loss='Huber', lr=0.001, stop = 100):
        dataloader = DataLoader(dataset, batch_size=batch_size, shuffle=shuffle)
        
        if loss == 'Huber':
            loss_func = nn.HuberLoss()
        elif loss == 'MSE':
            loss_func = nn.MSELoss()
        elif loss == 'L1':
            loss_func = nn.L1Loss()
        
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
                # print(output.shape)
                # print(target.shape)
                
                l = loss_func(output,target)
                if torch.isnan(l):
                    print(data.isnan().sum())
                    print(data.max())
                    print(data.min())
                    print(output.isnan().sum())
                    print(output.max())
                    print(output.min())
                    print(target.isnan().sum())
                    print(target.max())
                    print(target.min())
                    
                    return 0
    
                r2score = self.r2_score(target,output)[0].item()
                epoch_r2score.append(r2score)
                epoch_loss.append(l.item())
                
                l.backward()
                
                optim.step()
                
                if batch_idx % 20 == 0:
                    print("train epoch:{}, batch_idx:{}, loss: {:.4f}, R2_score:{:.4f}".format(epoch+1,batch_idx,l.item(),r2score))
            
            epoch_r2score = np.array(epoch_r2score)
            epoch_loss = np.array(epoch_loss)
            if epoch_r2score.mean() > stop:
                print("STOP: train epoch:{}, loss:{:.4f}, R2_score:{:.4f}".format(epoch+1,epoch_loss.mean(),epoch_r2score.mean()))
                print("")
                break
            print("FINISH: train epoch:{}, loss:{:.4f}, R2_score:{:.4f}".format(epoch+1,epoch_loss.mean(),epoch_r2score.mean()))
            print("")
            torch.save(self.model,'model.backup')
                
        
        self._r2score_lst = r2score_lst
        self._loss_lst = loss_lst
        
        return 1
        
    def train_by_time(self,dataset,EPOCHS,loss='Huber', lr=0.001,scale=100,seed=42):
        dataloader = ByTimeDataLoader(dataset)
        torch.manual_seed(seed)
        
        if loss == 'Huber':
            loss_func = nn.HuberLoss()
        else:
            loss_func = nn.MSELoss()
        
        optim = torch.optim.AdamW(self.model.parameters(),lr=lr,weight_decay=0.01)
        loss_lst = []
        r2score_lst = []
        for epoch in range(EPOCHS):
            self.model.train()

            for batch_idx, (data,target) in enumerate(dataloader):
                data = data.float().cuda()
                target = target.float().cuda()*scale
                optim.zero_grad()
                output = self.model(data)
                # print(output.shape)
                # print(target.shape)
                
                l = loss_func(output,target)
                r2score = self.r2_score(target,output)[0].item()
                r2score_lst.append(r2score)
                loss_lst.append(l.item())
                l.backward()
                optim.step()
                
                if batch_idx % 20 == 0:
                    print("train epoch:{}, batch_idx:{}, loss: {:.4f}, R2_score:{:.4f}".format(epoch+1,batch_idx,l.item(),r2score))
        
        self._r2score_lst = r2score_lst
        self._loss_lst = loss_lst
        
    
    def plot(self,skip=10):
        fig, (ax1,ax2) = plt.subplots(1,2,figsize=(4,8))
        ax1.plot(np.arange(len(self._loss_lst[::skip])),self._loss_lst[::skip], label='loss')
        ax1.set_xlabel('batch_idx')
        ax1.set_ylabel('loss')
        ax1.legend(loc='best')
        
        ax2.plot(np.arange(len(self._r2score_lst[::skip])),self._r2score_lst[::skip], label='r2-score')
        ax2.set_xlabel('batch_idx')
        ax2.set_ylabel('r2-score')
        ax2.legend(loc='best')

        
    def r2_score(self,target:torch.tensor,output:torch.tensor):
        # 计算总平方和 (SStot)
        mean_target = torch.mean(target,dim=0)
        total_sum_squares = torch.sum((target - mean_target) ** 2,dim=0)

        # 计算残差平方和 (SSres)
        residual_sum_squares = torch.sum((target - output) ** 2,dim=0)

        # 计算R² score
        r2score = 1 - (residual_sum_squares / total_sum_squares)
        return r2score
    
    def reload_model(self):
        self.model = torch.load('model.backup')
    
    @staticmethod
    def gen_train_data_set(prices, factors, train_slice, move_step, seq_len, forward, drop_mid = 0, dtype='float',by_time=False) -> TensorDataset:
        """
        基于此模型的训练集生成方法，单股票序列矩阵->收益率值，训练集生成函数
        
        params:
        - prices(pd.DataFrame): index为datetime格式, columns为资产名
        - factor(pd.DataFrame): index为multiindex, 分别为(asset,date)
        - model_set(ModelSet): 使用ModelSet的train_params设置生成训练集
        - drop_mid(float(0,1)): drop掉收益率中间的一定比例, 以提高训练集的有效性
        - dtype='float': 数据集的数据类型,默认使用float类型
        - by_time(Bool)=False: 如果设置为True,则生成的数据集是沿时间截面的,训练时可沿时间截面随机提取数据,但不保证每个时间点的批量大小的一致的
        
        return:
        - TensorDataset: by_time = False
        - List[data1(feature,label),data2,...]: by_time = True
        
        
        others:
        若数据时间点的前设定天数的比例有超过10%的空缺值比例, 或数据量有超过5%的数据空缺, 则丢弃该数据点,否则均值填充, 所以调用之前factor可不用dropna, 会自动处理空缺日期较多的数据点, prices可不用dropna, 空缺收益率数据会自动drop

        """
        def single_date_point_label(date, drop_mid):
            p = prices.loc[date:].iloc[:forward]
            y:Series = p.iloc[-1]/p.iloc[0]-1
            if drop_mid == 0:
                return y
            y = y.sort_values().dropna()
            keep_rate = (1-drop_mid)/2
            l = len(y)
            y = pd.concat([y.head(int(l*keep_rate)),y.tail(int(l*keep_rate))])
            return y
        
        def single_date_point_feature_label(date, label:Series):
            assets = label.index
            features = []
            labels = []
            for asset in assets:

                f = factors.loc[asset].loc[seek_forward_dates.loc[date]:date]
                if f.shape[0] < seq_len*0.9:
                    # print('pass1 asset:{}, date:{}, eff_length:{}'.format(asset,date,f.shape[0]))
                    continue
                f = factors.loc[asset].loc[:date].iloc[-seq_len:]
                if f.shape[0] != seq_len:
                    # print('pass2 asset:{}, date:{}, eff_length:{}'.format(asset,date,f.shape[0]))
                    continue
                if f.isna().sum().sum()/f.size > 0.05:
                    continue

                f = f.replace({np.inf: np.nan, -np.inf: np.nan}).fillna(0)


                features.append(f)
                labels.append(label.loc[asset])
            return features,labels
        
        def data_X_y(date_point, dtype, by_time):
            if by_time:
                dataset = []
                for date in date_point:
                    label = single_date_point_label(date,drop_mid)
                    feature,label = single_date_point_feature_label(date,label)
                    if dtype=='float':
                        feature = torch.tensor(np.array(feature)).float()
                        label = torch.tensor(np.array(label)).reshape(len(label),-1).float()
                        dataset.append((feature,label))
                    else:
                        feature = torch.tensor(np.array(feature))
                        label = torch.tensor(np.array(label)).reshape(len(label),-1)
                        dataset.append((feature,label))
                return dataset
            
            feature_set = []
            label_set = []
            for date in date_point:
                label = single_date_point_label(date,drop_mid)
                feature,label = single_date_point_feature_label(date,label)
                label_set += label
                feature_set += feature
            
            features = torch.tensor(np.array(feature_set))
            labels = torch.tensor(np.array(label_set).reshape(len(label_set),-1))
            # print(labels)
            if dtype == 'float':
                return TensorDataset(features.float(), labels.float())
            else:
                return TensorDataset(features, labels)
        
        start_date = train_slice.start
        end_date = train_slice.stop
        seek_forward_dates = trade_dates.shift(seq_len)
        train_date_point = CALENDAR_TOOL.trade_date_in_range(start_date,end_date,skip=move_step)[:-2]
        train_data_set = data_X_y(train_date_point,dtype,by_time)
        return train_data_set
    
    
    
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