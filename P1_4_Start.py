# -*- coding:utf-8 -*-
# author: Ade Tsa; Python ber3.7.9 (32bit); PyQt5 ver.5.15.6
import sys
# import numpy
# import PyQt5.QtCore
from PyQt5.QtCore import QThread    # Qt, pyqtSignal
import PyQt5.QtWidgets
import pandas
import P1_2_EditUI
import P1_3_Controller
import Module.Calculation
import Module.DataLoadAndRefresh
import Module.DataObtainAndSave
import Module.PopupFromDataframeShowTable


def run_main_window(self):
    # 載入初始數據 Started
    Module.DataLoadAndRefresh.load_data_initial(self)
    # 載入初始數據 Ended

    # QThread 多線程功能引入代碼 Started
    self.thread = QThread()
    self.ThreadObject = P1_3_Controller.ThreadClass(self)
    self.ThreadObject.moveToThread(self.thread)
    self.thread.started.connect(self.ThreadObject.thread_run)
    self.thread.finished.connect(lambda: P1_3_Controller.thread_finished(self))
    # QThread 多線程功能引入代碼 Ended

    # UI_connection(UI_Main_Window)    #介面功能/訊號 連接 Started
    self.actionSave.triggered.connect(lambda: Module.DataObtainAndSave.table_save_to_excel(self, 'tableWidget', 'Data\\ShortTermAssetDetail.xlsx'))
    self.actionTest.triggered.connect(lambda: P1_3_Controller.handle_test(self))
    self.pushButton_Start.clicked.connect(lambda: P1_3_Controller.thread_start(self))
    self.pushButton_Stop.clicked.connect(lambda: P1_3_Controller.thread_stop(self))
    self.pushButton_InputTrade.clicked.connect(lambda: UI_Dialog_InputTrade.show_ui(UI_Main_Window, UI_Dialog_InputTrade))
    self.pushButton_ShowTradeHistory.clicked.connect(lambda: UI_Window_TradeHistory.showUI(
        source='Data\\TradeRecord.xlsx', sort=10,
        geometry=[200, 150, 1050, 800],
        textAlignRight=[4, 6, 7, 8],
        columnWidth={'0': 60, '1': 140, '2': 180, '3': 35, '4': 70, '5': 80, '6': 80, '7': 70, '8': 90, '9': 35, '10': 140}
        ))
    self.tableWidget.doubleClicked.connect(lambda: UI_Dialog_InputTrade.show_ui(UI_Main_Window, UI_Dialog_InputTrade))
    self.tableWidget.cellClicked.connect(P1_3_Controller.cell_click)     # lambda:P1_3_Controller.handle_test(self))
    self.tableTotalCash.itemChanged.connect(lambda item: Module.Calculation.handle_formula_in_cell(item, self, 'tableTotalCash'))
    self.tableSummaryCurrentAsset.itemChanged.connect(lambda item: Module.Calculation.handle_formula_in_cell(item, self, 'tableSummaryCurrentAsset'))
    self.tableLongTermAsset.itemChanged.connect(lambda item: Module.Calculation.handle_formula_in_cell(item, self, 'tableLongTermAsset'))
    # UI_connection(UI_Main_Window)    #介面功能/訊號 連接 Ended


def run_dialog_input_trade(self):
    self.pushButton_decide.clicked.connect(lambda: P1_3_Controller.dialog_input_trade_for_decide(UI_Main_Window, UI_Dialog_InputTrade))
    self.pushButton_assume.clicked.connect(lambda: P1_3_Controller.dialog_input_trade_for_assume(UI_Main_Window, UI_Dialog_InputTrade))


if __name__ == "__main__":
    pandas.set_option('display.max_rows', 500)      # 最大行数
    pandas.set_option('display.max_columns', 500)   # 最大列数
    pandas.set_option('display.width', 4000)        # 页面宽度
    app = PyQt5.QtWidgets.QApplication(sys.argv)   # Create an instance of PyQt5.QtWidgets.QApplication
    # 載入全局變數 >>>直到下個註釋
    # 將 對象 實例化 並作初始設定>>>直到下個註釋
    UI_Main_Window = P1_2_EditUI.Main_Window()
    UI_Dialog_InputTrade = P1_2_EditUI.DialogInputTrade()
    UI_Window_TradeHistory = Module.PopupFromDataframeShowTable.dfQTable()
    # UI_Window_PopupDataframe = Module.PopupFromDataframeShowTable.dfQTable()

    # 以函數 運行 實例 >>>直到下個註釋
    run_main_window(UI_Main_Window)
    run_dialog_input_trade(UI_Dialog_InputTrade)
    #

    # print('the getattr is :', getattr(UI_Main_Window, 'tableTotalCash'))

    sys.exit(app.exec_())   # Start the application
