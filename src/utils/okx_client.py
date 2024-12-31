import os
import ccxt
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

class OKXClient:
    def __init__(self):
        self.api_key = os.getenv('OKX_API_KEY', '')
        self.secret_key = os.getenv('OKX_SECRET_KEY', '')
        self.passphrase = os.getenv('OKX_PASSPHRASE', '')
        self.use_testnet = os.getenv('USE_TESTNET', 'true').lower() == 'true'
        
        # 初始化 CCXT OKX 客户端
        self.exchange = ccxt.okx({
            'apiKey': self.api_key,
            'secret': self.secret_key,
            'password': self.passphrase,
            'enableRateLimit': True,
            'options': {
                'defaultType': 'spot',
                'test': self.use_testnet
            }
        })
        
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
                'volume': ticker['baseVolume']
            }
        except Exception as e:
            print(f"Error fetching ticker: {str(e)}")
            return None 