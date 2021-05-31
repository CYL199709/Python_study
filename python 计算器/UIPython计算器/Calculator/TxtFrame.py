#!usr/bin/env python3
# coding=utf-8

import os
import time

import wx

from CalculatorAndTxt.panel.NoteBookRef import MyNoteBook
from CalculatorAndTxt.panel.CalculatePanelRef import CalculatePanel
from CalculatorAndTxt.panel.DialogRef import AboutDialog, SearchDialog, ReplaceDialog
Version = "0.1"
ReleaseDate = "2019-9-22"

ID_EXIT = 200
ID_ABOUT = 201
ID_NEW = 202
ID_OPEN = 203
ID_OPEN_DIR = 204
ID_SAVE = 205
ID_SAVE_AS = 206
ID_UNDO = 207
ID_CUT = 208
ID_COPY = 209
ID_PASTE = 210
ID_DELETE = 211

ID_FIND = 212
ID_FIND_NEXT = 213
ID_REPLACE = 214

ID_SELECT_ALL = 215

cwd = os.getcwd()

class MainFrame(wx.Frame):
    def __init__(self, parent, id, title):
        wx.Frame.__init__(self, parent, id, title, size=(640, 480))
        self.cur_file = ''  # current operate file
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
        ################Notebook的调用##########################
        self.myNoteBook = MyNoteBook(parent=self, id=-1)
        ################查找和替换###############################
        self.find_dlg = None
        self.find_data = wx.FindReplaceData()

        self.Bind(wx.EVT_FIND, self.doFind)
        self.Bind(wx.EVT_FIND_NEXT, self.doFind)
        self.Bind(wx.EVT_FIND_REPLACE, self.doReplace)
        self.Bind(wx.EVT_FIND_REPLACE_ALL, self.doReplaceAll)
        self.Bind(wx.EVT_FIND_CLOSE, self.doFindClose)
        self.Bind(wx.EVT_CLOSE, self.doQuit)

    def _initFindReplaceDialog(self, mode):
        if mode == ID_REPLACE:
            style=(wx.FR_NOUPDOWN|wx.FR_NOMATCHCASE|wx.FR_NOWHOLEWORD|wx.FR_REPLACEDIALOG)  # 设置替换Dialog的style
            self.find_dlg = wx.FindReplaceDialog(parent=self, data=self.find_data, title='替换', style=style)
        else:
            self.find_dlg = wx.FindReplaceDialog(parent=self, data=self.find_data, title='替换', style=0)


    def setupStatusBar(self):
        self.csb = self.CreateStatusBar(number=3)  # 将状态栏分2栏
        self.SetStatusWidths([-2, -2, -1])  # 以2:1的长度比例分栏
        self.SetStatusText("Ready", 0)  # 在栏1里显示文本
        self.SetStatusText("", 1)  # 在栏1里显示文本

        self.timer = wx.PyTimer(self.notify)  # derived from wx.Timer
        self.timer.Start(1000, wx.TIMER_CONTINUOUS)  # 以1秒钟的时间，不停在跑
        self.notify()  # 加上运行frame可以立即显示，否则需要等待1秒钟时间

    def setupMenuBar(self):
        ######################创建菜单栏#################
        menubar = wx.MenuBar()

        ######################创建文件菜单#######################
        file_menu = wx.Menu()
        ######################创建菜单项：新建####################
        new_menu_item = wx.MenuItem(parentMenu=file_menu, id=ID_NEW, text='新建(&N)')
        new_menu_item.SetBitmap(bmp=wx.Bitmap(name=cwd + '\\images\\new.jpg'))
        file_menu.Append(menuItem=new_menu_item)
        self.Bind(wx.EVT_MENU, self.onNewFile, id=ID_NEW)
        ######################创建菜单项：打开####################
        open_menu_item = wx.MenuItem(parentMenu=file_menu, id=ID_OPEN, text='打开(&O)')
        open_menu_item.SetBitmap(bmp=wx.Bitmap(name=cwd + '\\images\\open.jpg'))
        file_menu.Append(menuItem=open_menu_item)
        self.Bind(wx.EVT_MENU, self.onOpen, id=ID_OPEN)
        ######################创建菜单项：保存####################
        save_menu_item = wx.MenuItem(parentMenu=file_menu, id=ID_SAVE, text='保存(&S)')
        save_menu_item.SetBitmap(bmp=wx.Bitmap(name=cwd + '\\images\\save.jpg'))
        file_menu.Append(menuItem=save_menu_item)
        self.Bind(wx.EVT_MENU, self.onSave, id=ID_SAVE)

        file_menu.AppendSeparator()  # 添加菜单的分割线

        ######################创建菜单项：退出####################
        quit_menu = wx.MenuItem(parentMenu=file_menu, id=ID_EXIT, text='退出(&Q)', helpString='Terminate calculator')  # 创建'退出'菜单项
        quit_menu.SetBitmap(bmp=wx.Bitmap(name=cwd + "\\images\\quit.jpg"))
        file_menu.Append(menuItem=quit_menu)
        self.Bind(wx.EVT_MENU, self.onMenuExit, id=ID_EXIT)

        menubar.Append(menu=file_menu, title='文件(&F)')  # 将菜单文件添加到菜单栏

        ######################创建编辑菜单#######################
        edit_menu = wx.Menu()
        ######################创建菜单项：撤销####################
        undo_menu_item = wx.MenuItem(parentMenu=edit_menu, id=ID_UNDO, text='撤销(&U)')
        undo_menu_item.SetBitmap(bmp=wx.Bitmap(name=cwd + '\\images\\undo.jpg'))
        edit_menu.Append(menuItem=undo_menu_item)
        self.Bind(wx.EVT_MENU, self.onUndo, id=ID_UNDO)

        edit_menu.AppendSeparator()

        ######################创建菜单项：剪切####################
        cut_menu_item = wx.MenuItem(parentMenu=edit_menu, id=ID_CUT, text='剪切(&T)')
        cut_menu_item.SetBitmap(bmp=wx.Bitmap(name=cwd + '\\images\\cut.jpg'))
        edit_menu.Append(menuItem=cut_menu_item)
        self.Bind(wx.EVT_MENU, self.onCut, id=ID_CUT)
        ######################创建菜单项：复制####################
        copy_menu_item = wx.MenuItem(parentMenu=edit_menu, id=ID_COPY, text='复制(&C)')
        copy_menu_item.SetBitmap(bmp=wx.Bitmap(name=cwd + '\\images\\copy.jpg'))
        edit_menu.Append(menuItem=copy_menu_item)
        self.Bind(wx.EVT_MENU, self.onCopy, id=ID_COPY)
        ######################创建菜单项：粘贴####################
        paste_menu_item = wx.MenuItem(parentMenu=edit_menu, id=ID_PASTE, text='粘贴(&P)')
        paste_menu_item.SetBitmap(bmp=wx.Bitmap(name=cwd + '\\images\\paste.jpg'))
        edit_menu.Append(menuItem=paste_menu_item)
        self.Bind(wx.EVT_MENU, self.onPaste, id=ID_PASTE)
        ######################创建菜单项：删除####################
        del_menu_item = wx.MenuItem(parentMenu=edit_menu, id=ID_DELETE, text='删除(&D)')
        del_menu_item.SetBitmap(bmp=wx.Bitmap(name=cwd + '\\images\\delete.jpg'))
        edit_menu.Append(menuItem=del_menu_item)
        self.Bind(wx.EVT_MENU, self.onDelete, id=ID_DELETE)

        edit_menu.AppendSeparator()

        ######################创建菜单项：查找####################
        find_menu_item = wx.MenuItem(parentMenu=edit_menu, id=ID_FIND, text='查找(&F)')
        find_menu_item.SetBitmap(bmp=wx.Bitmap(name=cwd + '\\images\\search.jpg'))
        edit_menu.Append(menuItem=find_menu_item)
        self.Bind(wx.EVT_MENU, self.onFind, id=ID_FIND)
        ######################创建菜单项：查找下一个####################
        find_next_menu_item = wx.MenuItem(parentMenu=edit_menu, id=ID_FIND_NEXT, text='查找下一个(&N)')
        find_next_menu_item.SetBitmap(bmp=wx.Bitmap(name=cwd + '\\images\\search_next.jpg'))
        edit_menu.Append(menuItem=find_next_menu_item)
        self.Bind(wx.EVT_MENU, self.onFindNext, id=ID_FIND_NEXT)
        ######################创建菜单项：替换####################
        replace_menu_item = wx.MenuItem(parentMenu=edit_menu, id=ID_REPLACE, text='替换(&R)')
        replace_menu_item.SetBitmap(bmp=wx.Bitmap(name=cwd + '\\images\\replace.jpg'))
        edit_menu.Append(menuItem=replace_menu_item)
        self.Bind(wx.EVT_MENU, self.onReplace, id=ID_REPLACE)

        edit_menu.AppendSeparator()

        ######################创建菜单项：全选####################
        select_all_menu_item = wx.MenuItem(parentMenu=edit_menu, id=ID_SELECT_ALL, text='全选(&A)')
        select_all_menu_item.SetBitmap(bmp=wx.Bitmap(name=cwd + '\\images\\select_all.jpg'))
        edit_menu.Append(menuItem=select_all_menu_item)
        self.Bind(wx.EVT_MENU, self.onSelectAll, id=ID_SELECT_ALL)

        menubar.Append(menu=edit_menu, title='编辑(&E)')  # 将菜单编辑添加到菜单栏

        ######################创建帮助菜单#######################
        help_menu = wx.Menu()
        ######################创建菜单项：关于####################
        about_menu = wx.MenuItem(help_menu, ID_ABOUT, '关于&(A)', 'More information')  # 创建'关于'菜单项
        about_menu.SetBitmap(wx.Bitmap(cwd + "\\images\\about.jpg"))
        help_menu.Append(about_menu)
        menubar.Append(help_menu, '帮助(&H)')
        self.Bind(wx.EVT_MENU, self.onMenuAbout, id=ID_ABOUT)

        self.SetMenuBar(menubar)  # 将菜单栏显示到frame上

        self.Bind(wx.EVT_CLOSE, self.onCloseWindow)  # 窗体关闭事件，注意此处没有绑定id

    def setupToolBar(self):
        self.toolbar = self.CreateToolBar()

    def setupIcon(self):
        self.icon_path = cwd + '\\images\\alienware.png'
        icon = wx.Icon(self.icon_path, wx.BITMAP_TYPE_PNG)  # 将png转换成bitmap位图
        self.SetIcon(icon)

    def notify(self):
        st = time.strftime('%Y{y}%m{m}%d{d} %H{h}%M{f}%S{s}').format(y='-', m='-', d='', h=':', f=':', s='')
        self.SetStatusText(st, 2)

    def onMenuExit(self, event):
        self.Close()  # 销毁frame主窗口
        event.Skip()

    def onMenuAbout(self, event):
        dlg = AboutDialog(None, -1)
        dlg.ShowModal()
        dlg.Destroy()
        event.Skip()

    def onCloseWindow(self, event):
        self.Destroy()  # 销毁主窗口或子窗口
        event.Skip()

    def onNewFile(self, event):
        if not self.myNoteBook.txtpanel.txtResultCtrl.IsEmpty():  # 判断多行文本框不为空时
            ########################信息对话框##########################################
            message_dlg = wx.MessageDialog(parent=self,message='是否将更改保存到无标题?',caption='记事本',
                                           style=wx.YES_NO | wx.ICON_QUESTION | wx.CANCEL)
            retCode = message_dlg.ShowModal()
            if retCode == wx.ID_YES:
                self.onSave(event)  # 保存
                self.myNoteBook.txtpanel.txtResultCtrl.SetValue('')  # 保存完创建新的文件夹
            elif retCode == wx.ID_NO:
                self.myNoteBook.txtpanel.txtResultCtrl.SetValue('')  # 清空
            else:
                message_dlg.Close()  # 取消
            message_dlg.Destroy()
            self.myNoteBook.txtpanel.txtResultCtrl.Refresh()  # 刷新
            event.Skip()

    def onOpen(self, event):
        """
        wx.FD_OPEN
        wx.FD_SAVE
        wx.FD_OVERWRITE_PROMPT
        wx.FD_MULTIPLE
        wx.FD_CHANGE_DIR
        """
        self.dirname=''
        fileFilter = "Text (*.txt)|*.txt|Python (*.py)|*.py|All files (*.*)|*.*"  # 文件过滤器
        ################################文件对话框###########################################
        file_dlg = wx.FileDialog(parent=self,message='选择文件', defaultDir=self.dirname,
                                 wildcard=fileFilter, style=wx.FD_OPEN)
        if file_dlg.ShowModal() == wx.ID_OK:
            self.filename =file_dlg.GetFilename()  # 获取文件名
            self.dirname = file_dlg.GetDirectory()  # 获取文件路径
            with open(os.path.join(self.dirname, self.filename), 'r', encoding='utf-8') as f:
                self.myNoteBook.txtpanel.txtResultCtrl.SetValue(f.read())
        file_dlg.Destroy()
        self.myNoteBook.txtpanel.txtResultCtrl.SetFocus()
        ########################将静态文本放入状态栏显示#################################
        wx.StaticText(parent=self.csb, id=-1,
                      label='文件名：' + self.filename + '，共' + str(self.myNoteBook.txtpanel.txtResultCtrl.GetNumberOfLines()) + '行',pos=(0,1))
        self.myNoteBook.txtpanel.txtResultCtrl.Refresh()
        event.Skip()

    def onSave(self, event):
        if self.myNoteBook.txtpanel.txtResultCtrl.IsEmpty():
            return
        self.dirname=''
        fileFilter = "Text (*.txt)|*.txt|Python (*.py)|*.py|All files (*.*)|*.*"
        file_dlg = wx.FileDialog(parent=self,message='保存文件', defaultDir=self.dirname,
                                 wildcard=fileFilter, style=wx.FD_SAVE)
        if file_dlg.ShowModal() == wx.ID_OK:
            self.filename =file_dlg.GetFilename()
            self.dirname = file_dlg.GetDirectory()
            with open(os.path.join(self.dirname, self.filename), 'w', encoding='utf-8') as f:
                f.write(self.myNoteBook.txtpanel.txtResultCtrl.GetValue())
        file_dlg.Destroy()
        self.Title = self.filename + ' - 记事本'

    def onUndo(self, event):
        """Undo select text"""
        self.myNoteBook.txtpanel.txtResultCtrl.Undo()  # 对多行文本实现撤销操作
        event.Skip()

    def onCut(self, event):
        """Cut select text"""
        self.myNoteBook.txtpanel.txtResultCtrl.Cut()  # 对多行文本实现剪切操作
        event.Skip()

    def onCopy(self, event):
        """Copy select text"""
        # self.myNoteBook.txtpanel.txtResultCtrl.Copy()  # 对多行文本实现复制操作，不是太好用

        ###################rewrite###############################
        text_obj = wx.TextDataObject()  # 获得多行文本框的对象
        text_obj.SetText(self.myNoteBook.txtpanel.txtResultCtrl.GetStringSelection())  # 获取选中的文本
        if wx.TheClipboard.IsOpened() or wx.TheClipboard.Open():  # 判断粘贴板是否打开
            wx.TheClipboard.SetData(text_obj)  # 将获取的文本对象放到粘贴板上
            wx.TheClipboard.Close()  # 关闭粘贴板
        else:  # 粘贴板没有打开的话
            wx.MessageBox(message='Unable to open the clipboard', caption='Error')
        self.myNoteBook.txtpanel.txtResultCtrl.Refresh()
        event.Skip()

    def onPaste(self, event):
        """Paste s进化理论elect text"""
        # self.myNoteBook.txtpanel.txtResultCtrl.Paste()  # 对多行文本实现粘贴操作，不是太好用

        #####################rewrite####################
        text_obj = wx.TextDataObject()  # 获得多行文本框的对象
        if wx.TheClipboard.IsOpened() or wx.TheClipboard.Open():
            if wx.TheClipboard.GetData(text_obj):
                self.myNoteBook.txtpanel.txtResultCtrl.GetInsertionPoint()
                self.myNoteBook.txtpanel.txtResultCtrl.SetValue(text_obj.GetText())
            wx.TheClipboard.Close()
        else:
            pass
        self.myNoteBook.txtpanel.txtResultCtrl.Refresh()
        event.Skip()

    def onDelete(self, event):
        """Delete select text"""
        # self.myNoteBook.txtpanel.txtResultCtrl.Clear()  # delete all text
        start, end = self.myNoteBook.txtpanel.txtResultCtrl.GetSelection()
        self.myNoteBook.txtpanel.txtResultCtrl.Remove(start, end)
        self.myNoteBook.txtpanel.txtResultCtrl.Refresh()
        event.Skip()

    def onFind(self, event):
        ###################方式1：自制查找Dialog#####################
        # dlg = SearchDialog(None, -1)
        # dlg.ShowModal()
        # dlg.Destroy()
        # event.Skip()
        ###################方式2：调用wx.FindReplaceData()、wx.FindReplaceDialog()两个类库制作查找Dialog##############
        print('onFind')
        evt_id = event.GetId()
        if evt_id in (ID_FIND, ID_FIND_NEXT):  # 查找包含查找与查找下一个两项
            self._initFindReplaceDialog(evt_id)
            self.find_dlg.Show()
        else:
            event.Skip()
        print('onFind over')

    def onFindNext(self, event):
        ###################方式1：自制查找下一个Dialog#####################
        # dlg = SearchDialog(None, -1)
        # dlg = SearchDialog(None, -1)
        # if dlg.findContentCtrl.GetValue() == "":
        #     dlg.ShowModal()
        #     dlg.Destroy()
        # else:
        #     pass
        # event.Skip()
        ###################方式2：调用wx.FindReplaceData()、wx.FindReplaceDialog()两个类库制作查找下一个Dialog##############
        print('onFindNext')
        evt_id = event.GetId()
        if evt_id in (ID_FIND_NEXT,):  # 查找包含查找与查找下一个两项
            self._initFindReplaceDialog(evt_id)
            self.find_dlg.Show()
        else:
            event.Skip()
        print('onFindNext over')

    def onReplace(self, event):
        ###################方式1：自制替换Dialog#####################
        # dlg = ReplaceDialog(None, -1)
        # dlg.ShowModal()
        # dlg.Destroy()
        # event.Skip()
        ###################方式2：调用wx.FindReplaceData()、wx.FindReplaceDialog()两个类库制作替换Dialog##############
        print('onReplace')
        evt_id = event.GetId()
        if evt_id in (ID_REPLACE,):  # 查找包含查找与查找下一个两项
            self._initFindReplaceDialog(evt_id)
            self.find_dlg.Show()
        else:
            event.Skip()
        print('onReplace over')

    def doFind(self, event):
        findStr = self.find_data.GetFindString()  # 获取查找Dialog的文本框数据
        if not self.findString(findStr):  # 如果没有查找到
            wx.Bell()  # 发出Dialog弹出响声
            style = wx.YES_NO | wx.ICON_WARNING | wx.CENTRE
            message = ("没有查找到你需要的内容，\n\n 或者已经到了文本的头或尾。") # 用\n\n可以控制上行和下行字体大小
            wx.MessageBox(message=message, caption='查找结果提示?', style=style)
        event.Skip()

    def doReplace(self, event):
        fstring = self.find_data.GetFindString()  # 获取Dialog中查找文本框的内容
        rstring = self.find_data.GetReplaceString()  # 获取Dialog中替换文本框的内容
        self.myNoteBook.txtpanel.txtResultCtrl.SetInsertionPoint(0)  # 设置光标在初始点处
        cpos = self.myNoteBook.txtpanel.txtResultCtrl.GetInsertionPoint()  # 获取光标位置
        start, end = cpos, cpos
        if fstring:
            if self.findString(fstring):
                start, end = self.myNoteBook.txtpanel.txtResultCtrl.GetSelection()  # 获取查到到的from和to部分
            self.myNoteBook.txtpanel.txtResultCtrl.Replace(start, end, rstring)
        event.Skip()

    def doReplaceAll(self, event):
        rstring = self.find_data.GetReplaceString()
        fstring = self.find_data.GetFindString()
        text = self.myNoteBook.txtpanel.txtResultCtrl.GetValue()
        newtext = text.replace(fstring, rstring)  # 直接用内置的replace函数替换所有
        self.myNoteBook.txtpanel.txtResultCtrl.TXResult.SetValue(newtext)
        event.Skip()

    def doFindClose(self, event):
        if self.find_dlg:
            self.find_dlg.Destroy()
            self.find_dlg =None
        event.Skip()
    def doQuit(self, event):
        pass
    def findString(self, findStr):
        pass

    def onSelectAll(self, event):
        self.myNoteBook.txtpanel.txtResultCtrl.SelectAll()
        self.myNoteBook.txtpanel.Refresh()
        event.Skip()



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

if __name__ == '__main__':
    main()
