# 数字录入练习系统

一个用于练习和提高数字录入速度的 Web 应用程序。通过实时反馈和计时功能，帮助用户提升数字录入的准确性和速度。

## 功能特点

- 随机生成数字序列供练习
- 实时计时功能
  - 显示每个数字的录入用时
  - 统计总体录入时间
- 即时错误检查
  - 输入错误时视觉提示
  - 完成后显示错误统计
- 响应式设计，适配各种屏幕尺寸
- 简洁直观的用户界面

## 使用说明

1. 点击"开始"按钮开始练习
2. 依次输入显示的数字
3. 每个数字框右侧会显示该数字的录入用时
4. 输入完成后点击"完成"按钮
5. 系统会自动检查输入是否正确并显示总用时
6. 错误的输入会以红色标注

## 技术栈

- HTML5
- CSS3
- JavaScript (原生)

## 本地部署

1. 克隆仓库到本地
2. 安装 Python 3.7+
3. 安装依赖包:
   ```
   pip install virtualenv
   virtualenv .venv
   ./.venv/Scripts/Activate.PS1 (windows)
   source .venv/bin/activate (mac/linux)
   pip install -r requirements.txt
   ```
4. 运行应用:
   ```
   python digital-entry/digital-entry.py
   ```
5. 在浏览器中访问 http://localhost:5000
