# -*- coding:utf-8 -*-
import sys
import PyQt5.QtCore
from PyQt5.QtCore import Qt
import PyQt5.QtGui
import PyQt5.QtWidgets
import PyQt5.uic
# import P1_1_UI     # Load the .py file - code (1/4)
import P1_3_Controller
import Interface.Dialog_InputTrade
import Module.Format


class Main_Window(PyQt5.QtWidgets.QMainWindow):     # <__main__.Main_Window object at 0x17A8E6C0>
    def __init__(self):
        super(Main_Window, self).__init__()         # Call the inherited classes __init__ method
        PyQt5.uic.loadUi('Interface\\Root_Window.ui', self)    # Load the .ui file
        # self.ui = P1_1_UI.Ui_MainWindow()         # Load the .py file - code (2/4)
        # self.ui.setupUi(self)                     # Load the .py file - code (3/4)
        self.further_retranslate_ui()

# UI edited by code Started
    def further_retranslate_ui(self):
        # self.showMaximized()

        """設定表格格式實例 Started"""
        float0_align_center = \
            Module.Format.SetCellFormatForColumn(0, self.tableWidget, None, 'Qt.AlignCenter | Qt.AlignVCenter', None)         # 0為小數位,數值置中
        float0_align_center_gainsboro = \
            Module.Format.SetCellFormatForColumn(0, self.tableWidget, None, 'Qt.AlignCenter | Qt.AlignVCenter', 'gainsboro')  # 0為小數位,數值置中
        float0_align_right = \
            Module.Format.SetCellFormatForColumn(0, self.tableWidget, None, 'Qt.AlignRight | Qt.AlignVCenter', None)          # 0為小數位
        float0_align_left_gainsboro = \
            Module.Format.SetCellFormatForColumn(0, self.tableWidget, None, None, 'gainsboro')                                # 0為小數位
        float0_align_right_gainsboro = \
            Module.Format.SetCellFormatForColumn(0, self.tableWidget, None, 'Qt.AlignRight | Qt.AlignVCenter', 'gainsboro')   # 0為小數位
        float2_align_right = \
            Module.Format.SetCellFormatForColumn(2, self.tableWidget, None, 'Qt.AlignRight | Qt.AlignVCenter', None)          # 2為小數位
        float2_align_right_gainsboro = \
            Module.Format.SetCellFormatForColumn(2, self.tableWidget, None, 'Qt.AlignRight | Qt.AlignVCenter', 'gainsboro')   # 2為小數位
        float3_align_right = \
            Module.Format.SetCellFormatForColumn(3, self.tableWidget, None, 'Qt.AlignRight | Qt.AlignVCenter', None)          # 3為小數位
        float1_percentage_align_right = \
            Module.Format.SetCellFormatForColumn(1, self.tableWidget, '%', 'Qt.AlignRight | Qt.AlignVCenter', None)           # 1為小數位
        '''設定表格格式實例 Ended'''

        '''設定表格tableWidget Started'''
        self.tableWidget.horizontalHeader().setStyleSheet('QHeaderView::section{background:whitesmoke}')
        self.tableWidget.setStyleSheet("QTableCornerButton::section{background:#c2c2c2;}")
        self.tableWidget.setStyleSheet("gridline-color:#909090")                    # or ("gridline-color:Darkgrey")
        # self.tableWidget.sortItems(1,Qt.AscendingOrder)                           # 设置按照第二欄自动升序排序     AscendingOrder/ DescendingOrder
        self.tableWidget.horizontalHeader().setSectionsClickable(False)             # 可以禁止点击表头的列
        self.tableWidget.setColumnWidth(0, 80)
        self.tableWidget.setColumnWidth(1, 140)
        self.tableWidget.setColumnWidth(2, 180)
        self.tableWidget.setColumnWidth(3, 35)
        self.tableWidget.setColumnWidth(6, 70)
        self.tableWidget.setColumnWidth(7, 35)
        # self.resizeColumnsToContents()
        # self.resizeRowsToContents()
        self.tableWidget.hideColumn(7)
        self.tableWidget.hideColumn(18)
        self.tableWidget.hideColumn(19)
        self.tableWidget.hideColumn(20)
        self.tableWidget.hideColumn(21)
        self.tableWidget.hideColumn(22)
        self.tableWidget.hideColumn(23)
        self.tableWidget.hideColumn(24)
        self.tableWidget.hideColumn(25)
        self.tableWidget.hideColumn(26)
        self.tableWidget.hideColumn(27)
        self.tableWidget.hideColumn(28)
        self.tableWidget.hideColumn(29)
        self.tableWidget.hideColumn(30)
        self.tableWidget.hideColumn(31)
        self.tableWidget.hideColumn(32)
        self.tableWidget.hideColumn(33)
        self.tableWidget.setItemDelegateForColumn(0, float0_align_center)
        self.tableWidget.setItemDelegateForColumn(2, float0_align_left_gainsboro)
        self.tableWidget.setItemDelegateForColumn(4, float0_align_right_gainsboro)
        self.tableWidget.setItemDelegateForColumn(5, float0_align_right_gainsboro)
        self.tableWidget.setItemDelegateForColumn(6, float0_align_center)
        self.tableWidget.setItemDelegateForColumn(8, float0_align_right_gainsboro)
        self.tableWidget.setItemDelegateForColumn(9, float2_align_right_gainsboro)
        self.tableWidget.setItemDelegateForColumn(10, float0_align_right)
        self.tableWidget.setItemDelegateForColumn(11, float0_align_right)
        self.tableWidget.setItemDelegateForColumn(12, float0_align_right_gainsboro)
        self.tableWidget.setItemDelegateForColumn(13, float0_align_right_gainsboro)
        self.tableWidget.setItemDelegateForColumn(14, float0_align_right)
        self.tableWidget.setItemDelegateForColumn(15, float1_percentage_align_right)
        self.tableWidget.setItemDelegateForColumn(16, float0_align_center_gainsboro)
        self.tableWidget.setItemDelegateForColumn(17, float3_align_right)
        self.tableWidget.setHorizontalHeaderLabels([
                                                    '00\n分類', '01\n代號', '02\n名稱', '03\n戶口', '04\n利息/\n盈虧\n(HKD)', '05\n利息/\n盈虧\n(本幣)', '06\n產品',
                                                    '07\n相關\n連結', '08\n股數/\n單位', '09\n買價\n(本幣)', '10\n成本\n(本幣)', '11\n市價\n(本幣)', '12\n成本\n(HKD)',
                                                    '13\n市價\n(HKD)', '14\n浮盈虧\n(HKD)', '15\n浮盈虧\n(%)', '16\n結算\n貨幣', '17\n現值/\n淨值', '18\n股息/\n股息率',
                                                    '19\n升跌', '20\n升跌 \n(%)', '21\n日高', '22\n日低', '23\n趨勢\n(當天)', '24\n市值\n(百萬)', '25\n平均成交量\n(百萬)',
                                                    '26\n成交量\n與市值\n比率', '27\n趨勢\n(一月)', '28\n趨勢\n(一年)', '29\n趨勢\n(三年)', '30\n趨勢\n(十年)',
                                                    '31\n市盈率\n(P/E)', '32\n每股\n盈餘', '33\n名稱\n(英文)'
                                                    ])
        '''設定表格tableWidget Ended'''

        '''設定表格tableTotalCash Started'''
        self.tableTotalCash.horizontalHeader().setStyleSheet('QHeaderView::section{background:whitesmoke}')
        self.tableTotalCash.setStyleSheet("QTableCornerButton::section{background:#c2c2c2;}")
        self.tableTotalCash.setStyleSheet("gridline-color:#909090")            # or ("gridline-color:Darkgrey")
        self.tableTotalCash.setColumnWidth(0, 110)
        self.tableTotalCash.setColumnWidth(1, 60)
        self.tableTotalCash.setColumnWidth(2, 60)
        self.tableTotalCash.setColumnWidth(3, 60)
        self.tableTotalCash.setColumnWidth(4, 70)
        self.tableTotalCash.setColumnWidth(5, 240)
        self.tableTotalCash.hideColumn(5)
        self.tableTotalCash.setItemDelegateForColumn(1, float0_align_right_gainsboro)
        self.tableTotalCash.setItemDelegateForColumn(2, float0_align_right_gainsboro)
        self.tableTotalCash.setItemDelegateForColumn(3, float0_align_right_gainsboro)
        self.tableTotalCash.setItemDelegateForColumn(4, float0_align_right)
        '''設定表格tableTotalCash Ended'''

        '''設定表格tableTotalCash Started'''
        self.tableSummaryCurrentAsset.horizontalHeader().setStyleSheet('QHeaderView::section{background:whitesmoke}')
        self.tableSummaryCurrentAsset.setStyleSheet("QTableCornerButton::section{background:#c2c2c2;}")
        self.tableSummaryCurrentAsset.setStyleSheet("gridline-color:#909090")            # or ("gridline-color:Darkgrey")
        self.tableSummaryCurrentAsset.setColumnWidth(0, 70)
        self.tableSummaryCurrentAsset.setColumnWidth(1, 80)
        self.tableSummaryCurrentAsset.setColumnWidth(2, 80)
        self.tableSummaryCurrentAsset.setColumnWidth(3, 80)
        self.tableSummaryCurrentAsset.setColumnWidth(4, 80)
        self.tableSummaryCurrentAsset.setColumnWidth(5, 50)
        self.tableSummaryCurrentAsset.setColumnWidth(6, 80)
        self.tableSummaryCurrentAsset.setColumnWidth(7, 35)
        self.tableSummaryCurrentAsset.setItemDelegateForColumn(0, float0_align_center)
        self.tableSummaryCurrentAsset.setItemDelegateForColumn(1, float2_align_right_gainsboro)
        self.tableSummaryCurrentAsset.setItemDelegateForColumn(2, float2_align_right)
        self.tableSummaryCurrentAsset.setItemDelegateForColumn(3, float2_align_right)
        self.tableSummaryCurrentAsset.setItemDelegateForColumn(4, float2_align_right_gainsboro)
        self.tableSummaryCurrentAsset.setItemDelegateForColumn(5, float1_percentage_align_right)
        self.tableSummaryCurrentAsset.setItemDelegateForColumn(6, float2_align_right)
        self.tableSummaryCurrentAsset.setItemDelegateForColumn(7, float0_align_center)
        '''設定表格tableTotalCash Ended'''

        '''設定表格tableShortTermAsset Started'''
        self.tableShortTermAsset.horizontalHeader().setStyleSheet('QHeaderView::section{background:whitesmoke}')
        self.tableShortTermAsset.setStyleSheet("QTableCornerButton::section{background:#c2c2c2;}")
        self.tableShortTermAsset.setStyleSheet("gridline-color:#909090")            # or ("gridline-color:Darkgrey")
        self.tableShortTermAsset.setColumnCount(14)
        self.tableShortTermAsset.setColumnWidth(0, 80)   # 00
        self.tableShortTermAsset.setColumnWidth(1, 80)   # 02
        self.tableShortTermAsset.setColumnWidth(2, 60)   # 03
        self.tableShortTermAsset.setColumnWidth(3, 55)   # 04
        self.tableShortTermAsset.setColumnWidth(4, 55)   # 05
        self.tableShortTermAsset.setColumnWidth(5, 80)   # 06
        self.tableShortTermAsset.setColumnWidth(6, 50)   # 08
        self.tableShortTermAsset.setColumnWidth(7, 50)   # 09
        self.tableShortTermAsset.setColumnWidth(8, 80)   # 10
        self.tableShortTermAsset.setColumnWidth(9, 80)   # 11
        self.tableShortTermAsset.setColumnWidth(10, 80)   # 12
        self.tableShortTermAsset.setColumnWidth(11, 80)  # 13
        self.tableShortTermAsset.setColumnWidth(12, 80)  # 14
        self.tableShortTermAsset.setColumnWidth(13, 50)  # 15
        self.tableShortTermAsset.setColumnWidth(14, 25)  # 16
        self.tableShortTermAsset.setItemDelegateForColumn(0, float0_align_center)      # 00
        self.tableShortTermAsset.setItemDelegateForColumn(1, float0_align_center_gainsboro)      # 02
        self.tableShortTermAsset.setItemDelegateForColumn(2, float0_align_center)      # 03
        self.tableShortTermAsset.setItemDelegateForColumn(3, float0_align_right_gainsboro)       # 04
        self.tableShortTermAsset.setItemDelegateForColumn(4, float0_align_right_gainsboro)       # 05
        self.tableShortTermAsset.setItemDelegateForColumn(5, float0_align_center)      # 06
        self.tableShortTermAsset.setItemDelegateForColumn(6, float0_align_right_gainsboro)       # 08
        self.tableShortTermAsset.setItemDelegateForColumn(7, float2_align_right_gainsboro)       # 09
        self.tableShortTermAsset.setItemDelegateForColumn(8, float2_align_right)      # 10
        self.tableShortTermAsset.setItemDelegateForColumn(9, float2_align_right)      # 11
        self.tableShortTermAsset.setItemDelegateForColumn(10, float2_align_right_gainsboro)       # 12
        self.tableShortTermAsset.setItemDelegateForColumn(11, float2_align_right_gainsboro)      # 13
        self.tableShortTermAsset.setItemDelegateForColumn(12, float2_align_right)      # 14
        self.tableShortTermAsset.setItemDelegateForColumn(13, float1_percentage_align_right)      # 15
        self.tableShortTermAsset.setItemDelegateForColumn(14, float0_align_center_gainsboro)     # 16
        '''設定表格tableShortTermAsset Ended'''

        '''設定表格tableLongTermAsset Started'''
        self.tableLongTermAsset.horizontalHeader().setStyleSheet('QHeaderView::section{background:whitesmoke}')
        self.tableLongTermAsset.setStyleSheet("QTableCornerButton::section{background:#c2c2c2;}")
        self.tableLongTermAsset.setStyleSheet("gridline-color:#909090")            # or ("gridline-color:Darkgrey")
        self.tableLongTermAsset.setColumnCount(14)
        self.tableLongTermAsset.setColumnWidth(0, 80)   # 00
        self.tableLongTermAsset.setColumnWidth(1, 80)   # 02
        self.tableLongTermAsset.setColumnWidth(2, 60)   # 03
        self.tableLongTermAsset.setColumnWidth(3, 55)   # 04
        self.tableLongTermAsset.setColumnWidth(4, 55)   # 05
        self.tableLongTermAsset.setColumnWidth(5, 80)   # 06
        self.tableLongTermAsset.setColumnWidth(6, 45)   # 08
        self.tableLongTermAsset.setColumnWidth(7, 50)   # 09
        self.tableLongTermAsset.setColumnWidth(8, 80)   # 10
        self.tableLongTermAsset.setColumnWidth(9, 80)   # 11
        self.tableLongTermAsset.setColumnWidth(10, 80)   # 12
        self.tableLongTermAsset.setColumnWidth(11, 80)  # 13
        self.tableLongTermAsset.setColumnWidth(12, 80)  # 14
        self.tableLongTermAsset.setColumnWidth(13, 50)  # 15
        self.tableLongTermAsset.setColumnWidth(14, 25)  # 16
        self.tableLongTermAsset.setItemDelegateForColumn(0, float0_align_center)      # 00
        self.tableLongTermAsset.setItemDelegateForColumn(1, float0_align_center_gainsboro)      # 02
        self.tableLongTermAsset.setItemDelegateForColumn(2, float0_align_center)      # 03
        self.tableLongTermAsset.setItemDelegateForColumn(3, float0_align_right_gainsboro)       # 04
        self.tableLongTermAsset.setItemDelegateForColumn(4, float0_align_right_gainsboro)       # 05
        self.tableLongTermAsset.setItemDelegateForColumn(5, float0_align_center)      # 06
        self.tableLongTermAsset.setItemDelegateForColumn(6, float0_align_right_gainsboro)       # 08
        self.tableLongTermAsset.setItemDelegateForColumn(7, float2_align_right_gainsboro)       # 09
        self.tableLongTermAsset.setItemDelegateForColumn(8, float2_align_right)      # 10
        self.tableLongTermAsset.setItemDelegateForColumn(9, float2_align_right)      # 11
        self.tableLongTermAsset.setItemDelegateForColumn(10, float2_align_right_gainsboro)       # 12
        self.tableLongTermAsset.setItemDelegateForColumn(11, float2_align_right_gainsboro)      # 13
        self.tableLongTermAsset.setItemDelegateForColumn(12, float2_align_right)      # 14
        self.tableLongTermAsset.setItemDelegateForColumn(13, float1_percentage_align_right)      # 15
        self.tableLongTermAsset.setItemDelegateForColumn(14, float0_align_center_gainsboro)     # 16
        '''設定表格tableLongTermAsset Ended'''
        self.show()     # Show the GUI
# UI edited by code Ended

    def keyPressEvent(self, event):         # 重新实现了keyPressEvent()事件处理器。
        # 按住键盘事件
        # 这个事件是PyQt自带的自动运行的，当我修改后，其内容也会自动调用
        if event.key() == Qt.Key_Escape:    # 当我们按住键盘是esc按键时
            self.tableWidget.clearSelection()
            self.tableWidget.setCurrentCell(-1, -1)
            # self.close()#关闭程序


class DialogInputTrade(PyQt5.QtWidgets.QMainWindow, Interface.Dialog_InputTrade.Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.further_retranslate_ui()

    def further_retranslate_ui(self):
        self.setWindowFlags(Qt.WindowStaysOnTopHint | Qt.WindowCloseButtonHint)
        self.DateB_dateEdit.setDisplayFormat("dd-MM-yyyy")

    def keyPressEvent(self, event):         # 重新实现了keyPressEvent()事件处理器。
        # 按住键盘事件
        # 这个事件是PyQt自带的自动运行的，当我修改后，其内容也会自动调用
        if event.key() == Qt.Key_Escape:    # 当我们按住键盘是esc按键时
            self.close()                    # 关闭程序

    def show_ui(self, ui_main_window, ui_dialog_input_trade):
        P1_3_Controller.Dialog_InputTrade_LoadFromTable(ui_main_window, ui_dialog_input_trade)
        self.show()


if __name__ == "__main__":
    app = PyQt5.QtWidgets.QApplication(sys.argv)        # Create an instance of QtWidgets.QApplication
    UI_Main_Window = Main_Window()                      # Create an instance of our class
    # window = P1_1_UI.Ui_MainWindow()                  # Load the .py file - code (4/4)
    app.exec_()                                         # Start the application
