from ..containers.dictfs import open_container
from .. import CONTAINER_KIND, FILE_KIND

simple_dict = {
    "a": b"hello",
    "b": b"this is a longer string",
    "subdir/": None
}


def test_ls_works():
    container = open_container(simple_dict)
    items = [x for x in container.ls()]
    names = sorted([x[0] for x in items])
    assert names == ["a", "b", "subdir/"]
    kinds = sorted([x[1] for x in items], reverse=True)
    assert kinds == [FILE_KIND, FILE_KIND, CONTAINER_KIND]


def test_stat_works():
    container = open_container(simple_dict)
    assert container.stat("doesnt_exist") is None
    assert container.stat("a").kind == FILE_KIND
    assert container.stat("a").size == 5
    assert container.stat("b").kind == FILE_KIND
    assert container.stat("b").size == 23
    assert container.stat("subdir/").kind == CONTAINER_KIND
    assert container.stat("subdir/").size == 0


def test_filter_works():
    container = open_container(simple_dict)
    assert sum(1 for _ in container.ls(lambda name, kind: len(name) == 1)) == 2
    assert sum(1 for _ in container.ls(lambda name, kind: kind == CONTAINER_KIND)) == 1
    assert sum(1 for _ in container.ls(lambda name, kind: len(name) == 1 and kind == CONTAINER_KIND)) == 0
