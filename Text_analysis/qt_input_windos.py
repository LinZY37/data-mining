import sys
from PyQt5 import QtWidgets, QtGui
import sqlite3
import time

from loadModel import predict_str_lable

# 创建或连接数据库
conn = sqlite3.connect('predictions.db')
c = conn.cursor()

# 创建表
c.execute('''
    CREATE TABLE IF NOT EXISTS predictions(
        time TEXT,
        text_input TEXT,
        prediction TEXT
    )
''')


class SentimentAnalysisApp(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('新闻分析')
        self.setGeometry(100, 100, 1000, 800)  # 修改窗口尺寸为1000x800
        layout = QtWidgets.QVBoxLayout()

        # 创建文本输入框并设置样式
        self.text_input = QtWidgets.QTextEdit("请输入文本")
        self.text_input.setStyleSheet('font-size: 16px;')  # 增大字体大小
        layout.addWidget(self.text_input)

        # 创建预测按钮并设置样式
        self.predict_button = QtWidgets.QPushButton("预测")
        self.predict_button.setStyleSheet('font-size: 16px; padding: 10px;')  # 增大字体和按钮内边距
        self.predict_button.clicked.connect(self.predict)
        layout.addWidget(self.predict_button)

        # 创建显示结果的标签并设置样式
        self.result_label = QtWidgets.QLabel("")
        self.result_label.setStyleSheet('font-size: 16px;')  # 增大字体大小
        layout.addWidget(self.result_label)

        # 创建显示以往记录的表格并设置样式
        self.records_table = QtWidgets.QTableWidget()
        self.records_table.setStyleSheet('font-size: 14px;')  # 增大字体大小
        layout.addWidget(self.records_table)

        self.setLayout(layout)
        self.show()

        # 加载以往的记录到表格中
        self.load_records()
    def predict(self):
        text = self.text_input.toPlainText()
        if text:
            labels, _ = predict_str_lable([text])
            prediction = ', '.join(labels)
            self.result_label.setText(f"预测的标签为：{prediction}")
            current_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
            c.execute("INSERT INTO predictions VALUES (?, ?, ?)", (current_time, text, prediction))
            conn.commit()
            self.load_records()
        else:
            self.result_label.setText("请输入需要分析的文本。")

    def load_records(self):
        records = c.execute("SELECT * FROM predictions ORDER BY time DESC").fetchall()
        self.records_table.setColumnCount(3)
        self.records_table.setRowCount(len(records))
        self.records_table.setHorizontalHeaderLabels(['Time', 'Text', 'Prediction'])

        # 设置列伸展策略
        header = self.records_table.horizontalHeader()
        header.setSectionResizeMode(QtWidgets.QHeaderView.Stretch)

        # 设置第一列和第三列的伸展因子，使其宽度相等
        header.setStretchLastSection(False)  # 确保最后一列不会自动伸展填充
        header.setSectionResizeMode(0, QtWidgets.QHeaderView.ResizeToContents)
        header.setSectionResizeMode(2, QtWidgets.QHeaderView.ResizeToContents)

        # 计算中间列的伸展因子，使其占总宽度的一半
        # 假设第一列和第三列的伸展因子之和为1，则中间列的伸展因子应该为1
        header.setSectionResizeMode(1, QtWidgets.QHeaderView.Stretch)

        for index, (time, text, prediction) in enumerate(records):
            self.records_table.setItem(index, 0, QtWidgets.QTableWidgetItem(time))
            self.records_table.setItem(index, 1, QtWidgets.QTableWidgetItem(text))
            self.records_table.setItem(index, 2, QtWidgets.QTableWidgetItem(prediction))


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    ex = SentimentAnalysisApp()
    sys.exit(app.exec_())