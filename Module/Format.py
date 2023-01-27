import PyQt5.QtCore
from PyQt5.QtCore    import Qt, QObject, pyqtSignal, pyqtSlot, QCoreApplication    #QThread
import PyQt5.QtGui
from PyQt5.QtGui     import *    # QFont
import PyQt5.QtWidgets
from PyQt5.QtWidgets import *    # QTableWidget,QFrame,QAbstractItemView,QtableWidgetItem, QMessageBox


def apply_color_in_last_row(source, target_table, Row, Column, Red, Green, Blue):
    # 處理applying white color in pervious row 開始
    table = getattr(source, target_table)
    totalrow = table.rowCount() - 1         # -1 due to rowCount start at 1, not   #print(3-83: totalrow)    # for testing
    if Row == 0:
        # print('3-85: Row is 0 is checked at def ')    # for testing
        CompletedRow = totalrow
    elif Row == 1:
        # print('3-92: Row is %d is checked at def ' %(Row))    # for testing
        CompletedRow = 0
    elif Row > 1:
        # print('3-96: Row is %d is checked at def ' %(Row))    # for testing
        CompletedRow = Row - 1
        # print('3-98: CompletedRow is %d is checked at def ' %CompletedRow)    # for testing
    else:
        pass
    # print('3-93: applying white color in pervious row is running#1.')                            # for testing
    count = 0
    if count == 0 and CompletedRow == totalrow:
        pass
    else:
        changeBackgroudColorPerCell(table, CompletedRow, Column, Red, Green, Blue)                  # 處理applying gainsboro color in pervious row 結束
    count += 1


def change_format_per_cell(source, target_table, row, column):
    table = getattr(source, target_table)
    factor = float(table.item(row, column).text())
    cell_text = QTableWidgetItem(str(factor))
    if factor >= 0:
        cell_text.setForeground(QBrush(QColor(0, 128, 0)))    # 後續加入百份比愈大,顏色愈深功能.
    elif factor < 0:
        cell_text.setForeground(QBrush(QColor(255, 0, 0)))    # 後續加入百份比愈大,顏色愈深功能.
    else:
        pass
    table.setItem(row, column, cell_text)


def changeBackgroudColorPerCell(source, Row, Column, Red, Green, Blue):
    #print('3-114: changeBackgroupColorPerCell worked')   ### for testing
    Celltext = source.item(Row,Column)
    Celltext.setBackground(PyQt5.QtGui.QColor(Red, Green, Blue))


def changeBackgroudColorPerColumn(source, Column, Red, Green, Blue):
    # print('3-145')
    totalrow = source.rowCount()
    # print('3-147: The total row is ',totalrow)
    for Row in range(totalrow):
        changeBackgroudColorPerCell(source, Row, Column, Red, Green, Blue)


class SetCellFormatForColumn(PyQt5.QtWidgets.QStyledItemDelegate):
    def __init__(self, decimal, parent=None, expression=None, alignment=None, bgColor=None):  #
        super().__init__(parent)
        self.Decimal = decimal
        self.Expression = expression  #
        if alignment == 'Qt.AlignRight | Qt.AlignVCenter':
            self.Alignment = Qt.AlignRight | Qt.AlignVCenter
        elif alignment == 'Qt.AlignCenter | Qt.AlignVCenter':
            self.Alignment = Qt.AlignCenter | Qt.AlignVCenter
        else:
            self.Alignment = Qt.AlignLeft | Qt.AlignVCenter
        self.BGcolor = bgColor

    def initStyleOption(self, option, index):
        super().initStyleOption(option, index)
        # print(self.Alignment)
        try:
            text = index.model().data(index, PyQt5.QtCore.Qt.DisplayRole)
            number = float(text)
            if self.Expression == '%':
                option.text = "{:.{}%}".format(number, self.Decimal)  # 設置百份比及小數位.
            else:
                option.text = "{:,.{}f}".format(number, self.Decimal)  # 設置小數位.
        except:
            pass
        option.displayAlignment = self.Alignment  # 設置文字擺放方式.
        if self.BGcolor != None:
            option.backgroundBrush = PyQt5.QtGui.QBrush(PyQt5.QtGui.QColor(self.BGcolor))  # 設置底色.