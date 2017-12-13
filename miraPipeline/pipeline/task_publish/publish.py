# -*- coding: utf-8 -*-
import os
import sys
sys.path.insert(0, "Z:/mira")
from miraLibs.pipeLibs.get_task_name import get_task_name
import pipeGlobal
from miraLibs.pyLibs import join_path
from miraLibs.pipeLibs import Project, pipeFile, get_logger
from miraLibs.dbLibs import db_api
from miraLibs.pipeLibs.pipeDb import task_from_db_path


class Publish(object):
    def __init__(self, work_file=None, change_task_status=True):
        self.work_file = work_file
        self.change_task_status = change_task_status
        self.context = pipeFile.PathDetails.parse_path(self.work_file)
        self.logger = self.get_logger()
        self.engine = self.context.engine
        self.project = self.context.project

    def get_publish_py(self):
        custom_dir = pipeGlobal.custom_dir
        publish_dir = join_path.join_path2(custom_dir, self.project, "publish")
        if not os.path.isdir(publish_dir):
            publish_dir = join_path.join_path2(custom_dir, "defaultProject", "publish")
        publish_py = join_path.join_path2(publish_dir, "publish.py")
        return publish_py

    def get_logger(self):
        task_name = get_task_name(self.context)
        logger = get_logger.get_logger(self.context.project, "publish", task_name)
        return logger

    def run_command(self, cmd):
        self.logger.info("cmd:\n\n%s\n\n" % cmd)
        return_file = os.popen(cmd)
        self.logger.info(return_file.read())
        return_file.close()

    def maya_publish(self):
        # publish mayabatch cmd to deadline
        publish_py = self.get_publish_py()
        if not os.path.isfile(publish_py):
            self.logger.error("%s is not an exist file" % publish_py)
            return
        mayabatch = Project(self.context.project).mayabatch_path
        cmd = '\"\"%s\" -command \"python \"\"file_name=\'%s\';execfile(\'%s\')\"\"\"\"' % (
            mayabatch, self.work_file, publish_py)
        self.run_command(cmd)
        self.post_publish()

    def nuke_publish(self):
        custom_dir = pipeGlobal.custom_dir
        publish_dir = join_path.join_path2(custom_dir, self.project, "publish")
        if not os.path.isdir(publish_dir):
            publish_dir = join_path.join_path2(custom_dir, "defaultProject", "publish")
        publish_py = join_path.join_path2(publish_dir, "%s.py" % self.context.step)
        if not os.path.isfile(publish_py):
            self.logger.error("%s is not an exist file" % publish_py)
            return
        nuke_path = Project(self.context.project).nuke_path
        cmd = "%s -t %s %s" % (nuke_path, publish_py, self.work_file)
        self.run_command(cmd)
        self.post_publish()

    def houdini_publish(self):
        # todo
        pass

    def post_publish(self):
        if not os.path.isfile(self.context.publish_path):
            self.logger.error("Something wrong with publish")
            return
        # set task sg_publishfile
        self.logger.info("start post publish...")
        db = db_api.DbApi(self.project).db_obj
        current_task = task_from_db_path.task_from_db_path(db, self.work_file)
        self.logger.info("Current Task: %s" % current_task)
        db.update_file_path(current_task, publish_file_path=self.context.publish_path)
        self.logger.info("update task sg_publishfile: %s" % self.context.publish_path)
        # change task status
        if self.change_task_status:
            db.update_task_status(current_task, "Delivered")
            self.logger.info("update task status: Delivered")
        # # for shotgun register publish file
        # self.logger.info("publish path: %s" % self.context.publish_path)
        # try:
        #     tk = toolkit.Toolkit(self.project).tk_obj
        #     self.logger.info("%s" % repr(tk.get_context_from_path(self.context.publish_path)))
        #     tk.publish_file(self.context.publish_path)
        # except RuntimeError as e:
        #     self.logger.error(str(e))
        self.logger.info("All Done.")

    def main(self):
        if self.engine == "maya":
            self.maya_publish()
        elif self.engine == "nuke":
            self.nuke_publish()
        elif self.engine == "houdini":
            self.houdini_publish()


def main():
    work_file = sys.argv[1]
    if len(sys.argv) == 3:
        change_task = sys.argv[2]
        p = Publish(work_file, change_task)
        p.main()
    elif len(sys.argv) == 2:
        print "yes"
        p = Publish(work_file)
        p.main()


if __name__ == "__main__":
    main()



