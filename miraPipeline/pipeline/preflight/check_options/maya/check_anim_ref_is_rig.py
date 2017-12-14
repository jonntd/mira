# -*- coding: utf-8 -*-
import maya.cmds as mc
from BaseCheck import BaseCheck
from miraLibs.pipeLibs import pipeFile


class Check(BaseCheck):
    def run(self):
        self.error_list = self.get_error_list()
        if self.error_list:
            self.fail_check(u"reference的文件中，有的不是绑定文件。")
        else:
            self.pass_check(u"所有的reference文件均是绑定文件。")

    def get_error_list(self):
        error_list = list()
        ref_files = mc.file(q=1, r=1)
        if not ref_files:
            return
        for ref_file in ref_files:
            context = pipeFile.PathDetails.parse_path(ref_file)
            if context:
                if context.step not in ["MidRig", "HighRig"]:
                    error_list.append(ref_file)
        return error_list
