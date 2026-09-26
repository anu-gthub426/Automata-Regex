from regexlib.parser import parse
from regexlib.nfa import compile_to_nfa,simulate
from regexlib.dfa import subset_construction


def run_dfa(dfa,string):

    current=dfa.start

    for char in string:

        current=dfa.transitions.get((current,char),frozenset())

    return current in dfa.accepts


def test_dfa_matches_nfa():

    cases={
        "a":["a","","aa"],
        "ab":["ab","a","b","ba","ac"],
        "a|b":["a","b","ab",""],
        "a*":["","a","aaaa","b","aab"],
        "a+":["a","aaa","","b"],
        "a?":["","a","aa","b"],
        "(a|b)*":["","ab","bbaa","c","abc"]
    }

    for pattern,strings in cases.items():

        nfa=compile_to_nfa(parse(pattern))
        dfa=subset_construction(nfa)

        for string in strings:

            nfa_result=simulate(nfa,string)
            dfa_result=run_dfa(dfa,string)

            assert dfa_result==nfa_result