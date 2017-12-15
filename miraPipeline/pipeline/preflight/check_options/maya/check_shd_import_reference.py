# -*- coding: utf-8 -*-
from BaseCheck import BaseCheck
from miraLibs.mayaLibs import ReferenceUtility


class Check(BaseCheck):
    def run(self):
        ru = ReferenceUtility.ReferenceUtility()
        ru.import_loaded_ref()
        self.pass_check(u"reference已导入")
