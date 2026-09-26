from regexlib.parser import parse
from regexlib.ast_nodes import Literal, Concat, Union, Star, Plus, Question


def test_empty_pattern():

    try:

        parse("")
        assert False

    except ValueError:

        pass


def test_literal():

    assert parse("a") == Literal("a")


def test_concat():

    assert parse("ab") == Concat(Literal("a"),Literal("b"))


def test_union():

    assert parse("a|b") == Union(Literal("a"),Literal("b"))


def test_star():

    assert parse("a*") == Star(Literal("a"))


def test_plus():
    
    assert parse("a+") == Plus(Literal("a"))


def test_question():

    assert parse("a?") == Question(Literal("a"))


def test_group():

    assert parse("(ab)") == Concat(Literal("a"),Literal("b"))


def test_nested_group():

    expected=Star(Union(Literal("a"),Literal("b")))

    assert parse("(a|b)*") == expected


def test_union_left_associative():

    expected=Union(Union(Literal("a"),Literal("b")),Literal("c"))

    assert parse("a|b|c") == expected


def test_missing_closing_parenthesis():

    try:

        parse("(ab")
        assert False

    except ValueError:

        pass


def test_empty_group():

    try:

        parse("()")
        assert False

    except ValueError:

        pass