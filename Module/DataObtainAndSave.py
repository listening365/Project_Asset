import pandas
import numpy
import yfinance
import csv


def exchange_rate_obtain_and_save(rate_count_cny_to_hkd=0, rate_count_usd_to_hkd=0):
    # 取得 人幣/港幣 匯率 Started
    if rate_count_cny_to_hkd > 1:
        pass
    else:
        rate_count_cny_to_hkd = 0
    while rate_count_cny_to_hkd == 0:
        try:
            info_cny_to_hkd = yfinance.Ticker("CNYHKD=X")
            print('3-191:', info_cny_to_hkd.info['bid'])
            rate_cny_to_hkd = info_cny_to_hkd.info['bid']
            if rate_cny_to_hkd:
                rate_count_cny_to_hkd = 1
        except Exception as error_message:
            print('Error in Module.DataObtainAndSave:21', error_message)
    # 取得 人幣/港幣 匯率 Ended
    # 取得 美元/港幣 匯率 Started
    if rate_count_cny_to_hkd == 1:
        pass
    else:
        rate_count_usd_to_hkd = 0
    while rate_count_usd_to_hkd == 0:
        try:
            info_usd_to_hkd = yfinance.Ticker("USDHKD=X")
            print('3-20:', info_usd_to_hkd.info['bid'])
            rate_usd_hkd = info_usd_to_hkd.info['bid']
            if rate_usd_hkd:
                rate_count_usd_to_hkd = 1
        except Exception as error_message:
            print('Error in Module.DataObtainAndSave:36', error_message)
    # 取得 美元/港幣 匯率 Ended
    if rate_count_cny_to_hkd == 1 and rate_count_usd_to_hkd == 1:
        data = {
                    '人幣/港幣': rate_cny_to_hkd,
                    '美元/港幣': rate_usd_hkd
                    }
        print(data)
        numpy.save('Data\\CurrencyExchangeRate.npy', data)
        return data


def table_save_to_excel(source, target_table, output_path):
    table = getattr(source, target_table)
    number_of_rows = table.rowCount()
    number_of_columns = table.columnCount()
    column_list = []
    for countHeader in range(number_of_columns):
        it = table.horizontalHeaderItem(countHeader)
        column_list.append(str(countHeader+1) if it is None else it.text())
    tmp_df = pandas.DataFrame( 
                columns=column_list,            # Fill columns
                index=range(number_of_rows)     # Fill rows
                )
    for i in range(number_of_rows):
        for j in range(number_of_columns):
            temp_item = table.item(i, j)
            if temp_item is not None:
                tmp_df.iloc[i, j] = table.item(i, j).text()
            else:
                tmp_df.iloc[i, j] = ''
    tmp_df.to_excel(output_path, index=False)


def table_save_to_csv(source, target_table, output_path):
    table = getattr(source, target_table)
    with open(output_path, 'w', encoding='utf-8-sig') as fileOutput:
        writer = csv.writer(fileOutput, lineterminator='\n')
        for row in range(table.rowCount()):
            row_data = []
            for column in range(table.columnCount()):
                item = table.item(row, column)
                if item is not None:
                    row_data.append(item.text())
                else:
                    row_data.append('')
            writer.writerow(row_data)
