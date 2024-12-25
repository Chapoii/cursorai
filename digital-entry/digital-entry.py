print("Hello, World!")
import random
from flask import Flask, render_template_string

app = Flask(__name__)
HTML_TEMPLATE = '''
<!DOCTYPE html>
<html>
<head>
    <title>数字录入练习</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 40px; }
        .container { display: flex; justify-content: space-around; }
        .number-list { font-size: 24px; line-height: 1.5; flex: 1; max-width: 45%; }
        .number { margin: 10px 0; display: flex; align-items: center; }
        .number input { margin-left: 10px; font-size: 20px; padding: 5px; width: 120px; }
        .timer { margin-left: 10px; font-size: 16px; color: #666; }
        .timer.slow { background-color: #fff3cd; }
        .total-time { margin-left: 20px; color: red; font-size: 20px; }
        .control-panel { margin-bottom: 20px; }
        button { font-size: 16px; padding: 8px 16px; margin-right: 10px; }
        .error { background-color: #ffebee; }
        .error input { border-color: red; }
        .number-display { width: 120px; }
    </style>
    <script>
        let startTimes = {};
        let globalStartTime = null;
        let entryTimes = {};
        
        function startEntry() {
            globalStartTime = new Date();
            document.getElementById('start-btn').disabled = true;
            document.getElementById('finish-btn').disabled = false;
            const inputs = document.querySelectorAll('input[type="number"]');
            inputs.forEach(input => {
                input.disabled = false;
                input.value = ''; // 清空输入框
                input.parentElement.classList.remove('error'); // 清除错误标记
            });
            document.getElementById('total-time').textContent = '';
            // 自动聚焦到第一个输入框
            inputs[0].focus();
            // 重置录入时间记录
            entryTimes = {};
        }

        function finishEntry() {
            if (!globalStartTime) return;
            const endTime = new Date();
            const totalTime = (endTime - globalStartTime) / 1000;
            document.getElementById('total-time').textContent = '总耗时: ' + totalTime.toFixed(2) + '秒';
            document.getElementById('start-btn').disabled = false;
            document.getElementById('finish-btn').disabled = true;
            
            // 计算平均录入时间
            let totalEntryTime = 0;
            let validEntryCount = 0;
            
            for (let time of Object.values(entryTimes)) {
                if (time > 0) {
                    totalEntryTime += time;
                    validEntryCount++;
                }
            }
            
            const averageTime = totalEntryTime / validEntryCount;
            
            // 检查输入是否正确并标记高于平均时间的录入
            document.querySelectorAll('.number').forEach(numberDiv => {
                const input = numberDiv.querySelector('input');
                const originalNumber = numberDiv.querySelector('.number-display').textContent.trim();
                const inputId = input.getAttribute('data-id');
                const timerSpan = document.getElementById('timer-' + inputId);
                
                input.disabled = true;
                
                if (input.value !== originalNumber) {
                    numberDiv.classList.add('error');
                    console.log(`原始数字: ${originalNumber}, 录入数字: ${input.value}`);
                }
                
                // 标记高于平均时间的录入
                if (entryTimes[inputId] > averageTime) {
                    timerSpan.classList.add('slow');
                }
            });
        }

        function handleInput(input) {
            const currentTime = new Date();
            const inputId = input.getAttribute('data-id');
            const timerSpan = document.getElementById('timer-' + inputId);
            
            if (input.value.length > 0) {
                // 如果没有开始时间，则设置开始时间
                if (!startTimes[inputId]) {
                    startTimes[inputId] = new Date();
                }
                const timeTaken = (currentTime - startTimes[inputId]) / 1000;
                timerSpan.textContent = timeTaken.toFixed(2) + '秒';
                entryTimes[inputId] = timeTaken;
            } else {
                timerSpan.textContent = '';
                // 删除这两行，不再重置开始时间和录入时间
                // delete startTimes[inputId];
                // delete entryTimes[inputId];
            }
        }

        function handleFocus(input) {
            const inputId = input.getAttribute('data-id');
            startTimes[inputId] = new Date();
        }

        function handleKeyPress(event, input) {
            if (event.key === 'Enter') {
                event.preventDefault();
                const inputs = document.querySelectorAll('input[type="number"]');
                const currentIndex = Array.from(inputs).indexOf(input);
                if (currentIndex < inputs.length - 1) {
                    inputs[currentIndex + 1].focus();
                } else {
                    // 如果是最后一个输入框，聚焦到完成录入按钮
                    document.getElementById('finish-btn').focus();
                }
            }
        }

        function handleKeyDown(event, input) {
            if (event.key === 'ArrowUp') {
                event.preventDefault();
                const inputs = document.querySelectorAll('input[type="number"]');
                const currentIndex = Array.from(inputs).indexOf(input);
                if (currentIndex > 0) {
                    inputs[currentIndex - 1].focus();
                }
            } else if (event.key === 'ArrowDown') {
                event.preventDefault();
                const inputs = document.querySelectorAll('input[type="number"]');
                const currentIndex = Array.from(inputs).indexOf(input);
                if (currentIndex < inputs.length - 1) {
                    inputs[currentIndex + 1].focus();
                }
            }
        }

        // 页面加载或刷新时自动聚焦到开始录入按钮
        window.onload = function() {
            document.getElementById('start-btn').focus();
        }

        // 开始录入按钮的回车键处理
        document.addEventListener('DOMContentLoaded', function() {
            document.getElementById('start-btn').addEventListener('keypress', function(event) {
                if (event.key === 'Enter') {
                    event.preventDefault();
                    startEntry();
                }
            });
        });
    </script>
</head>
<body>
    <h1>数字录入练习</h1>
    <div class="control-panel">
        <button id="start-btn" onclick="startEntry()">开始录入</button>
        <span id="total-time" class="total-time"></span>
    </div>
    <div class="container">
        <div class="number-list">
            {% for number in numbers[:10] %}
                <div class="number">
                    <span class="number-display">{{ number }}</span>
                    <input type="number" 
                           aria-label="输入数字" 
                           data-id="{{ loop.index }}"
                           onkeypress="handleKeyPress(event, this)"
                           onkeydown="handleKeyDown(event, this)"
                           oninput="handleInput(this)"
                           onfocus="handleFocus(this)"
                           disabled>
                    <span class="timer" id="timer-{{ loop.index }}"></span>
                </div>
            {% endfor %}
        </div>
        <div class="number-list">
            {% for number in numbers[10:] %}
                <div class="number">
                    <span class="number-display">{{ number }}</span>
                    <input type="number" 
                           aria-label="输入数字" 
                           data-id="{{ loop.index + 10 }}"
                           onkeypress="handleKeyPress(event, this)"
                           onkeydown="handleKeyDown(event, this)"
                           oninput="handleInput(this)"
                           onfocus="handleFocus(this)"
                           disabled>
                    <span class="timer" id="timer-{{ loop.index + 10 }}"></span>
                </div>
            {% endfor %}
        </div>
    </div>
    <button id="finish-btn" onclick="finishEntry()" disabled>完成录入</button>
    <button onclick="location.reload()">生成新的数字</button>
</body>
</html>
'''

@app.route('/')
def index():
    # 生成20个随机数字，包含不同位数
    ranges = [
        (10, 99),      # 2位数
        (100, 999),    # 3位数 
        (1000, 9999),  # 4位数
        (10000, 99999), # 5位数
        (100000, 9999999) # 6-7位数
    ]
    numbers = []
    for _ in range(20):
        # 随机选择一个范围生成数字
        min_val, max_val = random.choice(ranges)
        numbers.append(random.randint(min_val, max_val))
    return render_template_string(HTML_TEMPLATE, numbers=numbers)

if __name__ == '__main__':
    app.run(debug=True)
