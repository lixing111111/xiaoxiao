from flask import Flask, render_template, jsonify
import pandas as pd
from datetime import datetime
import yuxhe

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/predict')
def predict():
    try:
        # 获取预测结果
        prediction = yuxhe.predict_next()
        return jsonify({
            'success': True,
            'prediction': prediction,
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
        # 获取历史数据
        history_data = yuxhe.get_history_data()
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