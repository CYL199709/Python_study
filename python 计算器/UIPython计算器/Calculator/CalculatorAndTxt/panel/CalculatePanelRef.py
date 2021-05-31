#!usr/bin/env python3
# coding=utf-8

import wx
import math

ID_CALC = 300

class CalculatePanel(wx.Panel):
    def __init__(self, parent, id):
        super(CalculatePanel, self).__init__(parent, id)
        global ID_CALC
        # self.calc_panel = CalculatePanel(self, -1)
        self.resultStr = ''  # 在面板上定义存储在文本中的变量

        #########在面板放置多行可控文本#########
        #########方式1：坐标式布局###########
        # self.calc_panel.resultTextCtrl = wx.TextCtrl(self.calc_panel, -1, '', pos=(20, 10), size=(250, 50),
        #                                              style=wx.TE_MULTILINE | wx.TE_RICH2)
        # font = wx.Font(18, wx.FONTFAMILY_ROMAN, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD, underline=False)
        # self.calc_panel.resultTextCtrl.SetFont(font)  # 设置面板下可控文本字体中的颜色
        # button_lists = ['7', '8', '9', 'DEL', 'AC', '4', '5', '6', '*', '/', '1', '2', '3', '+', '-',
        #                 '0', '%', 'PI', 'e', 'sqrt', '^', 'sin', 'cos', 'tan', 'log', 'ln', '(', ')', '.', '=']
        # for i, button in enumerate(button_lists):
        #     wx.Button(self.calc_panel, ID_CALC, label='{}'.format(button), pos=(20 + 50*(i%5), 70+50*int(i/5)), size=(50, 40))
        #     self.Bind(wx.EVT_BUTTON, self.calc_panel.onCalcClick, id=ID_CALC)  # 通过绑定按钮的id进行事件绑定（平常是通过事件+按钮对象+事件处理器进行事件绑定）
        #     ID_CALC += 1

        ############方式2：流式布局BoxSizer与网格布局GridSizer结合############
        self.resultTextCtrl = wx.TextCtrl(parent=self, id=-1, value='', pos=(20, 10),
                                                     size=(250, 50),
                                                     style=wx.TE_MULTILINE | wx.TE_RICH2)

        vboxsizer = wx.BoxSizer(wx.VERTICAL)
        vboxsizer.Add(window=self.resultTextCtrl, proportion=0, flag=wx.ALL | wx.ALIGN_CENTER_HORIZONTAL,
                      border=10)
        font = wx.Font(pointSize=18, family=wx.FONTFAMILY_ROMAN, style=wx.FONTSTYLE_NORMAL, weight=wx.FONTWEIGHT_BOLD,
                       underline=False)
        self.resultTextCtrl.SetFont(font)  # 设置面板下可控文本字体中的颜色
        button_lists = ['7', '8', '9', 'DEL', 'AC', '4', '5', '6', '*', '/', '1', '2', '3', '+', '-',
                        '0', '%', 'PI', 'e', 'sqrt', '^', 'sin', 'cos', 'tan', 'log', 'ln', '(', ')', '.', '=']
        buttons = []
        for i, button in enumerate(button_lists):
            buttons.append(wx.Button(parent=self, id=ID_CALC, label='{}'.format(button), size=(50, 40),
                                     style=wx.EXPAND))
            self.Bind(wx.EVT_BUTTON, self.onCalcClick, id=ID_CALC)
            ID_CALC += 1
        gridsizer = wx.GridSizer(rows=6, cols=5, vgap=5, hgap=5)  # vgap、hgap表示控件在垂直，水平方向的间隙，以pixel为单位
        gridsizer.AddMany(buttons)  # AddMany(items)下的items可为列表和元组
        vboxsizer.Add(sizer=gridsizer, proportion=0, flag=wx.ALL | wx.ALIGN_CENTER_HORIZONTAL | wx.EXPAND, border=10)
        self.SetSizer(vboxsizer)

    def setResultText(self, value):
        # self.app = wx.GetApp()
        # self.resultTextCtrl = self.app.frame.calc_panel.resultTextCtrl
        # self.resultStr = self.app.frame.calc_panel.resultStr
        self.resultTextCtrl.SetValue(value)

    def onCalcClick(self, event):
        print('触发事件的id：{}, 触发的事件：{}'.format(event.GetId(), event.GetEventObject().GetLabel()))
        mathFunc = ['sqrt', 'sin', 'cos', 'tan']
        result = 'Error'
        if event.GetEventObject().GetLabel() == '=':
            for func in mathFunc:
                if func in self.resultStr:
                    try:
                        result = str(eval('math.' + self.resultStr))
                        # result = 'math.' + self.resultStr
                        break
                    except:
                        pass
            if '^' in self.resultStr:
                try:
                    temp = self.resultStr.split('^')
                    result = str(eval('pow(' + temp[0] + ',' + temp[1] + ')'))
                    # result = 'pow(' + temp[0] + ',' + temp[1] + ')'
                except:
                    pass
            elif 'ln' in self.resultStr:
                try:
                    result = str(eval('math.log' + self.resultStr[2:]))  # 从2开始，直接将ln(x)-->(x)字符串提取出来
                except:
                    pass
            elif 'log' in self.resultStr:
                try:
                    result = str(eval('math.log' + self.resultStr[3:] + '/math.log(10)'))
                except:
                    pass
            else:
                try:
                    result = str(eval(self.resultStr))
                    # result = self.resultStr
                except:
                    pass
            self.resultStr = result
            self.setResultText(self.resultStr)
            event.Skip()
        elif event.GetEventObject().GetLabel() == 'AC':
            '''click 'AC' button to clear screen (all clear缩写)'''
            self.resultTextCtrl.SetValue('')  # 多行文本框清空
            self.resultStr = ''  # 存储文本框内存清空
            event.Skip()
        elif event.GetEventObject().GetLabel() == 'DEL':
            '''click button "DEL" to Undo'''
            self.resultStr = self.resultStr[:-1]  # 将最后一个元素删除
            self.setResultText(self.resultStr)
            event.Skip()
        elif event.GetEventObject().GetLabel() == 'e':
            self.resultStr += str(round(math.e,6))
            self.setResultText(self.resultStr)
            event.Skip()
        elif event.GetEventObject().GetLabel() == 'PI':
            self.resultStr += str(round(math.pi,6))
            self.setResultText(self.resultStr)
            event.Skip()
        else:
            self.resultStr += event.GetEventObject().GetLabel()
            self.setResultText(self.resultStr)
            event.Skip()

