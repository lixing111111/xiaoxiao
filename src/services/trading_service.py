from src.utils.okx_client import OKXClient
from src.strategies.moving_average import MovingAverageStrategy
import time

class TradingService:
    def __init__(self, symbol='BTC/USDT', fast_period=5, slow_period=20):
        self.client = OKXClient()
        self.strategy = MovingAverageStrategy(fast_period, slow_period)
        self.symbol = symbol
        self.active = False
        self.last_order_time = 0
        self.min_order_interval = 60  # 最小下单间隔（秒）
    
    def start(self):
        """启动交易服务"""
        self.active = True
        print(f"Trading service started for {self.symbol}")
        
        while self.active:
            try:
                self.execute_trading_cycle()
                time.sleep(60)  # 每分钟执行一次
            except Exception as e:
                print(f"Error in trading cycle: {str(e)}")
                time.sleep(60)  # 发生错误时等待一分钟
    
    def stop(self):
        """停止交易服务"""
        self.active = False
        print("Trading service stopped")
    
    def execute_trading_cycle(self):
        """执行一个完整的交易周期"""
        # 获取最新行情数据
        ohlcv_data = self.client.get_ohlcv(self.symbol, timeframe='1m', limit=100)
        if not ohlcv_data:
            return
        
        # 生成交易信号
        signal = self.strategy.generate_signals(ohlcv_data)
        
        # 检查是否需要执行交易
        if signal['action'] != 'hold':
            # 检查下单时间间隔
            current_time = time.time()
            if current_time - self.last_order_time < self.min_order_interval:
                return
            
            # 获取账户余额
            balance = self.client.get_balance()
            if not balance:
                return
            
            # 计算仓位大小
            position_size = self.strategy.calculate_position_size(
                balance.get('USDT', 0),
                signal['price']
            )
            
            # 执行交易
            if signal['action'] == 'buy':
                order = self.client.create_order(
                    symbol=self.symbol,
                    order_type='market',
                    side='buy',
                    amount=position_size
                )
                if order:
                    print(f"Buy order executed: {order}")
                    self.last_order_time = current_time
            
            elif signal['action'] == 'sell':
                order = self.client.create_order(
                    symbol=self.symbol,
                    order_type='market',
                    side='sell',
                    amount=position_size
                )
                if order:
                    print(f"Sell order executed: {order}")
                    self.last_order_time = current_time 