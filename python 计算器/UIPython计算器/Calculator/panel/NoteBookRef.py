#!usr/bin/env python3
# coding=utf-8

import wx
from CalculatorAndTxt.panel.CalculatePanelRef import CalculatePanel
from CalculatorAndTxt.panel.TxtPanelRef import TxtPanel

class MyNoteBook(wx.Notebook):
    def __init__(self, parent, id):
        super(MyNoteBook, self).__init__(parent, id)
        self.panels = []

        ###############为界面设置Notebook#################
        self.txtpanel=TxtPanel(parent=self, id=-1)
        self.panels.append(self.txtpanel)
        self.AddPage(page=self.panels[0], text='记事本')

        self.calculatepanel = CalculatePanel(parent=self, id=-1)
        self.panels.append(self.calculatepanel)
        self.AddPage(page=self.panels[1], text='计算器')