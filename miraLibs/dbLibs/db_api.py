# -*- coding: utf-8 -*-
from miraLibs.pipeLibs import pipeMira


class DbApi(object):
    def __init__(self, project=None):
        self.project = project
        self.db_obj = self.get_db()

    def get_db(self):
        """
        get the database instance
        :return: database instance
        """
        database = pipeMira.get_site_value(self.project, "database")
        if database == "shotgun":
            from miraLibs.sgLibs import Sg
            db = Sg.Sg(self.project)
        elif database == "strack":
            from miraLibs.stLibs import St
            db = St.St(self.project)
        else:
            from miraLibs.stLibs import St
            db = St.St(self.project)
        return db
