# -*- coding:utf-8 -*-
# import os
import sys
# import csv
import time
import pandas
# import numpy
from lxml import html
import requests
import re
import yfinance
import efinance
# import datetime
import PyQt5.QtCore
from PyQt5.QtCore import QObject, pyqtSignal     # QThread  Qt, pyqtSlot, QCoreApplication
import PyQt5.QtGui
# from PyQt5.QtGui     import *    # QFont
import PyQt5.QtWidgets
from PyQt5.QtWidgets import *    # QTableWidget,QFrame,QAbstractItemView,QtableWidgetItem, QMessageBox
import P1_2_EditUI
import Module.DataObtainAndSave
import Module.DataLoadAndRefresh
import Module.Calculation
import Module.Format


# 訊號觸發功能 Started
def handle_test(self):
    print('3-19: 菜單功能 to [handle_test worked]', self)
    self.StateLabel.setText('測試功能已執行')


def cell_click(row, col):
    print("Click on " + str(row) + " " + str(col))
# 訊號觸發功能 Ended

# 獨立功能 Started


def Dialog_InputTrade_LoadFromTable(from_table, to_table=None):
    Row = from_table.tableWidget.currentRow()
    print('3-101:', Row)
    if Row == -1:   		# 判定無選取時
        # print('3-102: Row is unselected', Row)
        to_table.setWindowTitle('新交易')
        to_table.pushButton_assume.setEnabled(False)
        to_table.ClassificationB_lineEdit.setText('')
        to_table.CodeB_lineEdit.setText('')
        to_table.NameB_lineEdit.setText('')
        to_table.AccountB_comboBox.setCurrentIndex(0)
        to_table.InterestB_lineEdit.setText('')
        to_table.ProductB_comboBox.setCurrentIndex(0)
        to_table.UnitB_lineEdit.setText('')             # 8.股數/單位
        to_table.PriceB_lineEdit.setText('')            # 9.總價
        to_table.UnitB_lineEdit_assume.setText('')      # 股數/單位
        to_table.PriceB_lineEdit_assume.setText('')     # 單價
        to_table.CurrencyB_comboBox.setCurrentIndex(0)
        to_table.DateB_dateEdit.setDate(PyQt5.QtCore.QDate.currentDate())
    else:				# 判定有選取時
        to_table.setWindowTitle(from_table.tableWidget.item(Row, 2).text())
        to_table.pushButton_assume.setEnabled(True)
        classification = from_table.tableWidget.item(Row, 0).text()
        account = from_table.tableWidget.item(Row, 3).text()
        product = from_table.tableWidget.item(Row, 6).text()
        currency = from_table.tableWidget.item(Row, 16).text()
        price = from_table.tableWidget.item(Row, 17).text()
        to_table.ClassificationB_lineEdit.setText(from_table.tableWidget.item(Row, 0).text())
        to_table.CodeB_lineEdit.setText(from_table.tableWidget.item(Row, 1).text())
        to_table.NameB_lineEdit.setText(from_table.tableWidget.item(Row, 2).text())
        if account == 'FSM':
            to_table.AccountB_comboBox.setCurrentIndex(0)
        elif account == '富途':
            to_table.AccountB_comboBox.setCurrentIndex(1)
        elif account == '中行':
            to_table.AccountB_comboBox.setCurrentIndex(2)
        elif account == '一通':
            to_table.AccountB_comboBox.setCurrentIndex(3)
        elif account == 'SoFi':
            to_table.AccountB_comboBox.setCurrentIndex(4)
        # UiTo.InterestB_lineEdit.setText(UiFrom.tableWidget.item(Row, 5).text())   # 有待加入計算累計利息功能
        to_table.InterestB_lineEdit.setText('')                                         # 清空欄
        if product == 'A:貨幣基金':             # 'A: 現金/貨基/短債基金'
            to_table.ProductB_comboBox.setCurrentIndex(0)
        elif product == 'B:穩建理財':           # 'B: 穩建理財':
            to_table.ProductB_comboBox.setCurrentIndex(1)
        elif product == 'C:進取基金':           # 'C: 進取基金':
            to_table.ProductB_comboBox.setCurrentIndex(2)
        elif product == 'D:股票/證券':          # 'D: 股票/證券產品':
            to_table.ProductB_comboBox.setCurrentIndex(3)
        elif product == 'E:強積金':            # 'E: 強積金/股票':
            to_table.ProductB_comboBox.setCurrentIndex(4)
        elif product == 'F:貴金屬':            # 'F: 貴金屬':
            to_table.ProductB_comboBox.setCurrentIndex(5)
        # UiTo.UnitB_lineEdit.setText(UiFrom.tableWidget.item(Row, 8).text())   # 讀取8.股數/單位, 暫時廢棄
        to_table.UnitB_lineEdit.setText('')                                         # 清空欄
        # UiTo.PriceB_lineEdit.setText(UiFrom.tableWidget.item(Row, 9).text())  # 讀取9.買價(本幣), 暫時廢棄
        to_table.PriceB_lineEdit.setText('')                                        # 清空欄
        if currency == 'HKD':
            to_table.CurrencyB_comboBox.setCurrentIndex(0)
        elif currency == 'CNY':
            to_table.CurrencyB_comboBox.setCurrentIndex(1)
        elif currency == 'USD':
            to_table.CurrencyB_comboBox.setCurrentIndex(2)
        to_table.DateB_dateEdit.setDateTime(PyQt5.QtCore.QDateTime.currentDateTime())
        to_table.UnitB_lineEdit_assume.setText('')
        if price == '':											# 未必有用,待查.
            to_table.PriceB_lineEdit_assume.setText('')			    # 未必有用,待查.
        else:
            to_table.PriceB_lineEdit_assume.setText(price)
        to_table.assume_output_unit_label.setText('')
        to_table.assume_output_unitprice_label.setText('')


def dialog_input_trade_for_decide(from_source, to_source):      # QMessageBox.about(to_source, '錯誤', '必須輸入欄 "股數/單位" 及 "買價(本幣)"')
    row = from_source.tableWidget.currentRow()
    # print('3-166: row is ', row)
    input_classification = to_source.ClassificationB_lineEdit.text()
    input_code = to_source.CodeB_lineEdit.text()
    input_name = str(to_source.NameB_lineEdit.text())
    input_account = to_source.AccountB_comboBox.currentText()
    if to_source.InterestB_lineEdit.text() == "":
        input_interest = float(0)
    else:
        input_interest = float(to_source.InterestB_lineEdit.text())
    input_product = to_source.ProductB_comboBox.currentText()
    input_unit = float(to_source.UnitB_lineEdit.text()) if to_source.UnitB_lineEdit.text() != '' else 0         # 8.股數/單位
    input_price = float(to_source.PriceB_lineEdit.text()) if to_source.PriceB_lineEdit.text() != '' else 0      # 10.成本 / (總價)
    try:
        input_rate = input_price / input_unit                   # 9.買價
    except ZeroDivisionError:
        input_rate = 0
    input_currency = to_source.CurrencyB_comboBox.currentText()
    input_datetime = to_source.DateB_dateEdit.dateTime().currentDateTime().toString("yyyy-MM-dd HH:mm:ss")      # self.dateEdit.date().toString(Qt.ISODate)  # 选择日期     /toPyDateTime()
    df1 = pandas.read_excel('Data\\TradeRecord.xlsx')
    new_dict = {
            "00\n分類": input_classification,               # lambda: UiTo.ClassificationB_lineEdit.text(),
            "01\n代號": input_code,                         # lambda: UiTo.CodeB_lineEdit.text(),
            "02\n名稱": input_name,                         # lambda: UiTo.NameB_lineEdit.text(),
            "03\n戶口": input_account,                      # lambda: UiTo.AccountB_comboBox.text(),
            "05\n利息(本幣)": input_interest,                 # lambda: UiTo.InterestB_lineEdit.text(),
            "06\n產品": input_product,                      # lambda: UiTo.ProductB_comboBox.text(),
            "08\n股數/單位": input_unit,                      # lambda: float(UiTo.UnitB_lineEdit.text()),
            "09\n買價(本幣)": input_rate,     # lambda: float(UiTo.PriceB_lineEdit.text()),
            "10\n成本(本幣)": input_price,                    # lambda: float(UiTo.PriceB_lineEdit.text()),
            "16\n貨幣": input_currency,                     # lambda: UiTo.CurrencyB_comboBox.text(),
            "交易日期": input_datetime
            }
    df2 = pandas.DataFrame(new_dict, index=[0])
    df = pandas.concat([df1, df2], axis=0)
    df.to_excel('Data\\TradeRecord.xlsx', index=False)
    Module.DataLoadAndRefresh.load_data_for_table_of_investment(from_source)    # 將TradeRecord.xlsx讀入至tableWidget, 留有部份空欄.
    Module.DataLoadAndRefresh.handle_data_when_table_widget_changed(from_source, 'tableWidget', row)   # 將tableWidget留有部份空欄計算並進行後續處理.
    to_source.close()


def dialog_input_trade_for_assume(from_source, to_source):
    row = from_source.tableWidget.currentRow()
    # print('3-166: row is ', row)
    if from_source.tableWidget.item(row, 8).text() == '' or to_source.UnitB_lineEdit_assume.text() == '' or from_source.tableWidget.item(row, 9).text() == '' or to_source.PriceB_lineEdit_assume.text() == '':
        QMessageBox.about(to_source, '錯誤', '必須輸入欄 "股數/單位" 及 "買價(本幣)"')
    else:
        exist_unit = float(from_source.tableWidget.item(row, 8).text())
        assume_unit = float(to_source.UnitB_lineEdit_assume.text())    # 8.股數/單位
        exist_price = float(from_source.tableWidget.item(row, 9).text())
        assume_price = float(to_source.PriceB_lineEdit_assume.text())    # 9.買價(本幣)
        to_source.assume_output_unit_label.setText(str('%.2f' % (exist_unit + assume_unit)))
        to_source.assume_output_unitprice_label.setText(str('%.2f' % (((exist_unit * exist_price) + (assume_unit * assume_price)) / (exist_unit + assume_unit))))


# Class 功能類 started
class ThreadClass(QObject):     # 多線程類(QThread)
    # count = str('Thread Working')
    # count_signal = pyqtSignal(str)
    signal_thread_data_into_cell = pyqtSignal(object, int, int, object)
    signal_thread_update_data = pyqtSignal(object)

    def __init__(self, location):
        super(ThreadClass, self).__init__()
        self.run = True
        self.location = location
        self.signal_thread_data_into_cell.connect(applyDataInCellThenRowFromThreadSignal)
        self.signal_thread_update_data.connect(Module.DataLoadAndRefresh.load_exchange_rate_in_thread)
        # print('3-201: testing.ThreadClass.__init__', self.location)   ### For Testing

    def thread_run(self):        # 此函數內不能有修改PyQt5界面代碼.   e.g.self.location.tableWidget.setItem
        Module.DataObtainAndSave.exchange_rate_obtain_and_save()
        self.signal_thread_update_data.emit(self.location)
        self.run = True
        while self.run:
            thread_run_for_price(self)
            time.sleep(10)    # 定期更新時間

    def thread_stop(self):
        self.run = False
# Class 功能類 Ended


def thread_start(self):
    # print('3-23: Button to [button start]', self)
    self.StateLabel.setText("線程進行中")
    self.pushButton_Start.setEnabled(False)
    self.thread.start()


def thread_stop(self):
    # print('3-29: Button to [button stop]', self)
    self.StateLabel.setText("線程停止中")
    self.pushButton_Stop.setEnabled(False)
    self.ThreadObject.thread_stop()
    self.thread.quit()


def thread_finished(self):
    # print('3-35: Thread Finish.', self)
    self.StateLabel.setText('線程完結')
    self.pushButton_Start.setEnabled(True)
    self.pushButton_Stop.setEnabled(True)
    

def thread_run_for_price(self):
    total_row = self.location.tableWidget.rowCount()         # 由0算起
    for i in range(total_row):
        classification = self.location.tableWidget.item(i, 0).text()
        code = self.location.tableWidget.item(i, 1).text()
        price = self.location.tableWidget.item(i, 17).text()
        matches = ('B03_0P0000VG5A.HK', 'B04_0P0001I84C.HK', 'B08_0P0001KM2G.HK', 'D00_')
        if code in matches:
            try:
                match code:
                    case 'B03_0P0000VG5A.HK':                                                               # 貝萊德中國債券MDis(港元/每月派息)(LU0690034276.FD)
                        urlMatch = 'https://www.futunn.com/hk/stock/881088-HK'                              # self.location.tableWidget.item(i,28).text()
                        xpthMatch = '/html/body/div[3]/div/div[3]/section[1]/div[2]/div[2]/div[1]/span[1]'  # self.location.tableWidget.item(i,29).text()
                    case 'B04_0P0001I84C.HK':                                                               #
                        urlMatch = 'https://www.futunn.com/stock/882000-HK?seo_redirect=1'                  # self.location.tableWidget.item(i,28).text()
                        xpthMatch = '/html/body/div[3]/div/div[3]/section[1]/div[2]/div[2]/div[1]/span[1]'  # self.location.tableWidget.item(i,29).text()
                    case 'B08_0P0001KM2G.HK':                                                                            # 積利金
                        urlMatch = 'https://www.futunn.com/hk/stock/884030-HK'                              # 'https://online.kitco.com.hk/gold/index.html'
                        xpthMatch = "/html/body/div[3]/div/div[3]/section[1]/div[2]/div[2]/div[1]/span[1]"  # '/html/body/div[2]/div[3]/div/div[3]/div[4]/div[1]/span[3]'
                    case 'D00_':                                                                            # 積利金
                        urlMatch = 'http://www.dyhjw.com/gold/kjzb.html'                                    # 'https://online.kitco.com.hk/gold/index.html'
                        xpthMatch = "/html/body/div[10]/div[3]/div[1]/table/tbody/tr[4]/td[2]"              # '/html/body/div[2]/div[3]/div/div[3]/div[4]/div[1]/span[3]'
                    # case _:
                    #     pass
                    #     print('Not match.')
                headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) ''Chrome/51.0.2704.63 Safari/537.36'}
                url = urlMatch
                page = requests.get(url, headers=headers, timeout=30)
                tree = html.fromstring(page.text)
                feature_bullets = tree.xpath(xpthMatch + '/text()')
                if str(feature_bullets) == '[]':
                    Celltext = QTableWidgetItem(str(0))
                else:
                    Celltext = QTableWidgetItem(re.sub("人民幣 |\[|\'|\]|\,|,", "", str(feature_bullets)))    # 刪除無用字符
                print('P1_3 264: Matches ok')
            except:
                print('P1_3 266: Matches error')
# 利用yfinance取得股價 Started
        elif code[:1] == 'A':    # elif classification == '香港股票' or classification == '中國股票':
            try:
                ticker = yfinance.Ticker(code[4:])				# 移除字串 A00_
                feature_bullets = ticker.info['currentPrice']
                Celltext = QTableWidgetItem(str(feature_bullets))
            except:
                print('P1_3 274 error')
        elif code[:1] == 'B':                   # elif classification == '香港基金':
            try:
                float(price)
                Celltext = QTableWidgetItem(str(price))
            except:
                try:
                    ticker = yfinance.Ticker(code[4:])
                    feature_bullets = ticker.info['regularMarketPrice']
                    Celltext = QTableWidgetItem(str(feature_bullets))
                except:
                    print('P1_3 285 error')
# 利用efinance取得現價 Started
        elif code[:1] == 'C':      # elif classification == '中國基金':
            try:
                float(price)
                Celltext = QTableWidgetItem(str(price))
            except:
                try:
                    series = efinance.fund.get_base_info(code[4:])
                    feature_bullets = series['最新净值']
                    Celltext = QTableWidgetItem(str(feature_bullets))
                except:
                    pass
# 利用efinance取得現價 Ended
# 利用Xpath取得現價 Started
        else:
            print('P1_3: 277, not match at all')

# 利用Xpath取得現價 Ended
        Celltext.setBackground(PyQt5.QtGui.QColor(255, 255, 0))                                     # 將變動格變成黃色
        # self.location.tableWidget.setItem(i,16, Celltext)                                       # 此函數內不能有修改PyQt5界面代碼.
        self.signal_thread_data_into_cell.emit(self.location, i, 17, Celltext)
        time.sleep(1)
        # print('3-223: 處理行 %d, 總共有 %d 行' %(i + 1, total_row))                         ### for testing, # 由1算起
        '''將處理後的格變回白色 Started'''
        if i == total_row - 1:               # 如果正在計算最後的行數.
            if str(feature_bullets) == '[]':
                Celltext = QTableWidgetItem(str(1))
            else:
                feature_bullets = self.location.tableWidget.item(i, 17).text()
                Celltext = QTableWidgetItem(re.sub("人民幣 |\[|\'|\]", "", str(feature_bullets)))    # 前面的訊號發出後,必須重新建立對象
            Celltext.setBackground(PyQt5.QtGui.QColor(220, 220, 220))
            self.signal_thread_data_into_cell.emit(self.location, i, 17, Celltext)
        else:
            pass
        '''將處理後的格變回白色 Ended'''


def applyDataInCellThenRowFromThreadSignal(source, Row, Column, Celltext):
    # table = self.tableWidget   # 設定採用表格
    target_table = 'tableWidget'
    table = getattr(source, target_table)
    table.setItem(Row, Column, Celltext)
    Module.DataLoadAndRefresh.handle_data_when_table_widget_changed(source, target_table, Row)
    Module.Format.apply_color_in_last_row(source, target_table, Row, Column, 220, 220, 220)     # 220,220,220灰色


if __name__ == "__main__":
    app = PyQt5.QtWidgets.QApplication(sys.argv)    # Create an instance of PyQt5.QtWidgets.QApplication
    UI_Main_Window = P1_2_EditUI.Main_Window()      # Create an instance of our class
    sys.exit(app.exec_())                           # Start the application
