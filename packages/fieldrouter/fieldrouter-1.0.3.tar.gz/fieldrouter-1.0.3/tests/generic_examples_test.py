from pytest import importorskip


def test_simple():
    importorskip("examples.generic.simple")


def test_nested():
    importorskip("examples.generic.nested")


def test_reference():
    importorskip("examples.generic.reference")


def test_identity():
    importorskip("examples.generic.identity")
