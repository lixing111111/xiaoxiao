from flask import Flask, render_template, jsonify
from datetime import datetime
import json
import os

app = Flask(__name__)

# 预定义的预测结果（避免在 Vercel 上进行大量计算）
PREDICTIONS = {
    'next_date': '2024/12/31',
    'predictions': [3, 3, 3, 2]
}

# 从文件加载历史数据
def load_history_data():
    history_file = os.path.join(os.path.dirname(__file__), 'history.json')
    if os.path.exists(history_file):
        with open(history_file, 'r') as f:
            return json.load(f)
    return []

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/predict')
def predict():
    try:
        return jsonify({
            'success': True,
            'prediction': PREDICTIONS,
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        })

@app.route('/api/history')
def history():
    try:
        history_data = load_history_data()
        return jsonify({
            'success': True,
            'data': history_data
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        })

# Vercel 需要这个
app.debug = False

if __name__ == '__main__':
    app.run() 