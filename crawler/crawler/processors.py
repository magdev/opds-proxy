# -*- coding: utf-8 -*- 
import ast

class List(object):

    def __call__(self, values):
        v = []
        for value in values:
            v.append(ast.literal_eval(value))
        return v