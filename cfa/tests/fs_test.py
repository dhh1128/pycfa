import os
from ..containers.fs import open_container
from .. import CONTAINER_KIND, FILE_KIND

MY_FOLDER = os.path.dirname(os.path.abspath(__file__))
MY_PARENT = os.path.join(MY_FOLDER, '..')


def ignore_pytest_and_cache(name, kind):
    return name != '__pycache__' and name != '.pytest_cache'


def test_ls_works():
    container = open_container(MY_FOLDER)
    items = [x for x in container.ls(ignore_pytest_and_cache)]
    names = [x[0] for x in items]
    for expected in ['__init__.py', 'dictfs_test.py', 'fs_test.py']:
        assert expected in names
    assert '.' not in names
    assert '..' not in names
    kinds = [x[1] for x in items]
    assert FILE_KIND in kinds
    assert CONTAINER_KIND not in kinds
    container = open_container(MY_PARENT)
    kinds = [x[1] for x in container.ls()]
    assert CONTAINER_KIND in kinds


def test_stat_works():
    container = open_container(MY_FOLDER)
    assert container.stat("doesnt_exist") is None
    info = container.stat("fs_test.py")
    assert info.kind == FILE_KIND
    assert info.size > 1000
    assert info.size < 10000 # adjust if the size of this file exceeds 10 KiB
    container = open_container(MY_PARENT)
    assert container.stat("tests").kind == CONTAINER_KIND
    assert container.stat("tests").size == 0


def test_filter_works():
    container = open_container(MY_FOLDER)
    count_fs_tests = sum(1 for _ in container.ls(lambda name, kind: name.startswith('fs_test.')))
    count_tests = sum(1 for _ in container.ls(lambda name, kind: "_test" in name and name.endswith('.py') and kind == FILE_KIND))
    count_py = sum(1 for _ in container.ls(lambda name, kind: name.endswith('.py') and kind == FILE_KIND))
    assert count_fs_tests == 1
    assert count_tests > count_fs_tests
    assert count_py > count_tests
    assert sum(1 for _ in container.ls(lambda name, kind: ignore_pytest_and_cache(name, kind) and kind == CONTAINER_KIND)) == 0
