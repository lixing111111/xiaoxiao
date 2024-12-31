from flask import Flask, render_template, jsonify
from datetime import datetime

app = Flask(__name__)

# 预定义的预测结果
PREDICTIONS = {
    'next_date': '2024/12/31',
    'predictions': [3, 3, 3, 2]
}

# 预定义的历史数据
HISTORY_DATA = [
    {
        "date": "2024/12/29",
        "numbers": [2, 2, 0, 4]
    },
    {
        "date": "2024/12/28",
        "numbers": [9, 0, 7, 3]
    },
    {
        "date": "2024/12/27",
        "numbers": [1, 9, 2, 0]
    }
]

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
        return jsonify({
            'success': True,
            'data': HISTORY_DATA
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }) 