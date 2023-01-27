# -*- coding:utf-8 -*-
# author: Ade Tsa; Python ber3.7.9 (32bit); PyQt5 ver.5.15.6
# import PyQt5.QtWidgets
from PyQt5.QtWidgets import *
import numpy
import Module.DataLoadAndRefresh


def handle_formula_in_cell(item, source, target_table):     # tableTotalCash
    table = getattr(source, target_table)
    table.blockSignals(True)
    if item.text() != '':
        temp1 = eval(item.text())
    else:
        temp1 = ''
    print(temp1)
    temp2 = QTableWidgetItem(str(temp1))
    table.setItem(table.currentRow(), table.currentColumn(), temp2)
    Module.DataLoadAndRefresh.determine_table_for_next_function(source, target_table)
    table.blockSignals(False)


def calculation_cells_in_column(source, row_start, row_end, column, arithmetic, adjustment, output, output_row=None, output_column=None):
    dict_exchange_rate = numpy.load('Data\\CurrencyExchangeRate.npy', allow_pickle=True).item()
    total_cells = row_end - row_start + 1
    # print('total_cells is ', total_cells)
    factor1, factor2 = 0, 0
    temp_a1 = str(source.item(row_start, column).text())
    if temp_a1 != '':
        factor1 = float(str(temp_a1))
    else:
        factor1 = 0
    # print('factor1 is', factor1)
    # print('factor1 and factor2 are', factor1, factor2)
    for i in range(1, total_cells):
        temp_a2 = source.item(row_start + i, column).text()
        if temp_a2 != '':
            current_cell = float(str(temp_a2))
        else:
            current_cell = 0
        # print('current_cell is ', current_cell)
        match arithmetic:
            case '+':
                factor1 += current_cell     # if isinstance(current_cell, float | int | str) else 0
            case '-':
                factor1 -= current_cell     # if isinstance(current_cell, float | int | str) else 0
            case '*':
                factor1 *= current_cell     # if isinstance(current_cell, float | int | str) else 0
            case '/':
                factor1 /= current_cell     # if isinstance(current_cell, float | int | str) else 0
            case _:
                print('arithmetic: Not Match.')
    #     print('factor1 is', factor1)
    # print('total factor1 is', factor1)
    match adjustment:
        case 'CNYtoHKD':
            factor2 = dict_exchange_rate['人幣/港幣']
        case 'USDtoHKD':
            factor2 = dict_exchange_rate['美元/港幣']
        case 'None':
            factor2 = 1
        case _:
            print('adjustment: Not Match.')
    match output:
        case (x, output_table) if x == 'table':
            # print('table', output_table)
            Celltext = QTableWidgetItem(str(factor1 * factor2))
            output_table.setItem(output_row, output_column, Celltext)
        case (x, label) if x == 'label':
            # print('label', label)
            label.setText(format(float(factor1 * factor2), '0,.0f'))        # label.setText("%.0f" % float(factor1 * factor2))
        case (x, y) if x == 'other':
            print('good', y)
        case _:
            print('output: Not Match.')


def calculation_cells_in_row(source, row, column_start, column_end, arithmetic, adjustment, output, output_row=None, output_column=None):
    # 必須似calculation_cells_in_column重寫.
    dict_exchange_rate = numpy.load('CurrencyExchangeRate.npy', allow_pickle=True).item()
    total_cells = column_end - column_start + 1
    # print('total_cells is ', total_cells)
    factor1, factor2 = 0, 0
    temp_a1 = source.item(row, column_start).text()
    factor1 = float(str(temp_a1)) if isinstance(temp_a1, float | int) else 0
    # print('factor1 is', factor1)
    # print('factor1 and factor2 are', factor1, factor2)
    for i in range(1,total_cells):
        temp_a2 = source.item(row, column_start + i).text()
        current_cell = float(str(temp_a2)) if isinstance(temp_a2, float | int) else 0
        # print('current_cell is ', current_cell)
        match arithmetic:
            case '+':
                factor1 += current_cell if isinstance(current_cell, float | int) else 0
            case '-':
                factor1 -= current_cell if isinstance(current_cell, float | int) else 0
            case '*':
                factor1 *= current_cell if isinstance(current_cell, float | int) else 0
            case '/':
                factor1 /= current_cell if isinstance(current_cell, float | int) else 0
            case _:
                print('arithmetic: Not Match.')
        # print('factor1 is', factor1)
    # print('total factor1 is', factor1)
    match adjustment:
        case 'CNYtoHKD':
            factor2 = dict_exchange_rate['人幣/港幣']
        case 'USDtoHKD':
            factor2 = dict_exchange_rate['美元/港幣']
        case 'None':
            factor2 = 1
        case _:
            print('adjustment: Not Match.')
    match output:
        case (x, output_table) if x == 'table':
            print('table', output_table)
            Celltext = QTableWidgetItem(str(factor1 * factor2))
            output_table.setItem(output_row, output_column, Celltext)
        case (x, label) if x == 'label':
            print('label', label)
            label.setText(format(float(factor1 * factor2), '0,.0f'))        # label.setText("%.0f" % float(factor1 * factor2))
        case (x, y) if x == 'other':
            print('good', y)
        case _:
            print('output: Not Match.')



def calculation_all_cells_per_row(source, target_table, Row, Column1, Column2, Outputcolumn, Adjustment):
    # print('3-121:', exchange_Rate.info['bid'])
    table = getattr(source, target_table)
    dict_exchange_Rate = numpy.load('Data\\CurrencyExchangeRate.npy', allow_pickle=True).item()
    factor1 = float(str(table.item(Row, Column1).text()))
    factor2 = float(str(table.item(Row, Column2).text()))
    currency = str(table.item(Row, 16).text())
    if Adjustment == "+":
        result = factor1 + factor2
    elif Adjustment == "-":
        result = factor1 - factor2
    elif Adjustment == "*":
        result = factor1 * factor2
    elif Adjustment == "*currency":
        if currency == 'CNY':
            result = factor1 * factor2 * dict_exchange_Rate['人幣/港幣']
            # print('Calculation.py 144 ok')
        if currency == 'HKD':
            result = factor1 * factor2
        if currency == 'USD':
            result = factor1 * factor2 * dict_exchange_Rate['美元/港幣']
    elif Adjustment == "only*currency":
        factor2 = 1
        if currency == 'CNY':
            result = factor1 * factor2 * dict_exchange_Rate['人幣/港幣']
        if currency == 'HKD':
            result = factor1
        if currency == 'USD':
            result = factor1 * factor2 * dict_exchange_Rate['美元/港幣']
    elif Adjustment == "/":
        result = factor1 / factor2
    else:
        result = None
    cell_text = QTableWidgetItem(str(result))
    table.setItem(Row, Outputcolumn, cell_text)
#         settingBackgroudAsBlue = QTableWidgetItem()
#         settingBackgroudAsBlue.setBackgroundas(QBrush(QColor(0, 0, 250)))
#         table.setItemForColumn(0, settingBackgroudAsBlue)



def calculationPerColumn(source, Column1, Column2, Outputcolumn, Adjustment):
    #print('3-141:', exchange_Rate.info['bid'])
    dict_exchange_Rate = numpy.load('Data\\CurrencyExchangeRate.npy', allow_pickle=True).item()
    # print(dict_exchange_Rate['人幣/港幣'])
    # print(dict_exchange_Rate['美元/港幣'])

    totalrow = source.rowCount()
    # print(totalrow)
    for i in range(totalrow):
        factor1 = float(str(source.item(i,Column1).text())) if source.item(i,Column1).text() != '' else 0
        factor2 = float(str(source.item(i,Column2).text())) if source.item(i,Column2).text() != '' else 0
        if Adjustment == "factor1+Factor2":
            result = factor1 + factor2

        elif Adjustment == "factor1-Factor2":
            result = factor1 - factor2

        elif Adjustment == "factor1*Factor2":
            result = factor1 * factor2
        elif Adjustment == "factor1*Factor2*CNYtoHKD":
            result = factor1 * factor2 * dict_exchange_Rate['人幣/港幣']
        elif Adjustment == "factor1*Factor2*USDtoHKD":
            result = factor1 * factor2 * dict_exchange_Rate['美元/港幣']
        elif Adjustment == "factor1*CNYtoHKD":
            result = factor1 * dict_exchange_Rate['人幣/港幣']
        elif Adjustment == "factor1*USDtoHKD":
            result = factor1 * dict_exchange_Rate['美元/港幣']

        elif Adjustment == "factor1/Factor2":
            result = factor1 / factor2

        elif Adjustment == "Factor1_copied":
            result = factor1

        elif Adjustment == "Factor1To3*exchangeRate":
            factor3 = float(str(source.item(i,Column2 + 1).text())) if source.item(i,Column2 + 1).text() != '' else 0
            result = factor1 + factor2 * dict_exchange_Rate['人幣/港幣']  + factor3 * dict_exchange_Rate['美元/港幣']

        else:
            result = None
        cell_text = QTableWidgetItem(str(result))
        source.setItem(i,Outputcolumn, cell_text)

''' 以下代碼有關變動時作變色提示, 待多線桯時使用
#         settingBackgroudAsBlue = QTableWidgetItem()
#         settingBackgroudAsBlue.setBackgroundas(QBrush(QColor(0, 0, 250)))
#         self.tableWidget.setItemForColumn(0, settingBackgroudAsBlue)
'''


