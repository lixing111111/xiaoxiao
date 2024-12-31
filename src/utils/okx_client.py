import os
import ccxt
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

class OKXClient:
    def __init__(self):
        self.api_key = os.getenv('OKX_API_KEY')
        self.secret_key = os.getenv('OKX_SECRET_KEY')
        self.passphrase = os.getenv('OKX_PASSPHRASE')
        self.use_testnet = os.getenv('USE_TESTNET', 'true').lower() == 'true'
        
        # 初始化 CCXT OKX 客户端
        self.exchange = ccxt.okx({
            'apiKey': self.api_key,
            'secret': self.secret_key,
            'password': self.passphrase,
            'enableRateLimit': True,
            'options': {
                'defaultType': 'spot',  # 默认现货交易
                'test': self.use_testnet  # 使用测试网
            }
        })
        
        # 如果使用测试网
        if self.use_testnet:
            self.exchange.set_sandbox_mode(True)
    
    def get_ticker(self, symbol):
        """获取最新行情"""
        try:
            ticker = self.exchange.fetch_ticker(symbol)
            return {
                'symbol': symbol,
                'last': ticker['last'],
                'bid': ticker['bid'],
                'ask': ticker['ask'],
                'volume': ticker['baseVolume'],
                'timestamp': ticker['timestamp']
            }
        except Exception as e:
            print(f"Error fetching ticker: {str(e)}")
            return None
    
    def get_balance(self):
        """获取账户余额"""
        try:
            balance = self.exchange.fetch_balance()
            return balance['total']
        except Exception as e:
            print(f"Error fetching balance: {str(e)}")
            return None
    
    def create_order(self, symbol, order_type, side, amount, price=None):
        """创建订单"""
        try:
            order = self.exchange.create_order(
                symbol=symbol,
                type=order_type,
                side=side,
                amount=amount,
                price=price
            )
            return order
        except Exception as e:
            print(f"Error creating order: {str(e)}")
            return None
    
    def cancel_order(self, order_id, symbol):
        """取消订单"""
        try:
            return self.exchange.cancel_order(order_id, symbol)
        except Exception as e:
            print(f"Error canceling order: {str(e)}")
            return None
    
    def get_ohlcv(self, symbol, timeframe='1m', limit=100):
        """获取K线数据"""
        try:
            ohlcv = self.exchange.fetch_ohlcv(symbol, timeframe, limit=limit)
            return ohlcv
        except Exception as e:
            print(f"Error fetching OHLCV data: {str(e)}")
            return None 