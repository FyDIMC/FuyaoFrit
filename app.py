#!/usr/bin/env python3
# -*- coding:utf-8 -*-
'''
# @Author: Xu Wang
# @Date: Wednesday, August 17th 2022
# @Email: wangxu.93@hotmail.com
# @Copyright (c) 2022 Institute of Trustworthy Network and System, Tsinghua University
'''
import imp
import Rhino
import Eto.Forms as forms
import Eto.Drawing as drawing
from Eto.Drawing import Size, Font, FontStyle
import view.RowConfigPanel as RowConfigPanel
import view.DefaultPage as DefaultPage
import view.BandPage
reload(view.BandPage)
reload(RowConfigPanel)
reload(DefaultPage)
import os
# from RowControl import RowControl

class FritDialog(forms.Dialog[bool]):
    def __init__(self):
        self.Title = '福耀印刷花点排布工具'
        self.Padding = drawing.Padding(10)
        self.Resizable = False
        self.Closing += self.OnFormClosed
        self.MinimumSize = Size(800, 600)

        self.display = Rhino.Display.CustomDisplay(True)
        self.display.Clear()

        # 菜单
        self.create_menu()
        self.tab = forms.TabControl()
        self.tab.TabPosition = forms.DockPosition.Top
        default_page = DefaultPage.DefaultPage()
        # default_page.create()
        self.tab.Pages.Add(default_page)
        page = view.BandPage.BandPageView(self.display)
        self.tab.Pages.Add(page)

 
        # 标题
        # self.heading_label = forms.Label(Text= '带状区域', Font = Font('Microsoft YaHei', 14., FontStyle.Bold))
        # # self.m_headding.Color = drawing.Color.FromArgb(255, 0, 0)
        # self.heading_label.TextAlignment = forms.TextAlignment.Center
        # self.addButton = forms.Button(Text='添加行')
        # self.addButton.Click += self.AddButtonClick
        self.layout = forms.DynamicLayout()
        # default is circle dot
        self.layout.AddRow(self.tab)
        self.Content = self.layout 

    def create_menu(self):
        self.Menu = forms.MenuBar()
        current_path = os.getcwd()
        
        file_menu = self.Menu.Items.GetSubmenu("文件")
        edit_menu = self.Menu.Items.GetSubmenu("编辑")
        
        open_menu = forms.Command()
        open_menu.MenuText = "打开"
        open_menu.Image = drawing.Bitmap(current_path + '\\ico\\file-open.png')
        file_menu.Items.Add(open_menu, 0)
        
        add_region_menu = forms.Command(self.AddBandRegionCommand)
        add_region_menu.MenuText = "添加区域"
        add_region_menu.Image = drawing.Bitmap(current_path + '\\ico\\add-region.png')
        edit_menu.Items.Add(add_region_menu)

    # Start of the class functions
    def OnFormClosed(self, sender, e):
        # self.display.clear()
        pass

    def AddBandRegionCommand(self, sender, e):
        page = view.BandPage.BandPage(self.display)
        self.tab.Pages.Add(page)
        

if __name__ == "__main__":
    dialog = FritDialog();
    # rc = dialog.ShowModal(Rhino.UI.RhinoEtoApp.MainWindow)
    Rhino.UI.EtoExtensions.ShowSemiModal(dialog, Rhino.RhinoDoc.ActiveDoc, Rhino.UI.RhinoEtoApp.MainWindow)