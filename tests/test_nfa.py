from regexlib.parser import parse
from regexlib.nfa import compile_to_nfa,simulate


def test_literal():

    nfa=compile_to_nfa(parse("a"))

    assert simulate(nfa,"a")
    assert not simulate(nfa,"")
    assert not simulate(nfa,"aa")


def test_concat():

    nfa=compile_to_nfa(parse("ab"))

    assert simulate(nfa,"ab")
    assert not simulate(nfa,"a")
    assert not simulate(nfa,"b")
    assert not simulate(nfa,"ba")


def test_union():

    nfa=compile_to_nfa(parse("a|b"))

    assert simulate(nfa,"a")
    assert simulate(nfa,"b")
    assert not simulate(nfa,"ab")
    assert not simulate(nfa,"")


def test_star():

    nfa=compile_to_nfa(parse("a*"))

    assert simulate(nfa,"")
    assert simulate(nfa,"a")
    assert simulate(nfa,"aaaa")
    assert not simulate(nfa,"b")
    assert not simulate(nfa,"aab")


def test_plus():

    nfa=compile_to_nfa(parse("a+"))

    assert simulate(nfa,"a")
    assert simulate(nfa,"aaa")
    assert not simulate(nfa,"")


def test_question():

    nfa=compile_to_nfa(parse("a?"))

    assert simulate(nfa,"")
    assert simulate(nfa,"a")
    assert not simulate(nfa,"aa")


def test_group_star():

    nfa=compile_to_nfa(parse("(a|b)*"))

    assert simulate(nfa,"")
    assert simulate(nfa,"ab")
    assert simulate(nfa,"bbaa")
    assert not simulate(nfa,"c")
    assert not simulate(nfa,"abc")