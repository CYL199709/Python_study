#!usr/bin/env python3
# coding=utf-8

import os
import time

#import wx

from CalculatorAndTxt.panel.NoteBookRef import MyNoteBook
from CalculatorAndTxt.panel.CalculatePanelRef import CalculatePanel
Version = "0.1"
ReleaseDate = "2019-9-21"
ID_EXIT = 200
ID_ABOUT = 201

cwd = os.getcwd()

class MainFrame(wx.Frame):
    def __init__(self, parent, id, title):
        wx.Frame.__init__(self, parent, id, title, size=(310, 450))
        #######################创建状态栏#######################
        self.setupStatusBar()
        #######################创建菜单栏#######################
        self.setupMenuBar()
        #######################创建工具栏#######################
        # self.setupToolBar()
        #######################创建面板########################
        self.initUI()
        #######################标题栏图标#######################
        self.setupIcon()

    def initUI(self):
        self.calc_panel = CalculatePanel(parent=self, id=-1)

        ################Notebook的调用##########################
        # self.myNoteBook = MyNoteBook(parent=self, id=-1)


    def setupStatusBar(self):
        self.csb = self.CreateStatusBar(number=2)  # 将状态栏分2栏
        self.SetStatusWidths([-1, -1])  # 以2:1的长度比例分栏
        self.SetStatusText("Ready", 0)  # 在栏1里显示文本

        self.timer = wx.PyTimer(self.notify)  # derived from wx.Timer
        self.timer.Start(1000, wx.TIMER_CONTINUOUS)  # 以1秒钟的时间，不停在跑
        self.notify()  # 加上运行frame可以立即显示，否则需要等待1秒钟时间

    def setupMenuBar(self):
        menubar = wx.MenuBar()  # 创建菜单栏

        fmenu = wx.Menu() # 创建文件菜单
        quit_menu = wx.MenuItem(fmenu, ID_EXIT, '退出(&Q)', 'Terminate calculator')  # 创建'退出'菜单项
        quit_menu.SetBitmap(wx.Bitmap(cwd + "\\images\\quit.jpg"))
        fmenu.Append(quit_menu)
        menubar.Append(fmenu, '文件(&F)')

        hmenu = wx.Menu()  # 创建帮助菜单
        about_menu = wx.MenuItem(hmenu, ID_ABOUT, '关于&(A)', 'More information about calculator')  # 创建'关于'菜单项
        about_menu.SetBitmap(wx.Bitmap(cwd + "\\images\\about.jpg"))
        hmenu.Append(about_menu)
        menubar.Append(hmenu, '帮助(&H)')

        self.SetMenuBar(menubar)  # 将菜单栏显示到frame上

        # 为菜单项添加事件
        self.Bind(wx.EVT_MENU, self.onMenuExit, id=ID_EXIT)
        self.Bind(wx.EVT_MENU, self.onMenuAbout, id=ID_ABOUT)
        self.Bind(wx.EVT_CLOSE, self.onCloseWindow)

    def setupToolBar(self):
        self.toolbar = self.CreateToolBar()
    def setupIcon(self):
        self.icon_path = cwd + '\\images\\calcul.jpg'
        icon = wx.Icon(self.icon_path, wx.BITMAP_TYPE_JPEG)  # 将png转换成bitmap位图
        self.SetIcon(icon)

    def notify(self):
        st = time.strftime('%Y{y}%m{m}%d{d}  %H{h}%M{f}%S{s}').format(y='-', m='-', d='', h=':', f=':', s='')
        self.SetStatusText(st, 1)

    def onMenuExit(self, event):
        self.Close()  # 销毁frame主窗口
    def onMenuAbout(self, event):
        dlg = AboutDialog(None, -1)
        dlg.ShowModal()
        dlg.Destroy()
    def onCloseWindow(self, event):
        self.Destroy()  # 销毁主窗口或子窗口

class AboutDialog(wx.Dialog):
    def __init__(self, parent, id):
        wx.Dialog.__init__(self, parent, id, 'ABOUT ME', size=(200, 200))
        self.sizer = wx.BoxSizer(wx.VERTICAL)  # 流式布局
        self.sizer.Add(wx.StaticText(self, -1, '简单计算器'), 0, wx.ALIGN_CENTER_HORIZONTAL | wx.TOP, border=10)
        self.sizer.Add(wx.StaticText(self, -1, '@CopyRight 格桑工作室'), 0, wx.ALIGN_CENTER_HORIZONTAL | wx.TOP, border=5)
        self.sizer.Add(wx.StaticText(self, -1, 'Version %s，%s' % (Version, ReleaseDate)), 0, wx.ALIGN_CENTER_HORIZONTAL | wx.TOP, border=5)
        self.sizer.Add(wx.StaticText(self, -1, 'Author: 格桑'), 0, wx.ALIGN_CENTER_HORIZONTAL | wx.TOP, border=5)
        self.sizer.Add(wx.Button(self, wx.ID_OK), 0, wx.ALIGN_CENTER | wx.BOTTOM, border=10)
        self.SetSizer(self.sizer)

class MyApp(wx.App):
    def __init__(self):
        wx.App.__init__(self)

    def OnInit(self):
        self.title = "计算器"
        self.frame = MainFrame(None, -1, self.title)
        self.SetTopWindow(self.frame)
        self.frame.Center()
        self.frame.Show(show=True)
        return True

def main():
    app = MyApp()
    app.MainLoop()
    #####################对于MainLoop()函数的理解与下面的伪代码实质是一样的################
    '''
    def mainloop():
	while the main window has not been closed:
		if an event has occurred:
			run the associated event handler function
	'''

if __name__ == '__main__':
    main()


