# -*- coding: utf-8 -*-
import pymel.core as pm
from BaseCheck import BaseCheck


class Check(BaseCheck):
    def run(self):
        self.error_list = self.get_error_list()
        if self.error_list:
            self.fail_check(u"有隐藏的模型存在")
        else:
            self.pass_check(u"没有隐藏的模型存在")

    @staticmethod
    def get_error_list():
        error_list = [i.parent(0).name() for i in pm.ls(type="mesh") if not i.isVisible()]
        return error_list
