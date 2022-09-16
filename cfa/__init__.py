from collections import namedtuple
from stat import S_IFDIR, S_IFREG

FILE_KIND = S_IFREG
CONTAINER_KIND = S_IFDIR

CfaStat = namedtuple('CfaStat', ['kind', 'size'])


def match_all_items(name, kind):
    return True
