import os
from subprocess import call

class FileMgr(object):
    def __init__(self):
        self.dir = "."
        self.target_dir = "./output"
        self.passwd = "Test"

    def _getFileNames(self, dir):
        return os.listdir(dir)

    def compressAll(self, dir="", target_dir="", passwd=""):
        """
        compress all files and directories
        :return: void
        """
        if not dir:
            dir = self.dir
        if not target_dir:
            target_dir = self.target_dir
        if not passwd:
            passwd = self.passwd

        target_dir = os.path.abspath(target_dir)
        if not os.path.exists(target_dir):
            os.makedirs(target_dir)
        file_names = self._getFileNames(dir)
        file_names = filter(lambda x: not x.startswith('.'), file_names)
        for file in file_names:
            if os.path.isfile(file) and os.stat(file).st_size < 10000000:
                continue
            archive_name = file.split('.')[0] + ".archive"
            print "Compressing {} as {}...".format(file, archive_name)
            call(["7z", "a", archive_name, file, "-p" + passwd])
            print "Moving zipped file {} to folder {}".format(archive_name, target_dir)
            call(["mv", archive_name, target_dir])

    def decompressAll(self, dir="", target_dir="", passwd=""):
        if not dir:
            dir = self.dir
        if not target_dir:
            target_dir = self.target_dir
        if not passwd:
            passwd = self.passwd

        target_dir = os.path.abspath(target_dir)
        if not os.path.exists(target_dir):
            os.makedirs(target_dir)
        file_names = self._getFileNames(dir)
        file_names = filter(lambda x: x.endswith('.archive'), file_names)
        for file in file_names:
            print "De-compressing {} ...".format(file)
            call(["7z", "x", file, "-p" + passwd])
            print "Removing zipped file {}".format(file)
            call(["rm", "-rf", file])

    def flatAll(self, dir="", target_dir=""):
        """
        Flat all files to parent dir
        :param dir:
        :return: void
        """
        if not dir:
            dir = self.dir
        if not target_dir:
            target_dir = self.target_dir

        target_dir = os.path.abspath(target_dir)
        self._flatAll(dir, target_dir)


    def _flatAll(self, dir, target_dir):
        file_names = self._getFileNames(dir)
        for file in file_names:
            if os.path.isfile(file):
                if os.stat(file).st_size >= 10000000: # >= 10M
                    print "Moving {} to {}...".format(file, target_dir)
                    call(["mv", file, target_dir])
            if os.path.isdir(file):
                print "Jumping to sub dir {}...".format(file)
                self._flatAll(dir+file, target_dir)

