// 页面加载完成后执行
document.addEventListener('DOMContentLoaded', function() {
    // 加载历史数据
    loadHistoryData();
    
    // 绑定预测按钮点击事件
    document.getElementById('predict-btn').addEventListener('click', getPrediction);
});

// 加载历史数据
async function loadHistoryData() {
    try {
        const response = await fetch('/api/history');
        const data = await response.json();
        
        // 获取表格tbody元素
        const tbody = document.querySelector('#history-table tbody');
        tbody.innerHTML = ''; // 清空现有内容
        
        // 按日期降序排序
        data.sort((a, b) => new Date(b.日期) - new Date(a.日期));
        
        // 添加数据行
        data.forEach(row => {
            const tr = document.createElement('tr');
            tr.innerHTML = `
                <td>${formatDate(row.日期)}</td>
                <td>${row.号码1}</td>
                <td>${row.号码2}</td>
                <td>${row.号码3}</td>
                <td>${row.号码4}</td>
            `;
            tbody.appendChild(tr);
        });
    } catch (error) {
        console.error('加载历史数据失败:', error);
        alert('加载历史数据失败，请刷新页面重试');
    }
}

// 获取预测结果
async function getPrediction() {
    const button = document.getElementById('predict-btn');
    const display = document.getElementById('prediction-display');
    
    try {
        // 更改按钮状态
        button.disabled = true;
        button.textContent = '预测中...';
        
        // 发送预测请求
        const response = await fetch('/api/predict');
        const data = await response.json();
        
        // 显示预测结果
        document.getElementById('next-date').textContent = data.next_date;
        for (let i = 0; i < 4; i++) {
            document.getElementById(`pred${i+1}`).textContent = data.predictions[i];
        }
        
        // 显示预测结果区域
        display.classList.remove('d-none');
    } catch (error) {
        console.error('预测失败:', error);
        alert('预测失败，请重试');
    } finally {
        // 恢复按钮状态
        button.disabled = false;
        button.textContent = '获取预测结果';
    }
}

// 格式化日期
function formatDate(dateStr) {
    const date = new Date(dateStr);
    const year = date.getFullYear();
    const month = String(date.getMonth() + 1).padStart(2, '0');
    const day = String(date.getDate()).padStart(2, '0');
    return `${year}/${month}/${day}`;
} 