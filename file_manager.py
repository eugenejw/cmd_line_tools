import os
from subprocess import call

class FileMgr(object):
    def __init__(self):
        self.folder = "."
        self.target_folder = "./output"
        self.passwd = "Test"

    def _getFileNames(self, folder):
        return os.listfolder(folder)

    def compressAll(self, folder="", target_folder="", passwd=""):
        """
        compress all files and folderectories
        :return: void
        """
        if not folder:
            folder = self.folder
        if not target_folder:
            target_folder = self.target_folder
        if not passwd:
            passwd = self.passwd

        target_folder = os.path.abspath(target_folder)
        if not os.path.exists(target_folder):
            os.makefolders(target_folder)
        file_names = self._getFileNames(folder)
        file_names = filter(lambda x: not x.startswith('.'), file_names)
        for file in file_names:
            if os.path.isfile(file) and os.stat(file).st_size < 10000000:
                continue
            archive_name = file.split('.')[0] + ".archive"
            print "Compressing {} as {}...".format(file, archive_name)
            call(["7z", "a", archive_name, file, "-p" + passwd])
            print "Moving zipped file {} to folder {}".format(archive_name, target_folder)
            call(["mv", archive_name, target_folder])

    def decompressAll(self, folder="", target_folder="", passwd=""):
        if not folder:
            folder = self.folder
        if not target_folder:
            target_folder = self.target_folder
        if not passwd:
            passwd = self.passwd

        target_folder = os.path.abspath(target_folder)
        if not os.path.exists(target_folder):
            os.makefolders(target_folder)
        file_names = self._getFileNames(folder)
        file_names = filter(lambda x: x.endswith('.archive'), file_names)
        for file in file_names:
            print "De-compressing {} ...".format(file)
            call(["7z", "x", file, "-p" + passwd])
            print "Removing zipped file {}".format(file)
            call(["rm", "-rf", file])

    def flatAll(self, folder="", target_folder=""):
        """
        Flat all files to parent folder
        :param folder:
        :return: void
        """
        if not folder:
            folder = self.folder
        if not target_folder:
            target_folder = self.target_folder

        target_folder = os.path.abspath(target_folder)
        self._flatAll(folder, target_folder)


    def _flatAll(self, folder, target_folder):
        file_names = self._getFileNames(folder)
        for file in file_names:
            if os.path.isfile(file):
                if os.stat(file).st_size >= 10000000: # >= 10M
                    print "Moving {} to {}...".format(file, target_folder)
                    call(["mv", file, target_folder])
            if os.path.isfolder(file):
                print "Jumping to sub folder {}...".format(file)
                self._flatAll(folder+file, target_folder)

