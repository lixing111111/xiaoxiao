from flask import Flask, render_template, jsonify, request
from src.utils.okx_client import OKXClient
import os
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/status')
def get_status():
    try:
        client = OKXClient()
        ticker = client.get_ticker('BTC/USDT')
        
        return jsonify({
            'success': True,
            'data': {
                'running': False,
                'ticker': ticker
            }
        })
    except Exception as e:
        print(f"Error in status: {str(e)}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

# 添加健康检查端点
@app.route('/health')
def health():
    return jsonify({'status': 'ok'})

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=port) 