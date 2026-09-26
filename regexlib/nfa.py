from dataclasses import dataclass
from .ast_nodes import Literal, Concat, Union, Star, Plus, Question


@dataclass

class NFAFragment:

    start: int
    accept: int


class NFA:

    def __init__(self):

        self.states=set()
        self.start=None
        self.accepts=set()
        self.transitions={}
        self.epsilon={}
        self.next_state=0

    def new_state(self):

        state=self.next_state
        self.next_state+=1
        self.states.add(state)
        return state

    def add_transition(self,start,char,end):

        key=(start,char)

        if key not in self.transitions:

            self.transitions[key]=set()

        self.transitions[key].add(end)

    def add_epsilon(self,start,end):

        if start not in self.epsilon:

            self.epsilon[start]=set()

        self.epsilon[start].add(end)


def build(node,nfa):

    if isinstance(node,Literal):

        start=nfa.new_state()
        accept=nfa.new_state()

        nfa.add_transition(start,node.value,accept)

        return NFAFragment(start,accept)


    if isinstance(node,Concat):

        left=build(node.left,nfa)
        right=build(node.right,nfa)

        nfa.add_epsilon(left.accept,right.start)

        return NFAFragment(left.start,right.accept)


    if isinstance(node,Union):

        left=build(node.left,nfa)
        right=build(node.right,nfa)

        start=nfa.new_state()
        accept=nfa.new_state()

        nfa.add_epsilon(start,left.start)
        nfa.add_epsilon(start,right.start)

        nfa.add_epsilon(left.accept,accept)
        nfa.add_epsilon(right.accept,accept)

        return NFAFragment(start,accept)


    if isinstance(node,Star):

        fragment=build(node.child,nfa)

        start=nfa.new_state()
        accept=nfa.new_state()

        nfa.add_epsilon(start,fragment.start)
        nfa.add_epsilon(start,accept)

        nfa.add_epsilon(fragment.accept,fragment.start)
        nfa.add_epsilon(fragment.accept,accept)

        return NFAFragment(start,accept)


    if isinstance(node,Plus):

        fragment=build(node.child,nfa)

        start=nfa.new_state()
        accept=nfa.new_state()

        nfa.add_epsilon(start,fragment.start)

        nfa.add_epsilon(fragment.accept,fragment.start)
        nfa.add_epsilon(fragment.accept,accept)

        return NFAFragment(start,accept)


    if isinstance(node,Question):

        fragment=build(node.child,nfa)

        start=nfa.new_state()
        accept=nfa.new_state()

        nfa.add_epsilon(start,fragment.start)
        nfa.add_epsilon(start,accept)

        nfa.add_epsilon(fragment.accept,accept)

        return NFAFragment(start,accept)

    raise TypeError("Unknown AST node")

def compile_to_nfa(ast):

    nfa=NFA()

    fragment=build(ast,nfa)

    nfa.start=fragment.start
    nfa.accepts={fragment.accept}

    return nfa

def epsilon_closure(nfa,states):

    closure=set(states)
    stack=list(states)

    while stack:

        state=stack.pop()

        for next_state in nfa.epsilon.get(state,set()):

            if next_state not in closure:

                closure.add(next_state)
                stack.append(next_state)

    return closure

def simulate(nfa,string):

    current=epsilon_closure(nfa,{nfa.start})

    for char in string:

        next_states=set()

        for state in current:

            destinations=nfa.transitions.get((state,char),set())

            next_states.update(destinations)

        current=epsilon_closure(nfa,next_states)

    return bool(current & nfa.accepts)