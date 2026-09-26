from .nfa import epsilon_closure

class DFA:

    def __init__(self):

        self.states=set()
        self.start=None
        self.accepts=set()
        self.transitions={}


def move(nfa,states,char):

    destinations=set()

    for state in states:

        next_states=nfa.transitions.get((state,char),set())

        destinations.update(next_states)

    return destinations


def subset_construction(nfa):

    dfa=DFA()

    alphabet=set()

    for state,char in nfa.transitions:

        alphabet.add(char)

    start=epsilon_closure(nfa,{nfa.start})
    start=frozenset(start)

    dfa.start=start
    dfa.states.add(start)

    if start & nfa.accepts:

        dfa.accepts.add(start)

    worklist=[start]

    while worklist:

        current=worklist.pop()

        for char in alphabet:

            destinations=move(nfa,current,char)
            next_state=epsilon_closure(nfa,destinations)
            next_state=frozenset(next_state)

            if next_state not in dfa.states:

                dfa.states.add(next_state)

                if next_state & nfa.accepts:

                    dfa.accepts.add(next_state)

                worklist.append(next_state)

            dfa.transitions[(current,char)]=next_state

    return dfa