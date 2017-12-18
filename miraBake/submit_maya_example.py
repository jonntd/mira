# -*- coding: utf-8 -*-
import os
from miraLibs.deadlineLibs import submit_python


file_name = "W:/SnowKidTest/publish/shots/s996/c030A/Anim/Anim/_publish/maya/SnowKidTest_s996_c030A_Anim_Anim.ma"

white_list = "heshuai,pipemanager"


submit_python.submit_python(r"Z:\mira\miraLibs\dccLibs\run_maya_command.py",

                            "\"C:/Program Files/Autodesk/Maya2017/bin/mayabatch.exe\" "
                            "\"%s\" "
                            "\"from miraLibs.pipeLibs.pipeMaya.lgt import only_export_anim_env;only_export_anim_env.main()\"" % file_name,

                            white_list, os.path.basename(file_name))
