from flask import Flask, render_template, jsonify
import logging

app = Flask(__name__)

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@app.route('/')
def index():
    try:
        logger.info("访问主页")
        return render_template('index.html')
    except Exception as e:
        logger.error(f"主页错误: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/status')
def get_status():
    try:
        logger.info("检查状态")
        return jsonify({
            'success': True,
            'status': 'running'
        })
    except Exception as e:
        logger.error(f"状态检查错误: {str(e)}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/health')
def health():
    try:
        logger.info("健康检查")
        return jsonify({'status': 'ok'})
    except Exception as e:
        logger.error(f"健康检查错误: {str(e)}")
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run() 