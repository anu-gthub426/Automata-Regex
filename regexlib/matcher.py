from .parser import parse
from .nfa import compile_to_nfa
from .dfa import subset_construction
from .minimize import hopcroft_minimize


class Regex:

    def __init__(self,pattern):

        self.pattern=pattern

        ast=parse(pattern)

        nfa=compile_to_nfa(ast)

        alphabet=set()

        for state,char in nfa.transitions:

            alphabet.add(char)

        dfa=subset_construction(nfa)

        self.dfa=hopcroft_minimize(dfa,alphabet)


    def match(self,string):

        current=self.dfa.start

        for char in string:

            current=self.dfa.transitions.get((current,char))

            if current is None:

                return False

        return current in self.dfa.accepts