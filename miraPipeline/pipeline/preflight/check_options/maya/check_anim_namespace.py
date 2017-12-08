# -*- coding: utf-8 -*-
import maya.cmds as mc
from BaseCheck import BaseCheck
from miraLibs.mayaLibs import get_namespace


class Check(BaseCheck):
    def run(self):
        self.error_list = self.get_error_list()
        if self.error_list:
            self.fail_check(u"namespace与资产名不符。")
        else:
            self.pass_check(u"namespace与资产名相符。")

    def get_top_groups(self):
        top_groups = list()
        ref_files = mc.file(q=1, r=1)
        if not ref_files:
            return
        for ref in ref_files:
            ref_node = mc.referenceQuery(ref, referenceNode=1)
            dag_nodes = mc.referenceQuery(ref_node, dp=1, nodes=1)
            if not dag_nodes:
                continue
            top_group = dag_nodes[0]
            top_groups.append(top_group)
        return top_groups

    def get_error_list(self):
        top_groups = self.get_top_groups()
        if not top_groups:
            return
        error_list = list()
        for grp in top_groups:
            suffix = grp.split(":")[-1]
            asset_name = suffix.split("_")[1]
            namespace = get_namespace.get_namespace(grp)
            if not namespace.startswith(asset_name):
                error_list.append(grp)
        return error_list
