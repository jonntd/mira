# -*- coding: utf-8 -*-
import subprocess
import sys


def run_maya_command(maya_path, file_path, maya_command):
    """
    :param maya_path: mayabatch path
    :param file_path: maya file name
    :param maya_command: maya script
    :return:
    """
    maya_path = maya_path.replace("\\", "/")
    file_path = file_path.replace("\\", "/")
    cmd = "\"%s\" -file \"%s\" -command \"python(\\\"%s\\\")\"" % (maya_path, file_path, maya_command)
    print cmd
    p = subprocess.Popen(cmd, shell=True, stderr=subprocess.STDOUT, stdout=subprocess.PIPE)
    while p.poll() is None:
        for line in p.stdout.readlines():
            if line.strip():
                print line
        break


def main():
    print sys.argv
    if len(sys.argv) != 4:
        raise RuntimeError("Arguments wrong")
    maya_path = sys.argv[1]
    file_path = sys.argv[2]
    maya_command = sys.argv[3]
    run_maya_command(maya_path, file_path, maya_command)


if __name__ == "__main__":
    main()
