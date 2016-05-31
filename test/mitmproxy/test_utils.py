import json
from mitmproxy import utils
from . import tutils

utils.CERT_SLEEP_TIME = 0


def test_format_timestamp():
    assert utils.format_timestamp(utils.timestamp())


def test_format_timestamp_with_milli():
    assert utils.format_timestamp_with_milli(utils.timestamp())


def test_isBin():
    assert not utils.isBin("testing\n\r")
    assert utils.isBin("testing\x01")
    assert utils.isBin("testing\x0e")
    assert utils.isBin("testing\x7f")


def test_isXml():
    assert not utils.isXML("foo")
    assert utils.isXML("<foo")
    assert utils.isXML("  \n<foo")


def test_clean_hanging_newline():
    s = "foo\n"
    assert utils.clean_hanging_newline(s) == "foo"
    assert utils.clean_hanging_newline("foo") == "foo"


def test_pkg_data():
    assert utils.pkg_data.path("console")
    tutils.raises("does not exist", utils.pkg_data.path, "nonexistent")


def test_pretty_json():
    s = json.dumps({"foo": 1})
    assert utils.pretty_json(s)
    assert not utils.pretty_json("moo")


def test_LRUCache():
    cache = utils.LRUCache(2)

    class Foo:
        ran = False

        def gen(self, x):
            self.ran = True
            return x
    f = Foo()

    assert not f.ran
    assert cache.get(f.gen, 1) == 1
    assert f.ran
    f.ran = False
    assert cache.get(f.gen, 1) == 1
    assert not f.ran

    f.ran = False
    assert cache.get(f.gen, 1) == 1
    assert not f.ran
    assert cache.get(f.gen, 2) == 2
    assert cache.get(f.gen, 3) == 3
    assert f.ran

    f.ran = False
    assert cache.get(f.gen, 1) == 1
    assert f.ran

    assert len(cache.cacheList) == 2
    assert len(cache.cache) == 2
