# -*- coding: utf-8 -*-
"""
Created on Sept. 2016
@author: nathalie
"""

class BinTree:
    def __init__(self, key, left, right):
        """
        Init Tree
        """
        self.key = key
        self.left = left
        self.right = right

    def tostr(self):
        l, r, t = [], [], []
        middle_left, middle_right = 0, 0
        key = str(self.key)
        len_key = len(key)
        middle = len_key // 2
        len_left, len_right = 0, 0
        if self.left != None:
            l, middle_left = self.left.tostr()
            key = "_" + key
            len_key += 1
            len_left = len(l[0])
            middle += len_left + 1
        if self.right != None:
            r, middle_right = self.right.tostr()
            key += "_"
            len_key += 1
            len_right = len(r[0])
        if l == [] and r == []:
            return [key], len_key //2
        t.append( (" " * (middle_left + 1) + "_" * (len_left - middle_left - 1) if l else "") 
                  + key 
                  + ("_" * (middle_right) + " " * (len_right - middle_right) if r else "")
                )
        t.append( (" " * middle_left + "/" + " " * (len_left - middle_left - 1) if l else "") 
                  + " " * len_key 
                  + (" " * middle_right + "\\" + " " * (len_right - middle_right - 1) if r else "")
                )
        ll, lr = len(l), len(r)
        t = t + [   ((l[i] if i < ll else " " * len_left) 
                     + " " * len_key
                     + (r[i] if i < lr else " " * len_right) )
                     for i in range(max(ll, lr))
                ]
        return t, middle
                
    def __str__(self):
        return "".join(e + "\n" for e in self.tostr()[0])
