import json
import os
import sys

import mkwikidata
from rdflib import Graph
import pandas as pd

from PyQt6.QtWidgets import QApplication, QMainWindow, QLabel, QTextEdit, QWidget, QPushButton, \
    QHBoxLayout, QVBoxLayout, QFileDialog, QComboBox


def formate_data(result_table):
    """
     将查询的数据格式化，去掉不需要的的type列，只保留value列
    :param result_table: type is pandas.core.frame.DataFrame
    :return: pandas.core.frame.DataFrame
    """
    columns = list(result_table.columns)  # 获取列标题
    print("shape: ", type(result_table), result_table.shape)

    # print("head: \n", result_table.head())  # Viewing the first 5 lines
    new_columns = list()
    for item in columns:
        if item.endswith('.value'):
            new_columns.append(item)

    simple_table = result_table[new_columns]
    simple_table = simple_table.rename(columns=lambda col: col.replace(".value", ""))
    print("simple_table:\n ", simple_table)
    return simple_table


def get_query_dict():
    file_path = "test_data/query_data.json"
    f = open(file_path, 'r')
    choose_dict = json.load(f)  # is dict
    return choose_dict


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("my SPARQL")

        self.show_path_label = QLabel("file path")
        self.choose_button = QPushButton("选择rdf文件")
        layout1 = QHBoxLayout()
        layout1.addWidget(self.show_path_label)
        layout1.addWidget(self.choose_button)

        self.choose_query = QComboBox()
        # self.query_input = QTextEdit("请输入SPARQL查询语句")
        self.query_button = QPushButton("查询")
        layout2 = QHBoxLayout()
        layout2.addWidget(self.choose_query)
        layout2.addWidget(self.query_button)

        self.query_input = QTextEdit("请输入SPARQL查询语句")
        self.show_text = QTextEdit()
        layout3 = QVBoxLayout()
        layout3.addLayout(layout1)
        layout3.addLayout(layout2)
        layout3.addWidget(self.query_input)
        layout3.addWidget(self.show_text)

        container = QWidget()
        container.setLayout(layout3)

        # Set the central widget of the Window.
        self.setCentralWidget(container)
        self.setGeometry(300, 200, 600, 600)
        self.init_widget()

    def init_widget(self):
        choose_dict = get_query_dict()
        for k, v in choose_dict.items():
            self.choose_query.addItem(k, v)
        self.choose_button.clicked.connect(self.choose_file)
        self.choose_query.currentIndexChanged.connect(self.set_query_input_choose)
        self.query_button.clicked.connect(self.query_data)

    def choose_file(self):
        result = QFileDialog.getOpenFileName(self, caption='xml文件', directory='./', filter='*.rdf')
        file_path = result[0]
        print("result file type: ", result)
        if file_path and os.path.exists(file_path):
            self.show_path_label.setText(file_path)

        print("file_path: ", type(file_path), file_path)

    def set_query_input_choose(self, index):
        # print("value: ",  index)
        # self.choose_query.
        res = self.choose_query.itemData(index)
        self.query_input.setText(res)

    def query_data(self):
        """
        Query the rdf file with the given query string and return the results as a pandas Dataframe.
        """
        file_path = self.show_path_label.text().strip()
        query = self.query_input.toPlainText()
        print("file_path: ", file_path)
        if file_path != "file path":
            # print("file_path: ", file_path)
            g = Graph().parse(file_path)
            result = g.query(query).serialize(encoding='utf-8', format='json').decode('utf-8')
            query_result = json.loads(result)  # json to dict
            # result_table = pd.json_normalize(result["results"]["bindings"])
        else:
            query_result = mkwikidata.run_query(query, params={})
        # print("query: ", type(query), query)
        # print("query_result: ", query_result)
        if query_result and query_result["results"]["bindings"]:
            result_table = pd.json_normalize(query_result["results"]["bindings"])
            columns = list(result_table.columns)  # 获取列标题

            new_columns = list()
            for item in columns:
                if item.endswith('.value'):
                    new_columns.append(item)

            simple_table = result_table[new_columns]
            simple_table = simple_table.rename(columns=lambda col: col.replace(".value", ""))
            html_table = simple_table.to_html()
            self.show_text.setText(html_table)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
