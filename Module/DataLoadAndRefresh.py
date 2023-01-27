# -*- coding:utf-8 -*-
# author: Ade Tsa;
import numpy
# from PyQt5 import QtGui
from PyQt5.QtWidgets import QTableWidgetItem    # QHBoxLayout, QTableWidget, QScrollBar, QWidget
# from PyQt5.QtCore import Qt
import pandas
from pandas import isnull
import Module
import copy
# import P1_2_EditUI
'''這模組用於存放 運作邏輯'''


def load_data_initial(source):
    # 載入初始數據 Started
    load_dict = numpy.load('Data\\CurrencyExchangeRate.npy', allow_pickle=True).item()
    source.exchange_Rate_CHYHKD = load_dict['人幣/港幣']
    # load_data_for_table_of_investment(source)      # 重要:必須執行此行 讀取表格後 方能處理表格
    load_excel_via_df_to_table('Data\\ShortTermAssetDetail.xlsx', source, 'tableWidget')
    load_excel_via_df_to_table('Data\\TotalCash.xlsx', source, 'tableTotalCash')
    load_excel_via_df_to_table('Data\\ShortTermAsset.xlsx', source, 'tableShortTermAsset')
    load_excel_via_df_to_table('Data\\LongTermAsset.xlsx', source, 'tableLongTermAsset')
    load_excel_via_df_to_table('Data\\SummaryCurrentAsset.xlsx', source, 'tableSummaryCurrentAsset')
    # apply_data_in_column(source, 'tableWidget', 17, str('等待取價'))     # l初始 17.現價 為'等待取價' 以避免錯誤
    count_table_from_total_cast_to_summary_current_asset(source, 'tableTotalCash')
    # 載入初始數據 Ended


def apply_data_in_column(source, target_table, output_column, result):   # 此函數移植自P1_3_Controller
    table = getattr(source, target_table)
    total_row = table.rowCount()
    for i in range(total_row):
        cell_text = QTableWidgetItem(result)
        table.setItem(i, output_column, cell_text)


def determine_table_for_next_function(source, target_table):
    match target_table:
        case 'tableWidget':
            print('tableWidget is called')
        case 'tableTotalCash':
            # print('tableTotalCash is called')
            handle_data_when_table_total_cash_changed(source, target_table)
        case 'tableSummaryCurrentAsset':
            # print('tableSummaryCurrentAsset is called')
            handle_data_when_table_summary_current_asset_changed(source, target_table)
        case 'tableLongTermAsset':
            # print('tableLongTermAsset is called')
            handle_data_when_table_long_term_asset_changed(source, target_table)
        case _:
            print('no table is matched')


def handle_data_when_table_widget_changed(source, target_table, row):
    """將tableWidget留有部份空欄計算並進行後續處理."""
    # table = getattr(source, target_table)
    Module.Calculation.calculation_all_cells_per_row(source, target_table, row, 5, 5, 4, "only*currency")        	# 5.利息/盈虧(本幣)  x 匯價 = 4.利息/盈虧(HKD)
    Module.Calculation.calculation_all_cells_per_row(source, target_table, row, 10, 8, 9, "/")        				# 10.成本(本幣)  /  8.股數/單位 = 9.買價(本幣)
    Module.Calculation.calculation_all_cells_per_row(source, target_table, row, 8, 17, 11, "*")    			# 8.股數/單位 * 17.現值/淨值  = 11.市價(本幣)
    Module.Calculation.calculation_all_cells_per_row(source, target_table, row, 8, 9, 12, "*currency")        		# 8.股數/單位 x 9.買價(本幣) x 匯價 = 12.成本(HKD)
    Module.Calculation.calculation_all_cells_per_row(source, target_table, row, 8, 17, 13, "*currency")    	# 8.股數/單位 * 17.現值/淨值  = 13.市價(HKD)
    Module.Calculation.calculation_all_cells_per_row(source, target_table, row, 13, 12, 14, "-")    			# 13.市價(HKD) - 12.成本結算(HKD) = 14.浮盈虧(HKD)
    Module.Calculation.calculation_all_cells_per_row(source, target_table, row, 14, 12, 15, "/")   			# 14.浮盈虧(HKD) / 12.成本結算(HKD) = 15.浮盈虧(%)
    print('65')
    Module.Format.change_format_per_cell(source, target_table, row, 14)
    Module.Format.change_format_per_cell(source, target_table, row, 15)
    print('68')
    Module.DataObtainAndSave.table_save_to_excel(source, target_table, 'Data\\ShortTermAssetDetail.xlsx')  # todo
    print('70')
    load_data_for_table_of_short_term_asset(source)     # 將ShortTermAssetDetail.xlsx資料轉換為ShortTermAsset.xlsx, 井引用載入函數供tableShortTermAsset使用
    print('72')
    # todo


def handle_data_when_table_total_cash_changed(source, target_table):   # tableTotalCash
    table = getattr(source, target_table)
    Module.Calculation.calculationPerColumn(table, 1, 2, 4, 'Factor1To3*exchangeRate')
    count_table_from_total_cast_to_summary_current_asset(source, 'tableTotalCash')
    Module.DataObtainAndSave.table_save_to_excel(source, target_table, 'Data\\TotalCash.xlsx')


def handle_data_when_table_summary_current_asset_changed(source, target_table):
    # table = getattr(source, target_table)
    Module.DataObtainAndSave.table_save_to_excel(source, target_table, 'Data\\SummaryCurrentAsset.xlsx')


def handle_data_when_table_long_term_asset_changed(source, target_table):
    # table = getattr(source, target_table)
    Module.DataObtainAndSave.table_save_to_excel(source, target_table, 'Data\\LongTermAsset.xlsx')


def count_table_from_total_cast_to_summary_current_asset(source, target_table):
    table = getattr(source, target_table)
    Module.Calculation.calculation_cells_in_column(table, 0, 1, 1, '+', 'None', ('table', source.tableSummaryCurrentAsset), 0, 6)
    Module.Calculation.calculation_cells_in_column(table, 2, 2, 1, '+', 'None', ('table', source.tableSummaryCurrentAsset), 1, 6)
    Module.Calculation.calculation_cells_in_column(table, 3, 4, 2, '+', 'None', ('table', source.tableSummaryCurrentAsset), 3, 6)
    Module.Calculation.calculation_cells_in_column(table, 5, 9, 1, '+', 'None', ('table', source.tableSummaryCurrentAsset), 2, 6)


def load_data_for_table_of_investment(self):
    df_trade_record = pandas.read_excel('Data\\TradeRecord.xlsx')
    df_holding_record = copy.deepcopy(df_trade_record)
    df_holding_record = df_holding_record.groupby(['00\n分類', '01\n代號', '02\n名稱', '03\n戶口', '06\n產品', '16\n貨幣']).sum().reset_index()
    df_holding_record = df_holding_record.reindex(sorted(df_holding_record.columns), axis=1)  # 以header排序
    df_holding_record = df_holding_record.sort_values(by='01\n代號', ascending=True)  # 以欄值排序
    df_holding_record['09\n買價(本幣)'] = df_holding_record['10\n成本(本幣)'] / df_holding_record['08\n股數/單位']  # 將總額變回每單位單價均價
    # print('96', df_holding_record)
    if df_holding_record['08\n股數/單位'].eq(0).any():
        print('A trade is settled and the holding unit becomes zero.')
        df_settled_record = pandas.DataFrame(columns=df_trade_record.columns)
        # print('100', df_settled_record)
        target_index = df_holding_record.loc[df_holding_record['08\n股數/單位'] == 0, :].index.item()
        # print('target_index is', target_index)
        target_code = df_holding_record.at[target_index, '01\n代號']
        # print(target_code)
        df_holding_record.drop(df_holding_record[df_holding_record['08\n股數/單位'] == 0].index, inplace=True)
        cond = df_trade_record['01\n代號'] == target_code
        rows = df_trade_record.loc[cond, :]
        df_settled_record = df_settled_record.append(rows, ignore_index=True)
        df_settled_record.to_excel('Data\\SettledRecord.xlsx', index=False)
        df_trade_record.drop(rows.index, inplace=True)
        df_trade_record.to_excel('Data\\TradeRecord.xlsx', index=False)
        # print(df_trade_record)
        # print(df_settled_record)
    df_holding_record.to_excel('Data\\HoldingRecord.xlsx', index=False)
    df = df_holding_record
    # 將df載入table_widget Started
    if any(df):
        df_columns = df.columns.size
        # df_header = df.columns.values.tolist()
        # self.tableWidget.setColumnCount(df_columns)
        # self.tableWidget.setHorizontalHeaderLabels(df_header)
        self.tableWidget.setRowCount(df.shape[0])  # self.df.shape[0] Gives number of rows      # self.df.shape[1] Gives number of columns
        start_row = int(0)
        end_row = int(df.shape[0] + 1)
        # 数据预览窗口
        for row in range(start_row, end_row):
            for column in range(df_columns):
                value = ''
                if row < df.index.size:
                    value = '' if pandas.isnull(df.iloc[row, column]) else str(df.iloc[row, column])
                temp_item = QTableWidgetItem(value)
                if column == 0:
                    self.tableWidget.setItem(row, 0, temp_item)
                if column == 1:
                    self.tableWidget.setItem(row, 1, temp_item)
                if column == 2:
                    self.tableWidget.setItem(row, 2, temp_item)
                if column == 3:
                    self.tableWidget.setItem(row, 3, temp_item)
                if column == 4:  # 05利息(本幣)
                    self.tableWidget.setItem(row, 5, temp_item)
                if column == 5:
                    self.tableWidget.setItem(row, 6, temp_item)
                if column == 6:
                    self.tableWidget.setItem(row, 8, temp_item)
                if column == 7:
                    self.tableWidget.setItem(row, 9, temp_item)
                if column == 8:
                    self.tableWidget.setItem(row, 10, temp_item)
                if column == 9:
                    self.tableWidget.setItem(row, 16, temp_item)
    # 將DF載入table_widget Ended


def load_data_for_table_of_short_term_asset(source):
    """將ShortTermAssetDetail.xlsx資料轉換為ShortTermAsset.xlsx, 井引用載入函數供tableShortTermAsset使用"""
    df_record = pandas.read_excel('Data\\ShortTermAssetDetail.xlsx')
    df_record = df_record.drop(df_record.columns[[1, 7, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33]], axis=1)
    df_record['02\n名稱'] = ''
    df_record['03\n戶口'] = ''
    df_record['08\n股數/\n單位'] = ''
    df_record['09\n買價\n(本幣)'] = ''
    df_record['15\n浮盈虧\n(%)'] = ''
    df_record = df_record.groupby(['00\n分類', '02\n名稱', '03\n戶口', '06\n產品', '08\n股數/\n單位', '09\n買價\n(本幣)', '15\n浮盈虧\n(%)', '16\n結算\n貨幣']).sum().reset_index()
    df_record = df_record.reindex(sorted(df_record.columns), axis=1)  # 以header排序
    df_record = df_record.sort_values(by='06\n產品', ascending=True)  # 以欄值排序
    df_record['15\n浮盈虧\n(%)'] = df_record['14\n浮盈虧\n(HKD)'] / df_record['12\n成本\n(HKD)']
    # load_df_to_table(df_record, source, 'tableShortTermAsset')
    df_record.to_excel('Data\\ShortTermAsset.xlsx', index=False)
    load_excel_via_df_to_table('Data\\ShortTermAsset.xlsx', source, 'tableShortTermAsset')



def load_exchange_rate_in_thread(source):
    dict_exchange_rate = numpy.load('Data\\CurrencyExchangeRate.npy', allow_pickle=True).item()
    exchange_rate_cny_to_hkd = dict_exchange_rate['人幣/港幣']
    exchange_rate_usd_to_hkd = dict_exchange_rate['美元/港幣']
    source.ExchangeRateLabel_CHYHKD.setText("人幣/港幣: %.4f" % exchange_rate_cny_to_hkd)
    source.ExchangeRateLabel_USDHKD.setText("美元/港幣: %.4f" % exchange_rate_usd_to_hkd)


def load_excel_via_df_to_table(excel, source, target_table):  # 將pandas dataframe載入QTABLEWIDGET
    df = pandas.read_excel(excel)
    load_df_to_table(df, source, target_table)


def load_df_to_table(df, source, target_table):
    table = getattr(source, target_table)
    if any(df):
        df_columns = df.columns.size
        df_header = df.columns.values.tolist()
        df_row = df.shape[0]
        table.setColumnCount(df_columns)
        table.setRowCount(df_row)
        table.setHorizontalHeaderLabels(df_header)
        # 数据预览窗口
        for row in range(df_row):						# start_row, end_row
            for column in range(df_columns):
                value = '' if isnull(df.iloc[row, column]) else str(df.iloc[row, column])
                temp_item = QTableWidgetItem(value)
                table.setItem(row, column, temp_item)
                # table.item(row, column).setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
