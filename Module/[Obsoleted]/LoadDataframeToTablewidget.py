#-*- coding:utf-8 -*-
# author: Ade Tsa;
from PyQt5 import QtGui
from PyQt5.QtWidgets import QHBoxLayout, QTableWidget, QTableWidgetItem, QScrollBar, QWidget
from PyQt5.QtCore import Qt
import pandas
from pandas import isnull


def DataLoad_Initial(source_table):
    # 載入初始數據 Started
    pass
#     load_dict = numpy.load('..\Data\CurrencyExchangeRate.npy', allow_pickle=True).item()
#     self.exchange_Rate_CHYHKD = load_dict['人幣/港幣']
#     P1_3_Controller.handleLoad(self)        ####重要:必須執行此行 讀取表格後 方能處理表格
#     Module.LoadDataframeToTablewidget.pdToQTableWidget(source='Data\TotalCash.xlsx', table=self.tableTotalCash)
#     P1_3_Controller.tableTotalCash_changed(item=None, source=self.tableTotalCash, outputPath='Data\TotalCash.xlsx')
#     P1_3_Controller.applyDataInColumn(self, 17, str('等待取價'))      ###l初始 17.現價 為0 以避免錯誤
    # 載入初始數據 Ended
    
def  aaa():
    pass



def pdToQTableWidget( **kwargs):
    df = pandas.read_excel(kwargs['source'])
    ### 將df載入QTABLEWIDGET Started
    if any(df):
        df_columns = df.columns.size
        df_header = df.columns.values.tolist()
        df_row = df.shape[0]
        kwargs['table'].setColumnCount(df_columns)
        kwargs['table'].setRowCount(df_row)
        kwargs['table'].setHorizontalHeaderLabels(df_header)

        #print('the total row is',df_row)
#         start_row = int(self.scrollbar.value() / 9 * self.rowCount)
#         end_row = int((self.scrollbar.value() / 9 + 1) * self.rowCount)
        # 数据预览窗口
        for row in range(df_row):						#start_row, end_row
            for column in range(df_columns):
                value = ''
                #if row < df.index.size:
                value = '' if isnull(df.iloc[row, column]) else str(df.iloc[row, column])
                tempItem = QTableWidgetItem(value)
                kwargs['table'].setItem(row, column, tempItem)
                #kwargs['table'].item(row, column).setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
    ### 將DF載入QTABLEWIDGET Ended

