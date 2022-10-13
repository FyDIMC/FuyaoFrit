#!/usr/bin/env python3
# -*- coding:utf-8 -*-
'''
# @Author: Xu Wang
# @Date: Friday, August 19th 2022
# @Email: wangxu.93@hotmail.com
# @Copyright (c) 2022 Institute of Trustworthy Network and System, Tsinghua University
'''
from Zone import Zone
class BandZone(Zone):
    def __init__(self):
        Zone.__init__(self)
        self.type = 'band'
        self.rows = list()
        self.curves = [None, None, None]
        self.is_flip = [False, False]
        self.relations = {}
    
    def add_relation(self):
        pass