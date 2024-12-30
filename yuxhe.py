import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from sklearn.ensemble import GradientBoostingRegressor

# 原始数据
dates = [
    "2023/10/1", "2023/10/2", "2023/10/3", "2023/10/4", "2023/10/5",
    "2023/10/6", "2023/10/7", "2023/10/8", "2023/10/9", "2023/10/10",
    "2023/10/11", "2023/10/12", "2023/10/13", "2023/10/14", "2023/10/15"
]

numbers = [
    [1, 2, 3, 4], [5, 6, 7, 8], [9, 10, 11, 12], [13, 14, 15, 16],
    [17, 18, 19, 20], [21, 22, 23, 24], [25, 26, 27, 28], [29, 30, 31, 32],
    [33, 34, 35, 36], [37, 38, 39, 40], [41, 42, 43, 44], [45, 46, 47, 48],
    [1, 3, 5, 7], [2, 4, 6, 8], [9, 11, 13, 15]
]

def create_dataframe():
    """创建数据框架"""
    df = pd.DataFrame({
        '日期': dates,
        '号码1': [num[0] for num in numbers],
        '号码2': [num[1] for num in numbers],
        '号码3': [num[2] for num in numbers],
        '号码4': [num[3] for num in numbers]
    })
    df['日期'] = pd.to_datetime(df['日期'])
    return df

def create_features(df):
    """创建特征"""
    df = df.copy()
    df['月份'] = df['日期'].dt.month
    df['日'] = df['日期'].dt.day
    df['星期'] = df['日期'].dt.dayofweek
    
    # 创建滞后特征
    for i in range(1, 5):
        df[f'前一期号码{i}'] = df[f'号码{i}'].shift(1)
        df[f'前二期号码{i}'] = df[f'号码{i}'].shift(2)
    
    return df

def train_model(df, target_col):
    """训练模型"""
    features = ['月份', '日', '星期'] + \
               [f'前一期号码{i}' for i in range(1, 5)] + \
               [f'前二期号码{i}' for i in range(1, 5)]
    
    X = df.dropna()[features]
    y = df.dropna()[target_col]
    
    model = GradientBoostingRegressor(n_estimators=100, random_state=42)
    model.fit(X, y)
    return model

def predict_next():
    """预测下一期号码"""
    df = create_dataframe()
    df = create_features(df)
    
    last_date = df['日期'].max()
    next_date = last_date + timedelta(days=1)
    
    predictions = []
    for i in range(1, 5):
        model = train_model(df, f'号码{i}')
        
        # 准备预测特征
        pred_features = pd.DataFrame({
            '月份': [next_date.month],
            '日': [next_date.day],
            '星期': [next_date.dayofweek]
        })
        
        for j in range(1, 5):
            pred_features[f'前一期号码{j}'] = df.iloc[-1][f'号码{j}']
            pred_features[f'前二期号码{j}'] = df.iloc[-2][f'号码{j}']
        
        # 预测并取整
        pred = int(round(model.predict(pred_features)[0]))
        predictions.append(pred)
    
    return {
        'next_date': next_date.strftime('%Y/%m/%d'),
        'predictions': predictions
    }

def get_history_data():
    """获取历史数据"""
    df = create_dataframe()
    history = []
    
    for _, row in df.iterrows():
        history.append({
            '日期': row['日期'].strftime('%Y/%m/%d'),
            '号码1': int(row['号码1']),
            '号码2': int(row['号码2']),
            '号码3': int(row['号码3']),
            '号码4': int(row['号码4'])
        })
    
    return history 