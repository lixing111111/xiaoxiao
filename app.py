from flask import Flask, render_template, jsonify, request
from src.services.trading_service import TradingService
from src.utils.okx_client import OKXClient
import threading
import os
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

app = Flask(__name__)

# 全局变量存储交易服务实例
trading_service = None
trading_thread = None

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/start', methods=['POST'])
def start_trading():
    global trading_service, trading_thread
    
    try:
        if trading_service and trading_service.active:
            return jsonify({'success': False, 'message': 'Trading service is already running'})
        
        # 从请求中获取参数
        data = request.get_json()
        symbol = data.get('symbol', 'BTC/USDT')
        fast_period = int(data.get('fast_period', 5))
        slow_period = int(data.get('slow_period', 20))
        
        # 创建并启动交易服务
        trading_service = TradingService(symbol, fast_period, slow_period)
        trading_thread = threading.Thread(target=trading_service.start)
        trading_thread.start()
        
        return jsonify({'success': True, 'message': f'Trading service started for {symbol}'})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@app.route('/api/stop', methods=['POST'])
def stop_trading():
    global trading_service
    
    try:
        if not trading_service or not trading_service.active:
            return jsonify({'success': False, 'message': 'Trading service is not running'})
        
        trading_service.stop()
        return jsonify({'success': True, 'message': 'Trading service stopped'})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@app.route('/api/status')
def get_status():
    global trading_service
    
    try:
        client = OKXClient()
        balance = client.get_balance()
        
        status = {
            'running': trading_service.active if trading_service else False,
            'symbol': trading_service.symbol if trading_service else None,
            'balance': balance
        }
        
        return jsonify({'success': True, 'data': status})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3000) 