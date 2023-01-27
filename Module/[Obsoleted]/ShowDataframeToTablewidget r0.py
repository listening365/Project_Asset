#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 
# @Author  : Link
# @Revised by : Ade
# @File    : df_widget.py

from PyQt5 import QtGui
from PyQt5.QtWidgets import QHBoxLayout, QTableWidget, QTableWidgetItem, QScrollBar, QWidget
from PyQt5.QtCore import Qt
import pandas

class test(QWidget):
    print('Module -ShowDataframeToTablewidget- Loaded.')

class dfQTable(QWidget):
    rowCount = 0  # 单页可以显示的数据条数
    #df = DataFrame()

    def showUI(self):
        self.show()
        #Dataframe_TradeHistory = pandas.read_excel('Data\TradeRecord.xlsx')
        #Dataframe_TradeHistory = None      ## 初始Dataframe 會令程式失敗.
        self.df = pandas.read_excel('Data\TradeRecord.xlsx')
        self.pdToQTableWidget()
        self.further_retranslate_Ui()

    def keyPressEvent(self, event):#重新实现了keyPressEvent()事件处理器。
        #按住键盘事件
        #这个事件是PyQt自带的自动运行的，当我修改后，其内容也会自动调用
        if event.key() == Qt.Key_Escape:     #当我们按住键盘是esc按键时
            self.close()#关闭程序

    def further_retranslate_Ui(self):
        self.table.setColumnWidth(0,80)
        self.table.setColumnWidth(1,100)
        self.table.setColumnWidth(3,50)
        self.table.setColumnWidth(4,80)
        self.table.setColumnWidth(6,80)
        self.table.setColumnWidth(7,80)
        self.table.setColumnWidth(8,50)
        self.table.setColumnWidth(9,140)
        self.table.resizeRowsToContents()
        #self.table.resizeColumnsToContents()
        self.table.sortItems(9,Qt.DescendingOrder)                         #设置按照第二列自动升序排序

    def __init__(self, *args):
        super(dfQTable, self).__init__()
        self.ui_setup()
#         self.signal_setup()

    def ui_setup(self):
        self.setGeometry(250, 150, 900, 800)
        # 使用竖直Layout
        self.horizontalLayout = QHBoxLayout(self)
        # 建立一个QTableWidget
        self.table = QTableWidget(self)
        #self.table.verticalHeader().setStretchLastSection(True)

        # 建立一个竖直QScrollBar
#         self.scrollbar = QScrollBar(self)
#         self.scrollbar.setOrientation(Qt.Vertical)
#         self.scrollbar.setSingleStep(1)

        self.horizontalLayout.addWidget(self.table)
#         self.horizontalLayout.addWidget(self.scrollbar)

        self.setWindowFlags(Qt.WindowStaysOnTopHint | Qt.WindowCloseButtonHint)
        self.table.horizontalHeader().setStyleSheet('QHeaderView::section{background:whitesmoke}')     
        self.table.setStyleSheet("QTableCornerButton::section{background:#c2c2c2;}")
        self.table.setStyleSheet("gridline-color:#909090")            # or ("gridline-color:Darkgrey") 

        self.table.horizontalHeader().setSectionsClickable(False)   #可以禁止点击表头的列
        self.table.verticalHeader().hide()

#     def signal_setup(self):
#         self.scrollbar.valueChanged.connect(self.scrollbar_emit)
# 
#     def scrollbar_emit(self, e: int):
#         self.pdToQTableWidget()

#     def calculateRowCountParams(self):
#         if any(self.df):
#             # 先计算
#             rowHeight = self.table.rowHeight(0)
#             rowHeight = 30 if rowHeight == 0 else rowHeight
#             tableHeight = self.table.height()
#             self.rowCount = int(tableHeight / rowHeight) - 1
#             # print("每页行数", self.rowCount, sep=":")
#             # 更新table的行数
#             self.table.setRowCount(self.rowCount)

#             # 滑块的长度
#             scrollbar_count = int(self.df.index.size / self.rowCount)
#             # print("滑块长度", scrollbar_count, sep=":")
#             self.scrollbar.setMaximum(scrollbar_count * 9)

#     def resizeEvent(self, a0: QtGui.QResizeEvent) -> None:
#         self.calculateRowCountParams()
#         self.pdToQTableWidget()
#         if a0:
#             super().resizeEvent(a0)

    def pdToQTableWidget(self):
        """
        更新页面数据
        :return:
        """
        if any(self.df):
            df_columns = self.df.columns.size
            df_header = self.df.columns.values.tolist()
            self.table.setColumnCount(df_columns)
            self.table.setHorizontalHeaderLabels(df_header)

#             start_row = int(self.scrollbar.value() / 9 * self.rowCount)
#             end_row = int((self.scrollbar.value() / 9 + 1) * self.rowCount)

            self.table.setRowCount(self.df.shape[0])    # self.df.shape[0] Gives number of rows      # self.df.shape[1] Gives number of columns
            start_row = int(0)
            end_row = int(self.df.shape[0] + 1)

            print(self.df.shape[0] , self.df.shape[1])
            
            # 数据预览窗口
            for row in range(start_row, end_row):
                for column in range(df_columns):
                    value = ''
                    if row < self.df.index.size:
                        value = '' if pandas.isnull(self.df.iloc[row, column]) else str(self.df.iloc[row, column])
                    tempItem = QTableWidgetItem(value)
                    if column == 4 or column == 6 or column == 7 or column == 9:
                        tempItem.setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)
                    else:
                        tempItem.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
                    self.table.setItem(row , column, tempItem)       ### self.table.setItem((row - start_row), column, tempItem)
