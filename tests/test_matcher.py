from regexlib.matcher import Regex


def test_matcher():

    cases={
        "a":["a"],
        "ab":["ab"],
        "a|b":["a","b"],
        "a*":["","a","aaaa"],
        "a+":["a","aaa"],
        "a?":["","a"],
        "(a|b)*":["","ab","bbaa"]
    }

    for pattern,strings in cases.items():

        regex=Regex(pattern)

        for string in strings:

            assert regex.match(string)


def test_rejects_invalid_strings():

    cases={
        "a":["","b","aa"],
        "ab":["","a","abc","ba"],
        "a|b":["","ab","c"],
        "a*":["b","aab"],
        "a+":["","b","aab"],
        "a?":["aa","b"],
        "(a|b)*":["c","abc"]
    }

    for pattern,strings in cases.items():

        regex=Regex(pattern)

        for string in strings:

            assert not regex.match(string)


def test_fullmatch_not_search():

    regex=Regex("ab")

    assert regex.match("ab")
    assert not regex.match("abc")
    assert not regex.match("cab")


def test_empty_string():

    assert Regex("a*").match("")
    assert not Regex("a+").match("")


def test_redos_pattern():

    regex=Regex("(a+)+b")

    string="a"*30+"c"

    assert not regex.match(string)