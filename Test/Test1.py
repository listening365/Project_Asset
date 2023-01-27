"""
作者：鲁班工作室
qq:1514149460
wx:18550030945
"""
# coding:utf-8

from PyQt5.Qt import QThread, QThreadPool, QRunnable, QObject, QWidget, QApplication, QPushButton, QGridLayout, QTextEdit, pyqtSignal, QTextCursor
import sys


# 这里执行核心代码
class Thread(QRunnable):
    communication = None

    def __init__(self):
        super(Thread, self).__init__()
        self.thread_logo = None

    def run(self):
        self.communication.log_signal.emit('{}线程已经执行'.format(self.thread_logo))

    # 自定义函数，用来初始化一些变量
    def transfer(self, thread_logo, communication):
        """
        :param thread_logo:线程标识，方便识别。
        :param communication:信号
        :return:
        """

        self.thread_logo = thread_logo
        self.communication = communication


# 定义任务，在这里主要创建线程
class Tasks(QObject):
    communication = None
    max_thread_number = 0

    def __init__(self, communication, max_thread_number):
        """
        :param communication:通讯
        :param max_thread_number:最大线程数
        """
        super(Tasks, self).__init__()

        self.max_thread_number = max_thread_number
        self.communication = communication

        self.pool = QThreadPool()
        self.pool.globalInstance()

    def start(self):
        # 设置最大线程数

        self.pool.setMaxThreadCount(self.max_thread_number)
        for i in range(10):
            task_thread = Thread()
            task_thread.transfer(thread_logo=i, communication=self.communication)
            task_thread.setAutoDelete(True)  # 是否自动删除
            self.pool.start(task_thread)

        self.pool.waitForDone()  # 等待任务执行完毕
        self.communication.log_signal.emit('线程全部执行完毕')


# 重写QThread类
class NowThread(QThread):
    def __init__(self, communication, max_thread_number):
        """
        :param communication:通讯
        :param max_thread_number:最大线程数
        """
        super(NowThread, self).__init__()
        self.task = Tasks(
            communication=communication,
            max_thread_number=max_thread_number
        )

    def run(self):
        self.task.start()


class Window(QWidget):
    # 定义信号
    log_signal = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self.resize(1280, 800)
        self.setWindowTitle('QThreadPool实例')
        self.setup_ui()
        self.show()

    def setup_ui(self):
        # 初始化信号关联槽函数
        self.log_signal.connect(self.log_signal_event)

        layout = QGridLayout(self)  # 创建布局

        button = QPushButton('测试按钮', self)
        button.clicked.connect(self.button_event)
        text_edit = QTextEdit()
        text_edit.setObjectName('text_edit')

        layout.addWidget(button, 0, 0)
        layout.addWidget(text_edit, 0, 1)
        self.setLayout(layout)

    def button_event(self):
        thread = NowThread(
            communication=self,
            max_thread_number=5
        )
        thread.start()  # 开始线程
        thread.wait()  # 等待线程

    def log_signal_event(self, p_str):
        text_edit = self.findChild(QTextEdit, 'text_edit')
        text_cursor = QTextCursor(text_edit.textCursor())
        text_cursor.setPosition(0, QTextCursor.MoveAnchor)  # 移动光标
        text_cursor.insertHtml('<p style="font-size:20px;color:red;">{}</p>'.format(p_str))
        text_cursor.insertHtml('<br>')
        text_edit.setTextCursor(text_cursor)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = Window()
    sys.exit(app.exec())



"""

import tkinter as tk          # 导入 Tkinter 库
import time
import asyncio
import threading
 
 
 
class Form:
    def __init__(self):
        self.root=tk.Tk()
        self.root.geometry('500x300')
        self.root.title('窗体程序')  #设置窗口标题
        
        self.button=tk.Button(self.root,text="开始计算",command=self.change_form_state)
        self.label=tk.Label(master=self.root,text="等待计算结果")
 
        self.button.pack()
        self.label.pack()
 
        self.root.mainloop()
 
    async def calculate(self):
        await asyncio.sleep(3)
        self.label["text"]=300
 
    def get_loop(self,loop):
        self.loop=loop
        asyncio.set_event_loop(self.loop)
        self.loop.run_forever()
    def change_form_state(self):
        coroutine1 = self.calculate()
        new_loop = asyncio.new_event_loop()                        #在当前线程下创建时间循环，（未启用），在start_loop里面启动它
        t = threading.Thread(target=self.get_loop,args=(new_loop,))   #通过当前线程开启新的线程去启动事件循环
        t.start()
 
        asyncio.run_coroutine_threadsafe(coroutine1,new_loop)  #这几个是关键，代表在新线程中事件循环不断“游走”执行
 
 
if __name__=='__main__':
    form=Form()


########

import asyncio


async def test(i):
    print('test_1', i)
    await asyncio.sleep(2)
    print('test_2', i)

if __name__ == '__main__':
    
    loop =  asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    tasks = [test(i) for i in range(10)]
    loop.run_until_complete(asyncio.wait(tasks))
    loop.close()
    
####

#     loop = asyncio.get_event_loop()
# to
#     loop =  asyncio.new_event_loop()
#     asyncio.set_event_loop(loop)

# num = 1.1
# print(isinstance(num,float | int))
# if isinstance(num,float | int):
#     print('yes')
# else:
#     print('No')
# 
# match num:
#     case isinstance(num, int):
#         print('num is int')
#     case isinstance(num, int):
#         print('num is not int')
            
# color = 1.11
# 
# print(type(color))
# 
# if type(color) == int:
#     print('yes')
# 
# match color:
#     case color if type(color) == int:
#         print("I see red!")
#     case color if type(color) == float:
#         print("Grass is green")
#     case color if type(color) == str:
#         print("I'm feeling the blues :(")

color111 = ('good', 16)

print(type(color111))

match color111:
    case (x, y) if x == 'text':
        print('text', y)
    case (x, y) if x == 'label':
        print('label', y)
    case (x, y) if x == 'good':
        print('good', y)


# class ReservedCodes():     #保留CODE留在 大綱 以便檢索
#     pass
#     def pandasRelated():
#         pass
#         df["按行求和"] =df.apply(lambda x:x.sum(),axis =1)    #https://www.codeleading.com/article/44845482647/
#         df.loc["按列求和"] =df.apply(lambda x:x.sum())           #https://www.codeleading.com/article/44845482647/
#
#     def Other():
#         pass
#         # # class Getting_Web_Data():    #如需重新作類,須增加行的縮排並修改P1_4_start的相關部份
#         # def GetPriceViaXpathAndApplyToColumn(self):    #此函數暫未被引用.
#         #     totalrow = self.tableWidget.rowCount()
#         #     print(totalrow)    ### For Testing
#         #     for i in range(totalrow):
#         #         try:
#         #             url = self.tableWidget.item(i,28).text()
#         # #                 print(url)    ### for testing
#         #             page = requests.get(url)
#         #             tree = html.fromstring(page.text)
#         #             feature_bullets = tree.xpath(self.tableWidget.item(i,29).text()+'/text()')
#         # #                 print(self.tableWidget.item(i,29).text()+'/text()')    ### for testing
#         # #                 print(feature_bullets)                                 ### for testing
#         #             Celltext = QTableWidgetItem(re.sub("\[|\'|\]","",str(feature_bullets)))
#         #             self.tableWidget.setItem(i,16, Celltext)
#         # #             self.SetItemInMainThread.emit(i,feature_bullets)
#         #         except:
#         #             pass
#
#         # def flush(self, count):
#         #     self.StateLabel.setText(str(count))
#         #     # self.label.setText(str(count))
#         #
#         # class AppendItemInMainthread():
#         #     def trans(self,i,feature_bullet):
#         #         print(i)
#         #         print(feature_bullet)
#         # #         Celltext = QTableWidgetItem(re.sub("\[|\'|\]","",str(feature_bullets)))
#         # #         window.tableWidget.setItem(i,16, Celltext)
#         #
#         # class WorkingCalcuation():
#         #     def __init__(self):
#         #         super().__init__()
#         #         print("hello")
#         #
#         # class Main_Thread():
#         #     def __init__(self):
#         #         super().__init__()
#         #         print('Main_Thread ran')
#         # #
#         # class Basic_Function():
#         #     pass
#         #
#         # class OutputTest():
#         #    def __init__(self):
#         #        super().__init__()
#         #        print('OutputTest done!')
#
#         # class AlignCenter(PyQt5.QtWidgets.QStyledItemDelegate):
#         #     def initStyleOption(self, option, index):
#         #         super(AlignCenter, self).initStyleOption(option, index)
#         #         option.displayAlignment = Qt.AlignCenter | Qt.AlignVCenter
#
#         # writer = pandas.ExcelWriter('Trade Record\{}.xlsx'.format(Inputed_Code), engine = 'openpyxl', mode= 'a')
#

#######

# value = '1.4555555555'
# tempItem = QTableWidgetItem(value)
# print(tempItem)
# print(tempItem.data(0))
# print(tempItem.data(1))
# 
# number = 2.5555
# 
# print(number) 
# 
# print(str("{:,.{}f}".format(number, 2)))
# 
# tempItem = QTableWidgetItem(str("{:,.{}f}".format(float(tempItem.data(0)), 2)))
# 
# print(tempItem)
# print(tempItem.data(0))
# print(tempItem.data(1))
# 
# # tempItem.data = "{:,.{}f}".format(value, 2)
# #option.text = "{:,.{}f}".format(number, self.Decimal)  


# from PyQt5.QtWidgets import QApplication, QDialog, QGridLayout, QLabel, QLineEdit, QTableView
# from PyQt5.QtCore import QAbstractTableModel, Qt
# 
# class Example(QDialog):
#     def __init__(self, *args, **kwargs):
#         super(Example, self).__init__(*args, **kwargs)            
#         self.initUI()
# 
#     def initUI(self):
#         grid = QGridLayout(self)
#         a1 = QLabel('alphanumeric characters')
#         a2 = QLabel('alphanumeric characters')
# 
#         grid.addWidget(QLabel('Name'), 0, 0)
#         grid.addWidget(QLineEdit(), 0, 1)
#         grid.addWidget(QLabel('Street1'), 1, 0)
#         grid.addWidget(QLineEdit(), 1, 1)
#         grid.addWidget(QLabel('Street2'), 2, 0)
#         grid.addWidget(QLineEdit(), 2, 1)
#         grid.addWidget(QLabel('City'), 3, 0)
#         grid.addWidget(QLineEdit(), 3, 1)
# 
#         grid.addWidget(QLabel('only alphanumeric'), 0, 2, 4, 1)
# 
#         self.setGeometry(500, 500, 500, 500)
#         self.setWindowTitle('Lines')
#         self.show()
# if __name__ =="__main__":
#     app = QApplication(sys.argv) # Create an instance of PyQt5.QtWidgets.QApplication
#     ex = Example()
#     ex.show()
#     sys.exit(app.exec_()) # Start the application
    
#######

# def a(b,**x):
#     print(x)
#     print(x['z'])
#     print(x['z'][0])
#     print(b)
#     print(x['dict1']['1'])
#     for i in x['dict1']:
#         print(x['dict1'][i],)
# 
# a(b=1,r=1,y=2,z=[1,2,3], dict1={'1': 100, '2': 200})

##########

# df = pandas.read_excel('Data\TradeRecord.xlsx')
# Module.ShowDataframeToTablewidget_1.render(df)

###########

# df_TradeRecord = pandas.read_excel('Data\TradeRecord.xlsx')
# 
# df_HoldingRecord = copy.deepcopy(df_TradeRecord)
# #df_HoldingRecord['09\n買價(本幣)'] = df_TradeRecord['08\n股數/單位'] * df_TradeRecord['09\n買價(本幣)']    		#將每單位買價均價由單價變成總額
# df_HoldingRecord = df_HoldingRecord.groupby(['00\n分類','01\n代號','02\n名稱','03\n戶口','06\n產品','16\n貨幣']).sum().reset_index()
# df_HoldingRecord = df_HoldingRecord.reindex(sorted(df_HoldingRecord.columns), axis=1)							#以header排序    
# df_HoldingRecord = df_HoldingRecord.sort_values(by='01\n代號',ascending=True)									#以欄值排序    
# #df_HoldingRecord['09\n買價(本幣)'] = df_HoldingRecord['10\n成本(本幣)']  / df_HoldingRecord['08\n股數/單位']
# 
# #df_HoldingRecord['09\n買價(本幣)'] = df_HoldingRecord['09\n買價(本幣)']  / df_HoldingRecord['08\n股數/單位']   	#將總額變回每單位
# print('96', df_HoldingRecord)
# if df_HoldingRecord['08\n股數/單位'].eq(0).any():
#     print('A trade is settled and the holding unit becomes zero.')
#     df_SettledRecord = pandas.DataFrame(columns=df_TradeRecord.columns)
#     print('100', df_SettledRecord)
#     target_index = df_HoldingRecord.loc[df_HoldingRecord['08\n股數/單位']==0,:].index.item()
#     print('target_index is', target_index)
#     target_code = df_HoldingRecord.at[target_index,'01\n代號']
#     print(target_code)
# 
#     df_HoldingRecord.drop(df_HoldingRecord[df_HoldingRecord['08\n股數/單位'] == 0].index, inplace = True)
#         
#     cond = df_TradeRecord['01\n代號'] == target_code
#     rows = df_TradeRecord.loc[cond, :]
#     df_SettledRecord = df_SettledRecord.append(rows, ignore_index=True)
#     df_SettledRecord.to_excel('Data\SettledRecord.xlsx', index=False)
#     df_TradeRecord.drop(rows.index, inplace=True)
#     df_TradeRecord.to_excel('Data\TradeRecord.xlsx', index=False)
#     print(df_TradeRecord)
#     print(df_SettledRecord)

###########

# my_variable = 56
# print(isinstance(my_variable, int))
# my_variable = 56.0
# print(isinstance(my_variable, float))
my_string = "we"
print(isinstance(my_string, str))

if isinstance(my_string, str):
    print('Yes')
else:
    print('No')

# f1 = float(my_string)
# print(f1, type(f1))

try:
    float(my_string)
    print('1')
except:
    print('2')

##############

# urlMatch = 'http://www.dyhjw.com/gold/kjzb.html' 							#self.location.tableWidget.item(i,28).text()      
# xpthMatch = "/html/body/div[10]/div[3]/div[1]/table/tbody/tr[4]/td[2]" 		#self.location.tableWidget.item(i,29).text()
# 
# headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) ''Chrome/51.0.2704.63 Safari/537.36'}                    
# url = urlMatch   
# #print('3-212: URL is ' , url)    ### for testing                
# page = requests.get(url, headers = headers, timeout = 30)
# #print('3-263: page is ' , page)    ### for testing 
# tree = html.fromstring(page.text)
# feature_bullets = tree.xpath(xpthMatch +'/text()')
# #print('3-266: Value is ' , feature_bullets)                                                ### for testing
# if str(feature_bullets) == '[]':
#     print('No content')
# else:
#     print(re.sub("人民幣 |\[|\'|\]|\,","",str(feature_bullets)))    # 刪除無用字符

###########

code1 = '600520.SS'
ticker = yfinance.Ticker(code1)
feature_bullets = ticker.info['currentPrice']
print(feature_bullets)
#print(ticker.info)
#Celltext = QTableWidgetItem(re.sub("人民幣 |\[|\'|\]","",str(feature_bullets)))

###########

code2 = '0P0001I84C.HK'
ticker = yfinance.Ticker(code2)
feature_bullets = ticker.info['regularMarketPrice']
print(feature_bullets)
print(ticker.info)
#Celltext = QTableWidgetItem(re.sub("人民幣 |\[|\'|\]","",str(feature_bullets)))

###########

# 股票代码
# stock_code = '600519'
# df1 = efinance.stock.get_quote_history(stock_code)
# # series1 = ef.stock.get_base_info(stock_code)
# print(df1.tail(1))

############

# print(ef.stock.get_daily_billboard())
# print(ef.fund.get_quote_history('161725'))
series2 = efinance.fund.get_base_info('161725')
# print(series2)
print(series2['最新净值'])

##########

# # Quick Examples
# 
# #Using drop() to delete rows based on column value
# df.drop(df[df['Fee'] >= 24000].index, inplace = True)
# 
# # Remove rows
# df2 = df[df.Fee >= 24000]
# 
# # If you have space in column name
# # Specify column name with in single quotes
# df2 = df[df['column name']]
# 
# # Using loc
# df2 = df.loc[df["Fee"] >= 24000 ]
# 
# # Delect rows based on multiple column value
# df2 = df[ (df['Fee'] >= 22000) & (df['Discount'] == 2300)]
# 
# # Drop rows with None/NaN
# df2 = df[df.Discount.notnull()]

"""
