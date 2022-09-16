import os

from .. import match_all_items, CONTAINER_KIND, FILE_KIND, CfaStat


class Folder:
    def __init__(self, path):
        assert os.path.isdir(path)
        self.path = os.path.normpath(os.path.abspath(path))
        self.dirnames = None
        self.filenames = None

    def __str__(self):
        return self.path

    def ls(self, filter=match_all_items):
        if self.dirnames is None:
            # Cache items in this folder so we don't go to disk more than once.
            for _, dirnames, filenames in os.walk(self.path, topdown=True, followlinks=False):
                self.dirnames = dirnames[:]
                self.filenames = filenames
                # Break after one folder (don't recurse).
                dirnames.clear()
        for d in self.dirnames:
            if filter(d, CONTAINER_KIND):
                yield d, CONTAINER_KIND
        for f in self.filenames:
            if filter(f, FILE_KIND):
                yield f, FILE_KIND

    def stat(self, name):
        path = os.path.join(self.path, name)
        try:
            # Don't follow symlinks, and only return regular files
            # and folders for now.
            info = os.lstat(path)
            mode = info.st_mode & (FILE_KIND | CONTAINER_KIND)
            if mode:
                return CfaStat(mode, info.st_size if mode == FILE_KIND else 0)
        except FileNotFoundError:
            pass


def open_container(path):
    return Folder(path)
