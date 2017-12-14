# -*- coding: utf-8 -*-
import maya.cmds as mc
from BaseCheck import BaseCheck


class Check(BaseCheck):
    def run(self):
        self.error_list = self.get_error_list()
        if self.error_list:
            self.fail_check(u"这些资产分组不正确。")
        else:
            self.pass_check(u"资产分组正确。")

    def get_error_list(self):
        error_list = list()
        if mc.objExists("Char"):
            char_assets = self.get_assets("Char")
            if char_assets:
                char_error_list = [asset for asset in char_assets if not asset.split(":")[-1].split("_")[0] in ["char"]]
                error_list.extend(char_error_list)
        if mc.objExists("Prop"):
            prop_assets = self.get_assets("Prop")
            if prop_assets:
                char_error_list = [asset for asset in prop_assets
                                   if not asset.split(":")[-1].split("_")[0] in ["prop", "cprop"]]
                error_list.extend(char_error_list)
        return error_list

    def get_assets(self, asset_type):
        transforms = mc.listRelatives(asset_type, ad=1, type="transform")
        if transforms:
            assets = [transform for transform in transforms if transform.endswith("_ROOT")]
            return assets
