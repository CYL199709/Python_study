#!usr/bin/env python3
# coding=utf-8

import wx

class TxtPanel(wx.Panel):
    def __init__(self, parent, id):
        super(TxtPanel, self).__init__(parent, id)
        self.app = wx.GetApp()

        vboxsizer = wx.BoxSizer(wx.VERTICAL)
        self.txtResultCtrl=wx.TextCtrl(parent=self, id=-1, value='', style=wx.TE_MULTILINE | wx.TE_RICH2)
        vboxsizer.Add(window=self.txtResultCtrl, proportion=1, flag=wx.EXPAND)
        self.SetSizer(vboxsizer)

        self.txtResultCtrl.Bind(wx.EVT_LEFT_UP, self.getSelectStringCursor)
        self.txtResultCtrl.Bind(wx.EVT_TEXT, self.onPaintMotion)

    def getSelectStringCursor(self, event):
        m=self.txtResultCtrl.GetStringSelection()
        print(m)
        event.Skip()

    def onPaintMotion(self, event):
        line = self.txtResultCtrl.GetNumberOfLines()
        wordLen = self.txtResultCtrl.GetLineLength(lineNo=line)
        num = len(self.txtResultCtrl.GetValue().strip())
        self.app.frame.csb.SetStatusText(u"第{}行{}列， 共{}字" .format(line, wordLen, num),1)
        event.Skip()

