from regexlib.parser import parse
from regexlib.nfa import compile_to_nfa,simulate
from regexlib.dfa import subset_construction
from regexlib.minimize import hopcroft_minimize


def run_dfa(dfa,string):

    current=dfa.start

    for char in string:

        current=dfa.transitions.get((current,char),frozenset())

    return current in dfa.accepts


def run_minimized(mdfa,string):

    current=mdfa.start

    for char in string:

        current=mdfa.transitions.get((current,char),frozenset())

    return current in mdfa.accepts


def test_minimized_matches_dfa():

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

        alphabet=set()

        for state,char in nfa.transitions:

            alphabet.add(char)

        mdfa=hopcroft_minimize(dfa,alphabet)

        for string in strings:

            nfa_result=simulate(nfa,string)
            dfa_result=run_dfa(dfa,string)
            minimized_result=run_minimized(mdfa,string)

            assert minimized_result==dfa_result==nfa_result


def test_minimization_does_not_increase_states():

    pattern="(a|a)"

    nfa=compile_to_nfa(parse(pattern))
    dfa=subset_construction(nfa)

    alphabet=set()

    for state,char in nfa.transitions:

        alphabet.add(char)

    mdfa=hopcroft_minimize(dfa,alphabet)

    assert len(mdfa.states)<=len(dfa.states)


def test_all_accepting_states_can_merge():

    nfa=compile_to_nfa(parse("a*"))
    dfa=subset_construction(nfa)

    alphabet={"a"}

    mdfa=hopcroft_minimize(dfa,alphabet)

    assert len(dfa.states)==2
    assert len(dfa.accepts)==2
    assert len(mdfa.states)==1
    assert len(mdfa.accepts)==1