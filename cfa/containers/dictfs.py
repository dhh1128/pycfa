import os

from .. import match_all_items, CONTAINER_KIND, FILE_KIND, CfaStat


class Handle:
    def __init__(self, obj):
        assert isinstance(obj, dict)
        self.obj = obj

    def ls(self, filter=match_all_items):
        for key, value in self.obj.items():
            if key.endswith('/'):
                if filter(key, CONTAINER_KIND):
                    yield key, CONTAINER_KIND
            elif filter(key, FILE_KIND):
                yield key, FILE_KIND

    def stat(self, name):
        if name in self.obj:
            is_container = name.endswith('/')
            if is_container:
                return CfaStat(CONTAINER_KIND, 0)
            else:
                return CfaStat(FILE_KIND, len(self.obj[name]))


def open_container(obj):
    return Handle(obj)
