# -*- coding: utf-8 -*-
from Maya import Maya


def main(asset_dir):
    maya = Maya(asset_dir)
    maya.launch_folder()
