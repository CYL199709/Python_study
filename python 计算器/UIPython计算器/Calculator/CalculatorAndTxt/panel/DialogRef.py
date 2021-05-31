#!usr/bin/env python3
# coding=utf-8
import wx
import sys

Version = "0.1"
ReleaseDate = "2019-9-21"

ID_FIND = 301
ID_FIND_NEXT = 302
ID_REPLACE = 303
ID_REPLACE_ALL = 304

class AboutDialog(wx.Dialog):
    def __init__(self, parent, id):
        wx.Dialog.__init__(self, parent, id, '关于', size=(200, 200))
        self.sizer = wx.BoxSizer(wx.VERTICAL)  # 流式布局
        self.sizer.Add(wx.StaticText(self, -1, '简单计算器'), 0, wx.ALIGN_CENTER_HORIZONTAL | wx.TOP, border=10)
        self.sizer.Add(wx.StaticText(self, -1, '@CopyRight 格桑工作室'), 0, wx.ALIGN_CENTER_HORIZONTAL | wx.TOP, border=5)
        self.sizer.Add(wx.StaticText(self, -1, 'Version %s，%s' % (Version, ReleaseDate)), 0, wx.ALIGN_CENTER_HORIZONTAL | wx.TOP, border=5)
        self.sizer.Add(wx.StaticText(self, -1, 'Author: 格桑'), 0, wx.ALIGN_CENTER_HORIZONTAL | wx.TOP, border=5)
        self.sizer.Add(wx.Button(self, wx.ID_OK), 0, wx.ALIGN_CENTER | wx.BOTTOM, border=10)
        self.SetSizer(self.sizer)

class SearchDialog(wx.Dialog):
    def __init__(self, parent, id):
        wx.Dialog.__init__(self, parent, id, '查找', size=(410, 175))
        self.app =  wx.GetApp()

        # 将控件放到Panel里面
        self.panel = wx.Panel(parent=self, id=-1)

        # 显示查找内容的静态文本
        wx.StaticText(parent=self.panel, id=-1, label='查找内容(&N)：',pos=(5, 20))

        # 输入查找内容的可编辑的文本
        self.findContentCtrl=wx.TextCtrl(parent=self.panel, id=-1, value='', pos=(85,20), size=(210,25))
        self.findContentCtrl.Bind(wx.EVT_TEXT, self.onText)

        # 放置一个按钮用于实现"查找下一个(&F)"功能
        self.findNextBtn = wx.Button(parent=self.panel, id=ID_FIND_NEXT, label='查找下一个(&F)', pos=(300,15), size=(85,30))
        self.findNextBtn.Disable()

        # 放置一个复选框用于实现"区分大小写(&C)"功能
        self.checkBox = wx.CheckBox(parent=self.panel, id=-1, label='区分大小写(&C)', pos=(5,100))
        self.checkBox.Bind(wx.EVT_CHECKBOX, self.onCaseSensitive)

        # 放置一个单选框用于实现"方向"功能
        listDirection=['向上(&U)', '向下(&D)']  # 在小标签为“方向”的容器中添加列表中的2个单选框
        self.radioDirection=wx.RadioBox(parent=self.panel, id=-1, label='方向', pos=(130,60), size=(165,60),
                                        choices=listDirection, majorDimension=2, style=wx.RA_SPECIFY_COLS)
        self.radioDirection.Bind(wx.EVT_RADIOBOX, self.onDirection)

        # 关闭该对话框
        self.cancelBtn = wx.Button(parent=self.panel, id=ID_FIND_NEXT, label='取消', pos=(300, 50),
                                     size=(85, 30))
        self.cancelBtn.Bind(wx.EVT_BUTTON, self.onCancel)

    def onText(self, event):
        self.findNextBtn.Enable(enable=True)
    def onCaseSensitive(self, event):
        pass
    def onDirection(self, event):
        pass
    def onCancel(self, event):
        self.Destroy()
        event.Skip()

class ReplaceDialog(wx.Dialog):
    def __init__(self, parent, id):
        wx.Dialog.__init__(self, parent, id, '替换', size=(410, 215))
        self.app =  wx.GetApp()

        # 将控件放到Panel里面
        self.panel = wx.Panel(parent=self, id=-1)

        # 显示查找内容的静态文本
        wx.StaticText(parent=self.panel, id=-1, label='查找内容(&N)：',pos=(5, 20))

        # 输入查找内容的可编辑的文本
        self.findContentCtrl=wx.TextCtrl(parent=self.panel, id=-1, value='', pos=(85,20), size=(210,25))
        self.findContentCtrl.Bind(wx.EVT_TEXT, self.onText)

        # 显示替换的静态文本
        wx.StaticText(parent=self.panel, id=-1, label="替换为(&P) : ", pos=(5, 50))

        # 输入替换为内容的可编辑的文本
        self.replaceContentCtrl=wx.TextCtrl(parent=self.panel, id=-1, value='', pos=(85,50), size=(210,25))
        self.replaceContentCtrl.Bind(wx.EVT_TEXT, self.onText)

        # 放置一个按钮用于实现"查找下一个(&F)"功能
        self.findNextBtn = wx.Button(parent=self.panel, id=ID_FIND_NEXT, label='查找下一个(&F)', pos=(300,15), size=(85,30))
        self.findNextBtn.Disable()

        # 放置一个复选框用于实现"区分大小写(&C)"功能
        self.checkBox = wx.CheckBox(parent=self.panel, id=-1, label='区分大小写(&C)', pos=(5,130))
        self.checkBox.Bind(wx.EVT_CHECKBOX, self.onCaseSensitive)

        # 放置一个按钮用于实现"替换(&R)"功能
        self.replaceBtn = wx.Button(parent=self.panel, id=ID_REPLACE, label='替换(&R)', pos=(300, 50),
                                     size=(85, 30))
        self.replaceBtn.Disable()

        # 放置一个按钮用于实现"全部替换(&A)"功能
        self.replaceAllBtn = wx.Button(parent=self.panel, id=ID_REPLACE, label='全部替换(&A)', pos=(300, 85),
                                        size=(85, 30))
        self.replaceAllBtn.Disable()

        # 关闭该对话框
        self.cancelBtn = wx.Button(parent=self.panel, id=ID_FIND_NEXT, label='取消', pos=(300, 120),
                                     size=(85, 30))
        self.cancelBtn.Bind(wx.EVT_BUTTON, self.onCancel)

    def onText(self, event):
        pass
    def onCaseSensitive(self, event):
        pass
    def onDirection(self, event):
        pass
    def onCancel(self, event):
        self.Destroy()
        event.Skip()



