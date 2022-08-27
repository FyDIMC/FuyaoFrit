#!/usr/bin/env python3
# -*- coding:utf-8 -*-
'''
# @Author: Xu Wang
# @Date: Tuesday, August 16th 2022
# @Email: wangxu.93@hotmail.com
# @Copyright (c) 2022 Institute of Trustworthy Network and System, Tsinghua University
'''
import Rhino as rc

class Dot:
    def __init__(self, x, y, config, theta):
        self.centroid = rc.Geometry.Point3d(x, y, 0)
        self.theta = theta
        self.config = config
        self.curve = None

    def draw(self):
        print("Dot: this function should not be executed!")
    
    
    