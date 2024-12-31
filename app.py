from flask import Flask, render_template, jsonify

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/status')
def get_status():
    try:
        # 使用模拟数据
        ticker = {
            'symbol': 'BTC/USDT',
            'last': 42000.00,
            'bid': 41999.00,
            'ask': 42001.00,
            'volume': 1000.00
        }
        
        return jsonify({
            'success': True,
            'data': {
                'running': True,
                'ticker': ticker
            }
        })
    except Exception as e:
        print(f"Error in status: {str(e)}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/health')
def health():
    return jsonify({'status': 'ok'})

if __name__ == '__main__':
    app.run() 