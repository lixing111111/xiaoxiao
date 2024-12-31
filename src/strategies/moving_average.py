import numpy as np
import pandas as pd

class MovingAverageStrategy:
    def __init__(self, fast_period=5, slow_period=20):
        self.fast_period = fast_period
        self.slow_period = slow_period
        self.position = 0  # -1: 空仓, 0: 无仓位, 1: 多仓
    
    def calculate_signals(self, ohlcv_data):
        """计算交易信号"""
        # 将 OHLCV 数据转换为 DataFrame
        df = pd.DataFrame(ohlcv_data, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
        
        # 计算快速和慢速移动平均线
        df['fast_ma'] = df['close'].rolling(window=self.fast_period).mean()
        df['slow_ma'] = df['close'].rolling(window=self.slow_period).mean()
        
        # 计算金叉和死叉信号
        df['golden_cross'] = (df['fast_ma'] > df['slow_ma']) & (df['fast_ma'].shift(1) <= df['slow_ma'].shift(1))
        df['death_cross'] = (df['fast_ma'] < df['slow_ma']) & (df['fast_ma'].shift(1) >= df['slow_ma'].shift(1))
        
        return df
    
    def generate_signals(self, ohlcv_data):
        """生成交易信号"""
        df = self.calculate_signals(ohlcv_data)
        
        # 获取最新的信号
        latest = df.iloc[-1]
        signal = {
            'timestamp': latest['timestamp'],
            'price': latest['close'],
            'action': 'hold',  # 默认持仓不变
            'position_size': 0
        }
        
        # 根据信号生成交易动作
        if latest['golden_cross'] and self.position <= 0:
            signal['action'] = 'buy'
            signal['position_size'] = 1
            self.position = 1
        elif latest['death_cross'] and self.position >= 0:
            signal['action'] = 'sell'
            signal['position_size'] = -1
            self.position = -1
        
        return signal
    
    def calculate_position_size(self, balance, current_price, risk_percentage=0.02):
        """计算仓位大小"""
        # 使用账户余额的 risk_percentage 作为每次交易的最大损失
        position_size = (balance * risk_percentage) / current_price
        return round(position_size, 8)  # 根据交易所的精度要求调整 