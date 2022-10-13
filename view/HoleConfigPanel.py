#!/usr/bin/env python3
# -*- coding:utf-8 -*-
'''
# @Author: Xu Wang
# @Date: Wednesday, August 24th 2022
# @Email: wangxu.93@hotmail.com
# @Copyright (c) 2022 Institute of Trustworthy Network and System, Tsinghua University
'''

import Rhino as rc
import Eto.Forms as forms
import Eto.Drawing as drawing
from Eto.Drawing import Font
from model.HoleFrits import HoleArrangeType, HoleFrits
import rhinoscriptsyntax as rs
from frits import FritType
import utils

class HoleConfigPanel(forms.GroupBox):
    def __init__(self, parent, hole_config):
        self.parent = parent
        self.model = hole_config
        self.Text = '第{}排'.format(hole_config.hole_id)
        self.setup_view()
        self.display = rc.Display.CustomDisplay(True)
        self.display_color = rc.Display.ColorHSL(0.83,1.0,0.5)

    def setup_view(self):
        self.RemoveAll()
        self.basic_setting_label = forms.Label(Text='基础设置:', Font = Font('Microsoft YaHei', 12.))
        self.dot_type_label = forms.Label(Text = '花点类型：')
        self.dot_type_combo = forms.ComboBox()
        # self.dot_type_combo.Padding = drawing.Padding(20, 0, 0, 0)
        self.dot_type_combo.DataStore = FritType.get_frit_type_strings()
        self.dot_type_combo.SelectedIndex = self.model.dot_type
        self.dot_type_combo.SelectedIndexChanged += self.change_dot_type 
        # self.dot_type_combo.ReadOnly = True
        # for circle dot
        self.circle_dot_radius_label = forms.Label(Text='圆点半径：')
        self.circle_dot_radius = forms.TextBox(Text='{0}'.format(self.model.circle_config.r))
        self.circle_dot_radius.Size = drawing.Size(60, -1)
        self.circle_dot_radius.TextChanged += self.circle_dot_radius_changed
        
        self.round_rect_edge_label = forms.Label(Text='圆角矩形边长：')
        self.round_rect_edge = forms.TextBox(Text='{0}'.format(self.model.round_rect_config.k))
        self.round_rect_edge.Size = drawing.Size(60, -1)
        self.round_rect_edge.TextChanged += self.round_rect_edge_changed

        self.round_rect_radius_label = forms.Label(Text='圆角矩形半径：')
        self.round_rect_radius = forms.TextBox(Text='{0}'.format(self.model.round_rect_config.r))
        self.round_rect_radius.Size = drawing.Size(60, -1)
        self.round_rect_radius.TextChanged += self.round_rect_radius_changed

        self.stepping_label = forms.Label(Text='水平间距：')
        self.stepping_input = forms.TextBox(Text='{0}'.format(self.model.stepping))
        self.stepping_input.Size = drawing.Size(60, -1)
        self.stepping_input.TextChanged += self.stepping_input_changed

        self.position_label = forms.Label(Text='垂直间距：')
        self.position_input = forms.TextBox(Text='{0}'.format(self.model.vspace))
        self.position_input.Size = drawing.Size(60, -1)
        self.position_input.TextChanged += self.position_input_changed

        self.arrange_setting_label = forms.Label(Text='排布方式:', Font = Font('Microsoft YaHei', 12.))
        
        self.arrage_type_label = forms.Label(Text='类型：')
        self.arrage_type_combo = forms.ComboBox()
        self.arrage_type_combo.DataStore = HoleArrangeType.get_hole_arrange_type()  
        self.arrage_type_combo.SelectedIndex = self.model.arrange_type
        self.arrage_type_combo.SelectedIndexChanged += self.change_row_arrange_type

        self.config_panel = forms.Panel()
        self.update_btn = forms.Button(Text='填充花点')
        self.update_btn.Size = drawing.Size(100, 30)
        self.update_btn.Click += self.fill_row_frits

        self.layout = forms.DynamicLayout()
        self.layout.DefaultSpacing = drawing.Size(10, 10)
       
        # default is circle dot
        self.layout.BeginVertical(padding=drawing.Padding(10, 0, 0, 0), spacing=drawing.Size(10, 0))
        self.layout.AddRow(self.basic_setting_label, None)
        self.layout.EndVertical()
        self.layout.BeginVertical(padding=drawing.Padding(10, 0, 0, 0), spacing=drawing.Size(10, 0))
        if self.model.dot_type == FritType.CIRCLE_DOT:
            self.layout.AddRow(self.dot_type_label, self.dot_type_combo, self.circle_dot_radius_label, self.circle_dot_radius, self.stepping_label,
                self.stepping_input, self.position_label, self.position_input, None)
            
        elif self.model.dot_type == FritType.ROUND_RECT:
            self.layout.AddRow(self.dot_type_label, self.dot_type_combo, self.round_rect_edge_label, self.round_rect_edge, self.round_rect_radius_label,
                self.round_rect_radius, self.stepping_label, self.stepping_input, self.position_label, self.position_input, None)
        self.layout.EndVertical()
        self.layout.BeginVertical(padding=drawing.Padding(10, 0, 0, 0), spacing=drawing.Size(10, 0))
        self.layout.AddRow(self.arrange_setting_label, None)
        self.layout.EndVertical()
        self.layout.BeginVertical(padding=drawing.Padding(10, 0, 0, 0), spacing=drawing.Size(10, 0))
        self.layout.AddRow(self.arrage_type_label, self.arrage_type_combo, None)
        self.layout.EndVertical()
        self.layout.BeginVertical(padding=drawing.Padding(10, 0, 0, 0), spacing=drawing.Size(10, 0))
        self.layout.AddRow(self.update_btn, None)
        self.layout.EndVertical()
        self.Content = self.layout
    
    def change_dot_type(self, sender, e):
        if self.dot_type_combo.SelectedIndex == 0:
            self.model.dot_type = FritType.CIRCLE_DOT
        elif self.dot_type_combo.SelectedIndex == 1:
            self.model.dot_type = FritType.ROUND_RECT
        self.setup_view()

    def change_row_arrange_type(self, sender, e):
        self.model.arrange_type = self.arrage_type_combo.SelectedIndex

    def change_row_choice(self, sender, e):
        pass
    
    def circle_dot_radius_changed(self, sender, e):
        try:
            self.model.circle_config.r = float(self.circle_dot_radius.Text)
        except:
            pass
    
    def round_rect_edge_changed(self, sender, e):
        try:
            self.model.round_rect_config.k = float(self.round_rect_edge.Text)
        except:
            pass
    
    def round_rect_radius_changed(self, sender, e):
        try:
            self.model.round_rect_config.r = float(self.round_rect_radius.Text)
        except:
            pass
    
    def stepping_input_changed(self, sender, e):
        try:
            self.model.stepping = float(self.stepping_input.Text)
        except:
            pass
    
    def position_input_changed(self, sender, e):
        try:
            self.model.vspace = float(self.position_input.Text)
        except:
            pass

    def fill_row_frits(self, sender, e):
        self.clear_dots()
        self.model.fill_dots()
        # self.display.AddCurve(self.model.border_curve)
        for d in self.model.dots:
            d.draw(self.display, self.display_color)
    
    def clear_dots(self):
        self.display.Clear()
    
    def bake(self):
        layer_name = 'page_{0}_hole_{1}'.format(self.parent.page_id, self.model.hole_id)
        rs.AddLayer(layer_name, utils.get_color(self.model.hole_id), parent='fuyao_frits')
        for d in self.model.dots:
            obj = d.bake()
            rs.ObjectLayer(obj, layer_name)
        