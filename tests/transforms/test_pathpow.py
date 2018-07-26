from functools import partial
import pytest

from pysh.transforms import pathpow
from pysh.dsl.path import Path, RecursiveMatcher

from .utils import factory

lex, parse, comp, auto = factory(pathpow)


def test_rglob():
    assert lex('_ ** g') == '_ **__PYSH_POW__** g'


def test_rglob_dsl():
    expr = auto("_ ** 'foo'")

    assert type(expr) == RecursiveMatcher
    assert expr.matcher == 'foo'

@pytest.mark.skip('chaining matchers not yet supported')
def test_rglob_precendence():
    expr = auto("_ / 'foo' ** '*.jpg'")
    assert type(expr) == RecursiveMatcher
    assert expr.path == 'foo'

    expr = auto("_'/tmp' / 'foo' ** '*.jpg'")
    assert type(expr) == RecursiveMatcher
    assert expr.path == 'foo'

@pytest.mark.skip('chaining matchers not yet supported')
def test_rglob_callable():
    expr = auto("_ / str.isalpha ** '*.jpg'")

    assert type(expr) == RecursiveMatcher
    assert expr.path == str.isalpha


@pytest.mark.parametrize("expression", [
    ('2**3'),
    ('2**-3'),
    ('2**3**4'),
    ('2**2 / 2**2'),
    ('2**2+3'),
    ('2**2*3'),
    ('2*3**4'),
])
def test_arithmetic(expression):
    assert auto(expression) == eval(expression)
