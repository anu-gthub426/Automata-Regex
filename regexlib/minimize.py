class MinimizedDFA:

    def __init__(self):
        
        self.states=set()
        self.start=None
        self.accepts=set()
        self.transitions={}


def hopcroft_minimize(dfa,alphabet):

    accepting=set(dfa.accepts)
    non_accepting=dfa.states-accepting

    groups=[]

    if accepting:

        groups.append(accepting)

    if non_accepting:

        groups.append(non_accepting)


    if len(groups)==1:

        worklist=[frozenset(groups[0])]

    else:

        smaller=min(groups,key=len)

        worklist=[frozenset(smaller)]


    predecessors={}

    for char in alphabet:

        predecessors[char]={}

        for state in dfa.states:

            destination=dfa.transitions.get((state,char))

            if destination is not None:

                if destination not in predecessors[char]:

                    predecessors[char][destination]=set()

                predecessors[char][destination].add(state)


    while worklist:

        splitter=worklist.pop()

        for char in alphabet:

            affected=set()

            for state in splitter:

                affected.update(predecessors[char].get(state,set()))

            if not affected:

                continue

            new_groups=[]

            for group in groups:

                intersection=group & affected
                difference=group-affected

                if not intersection or not difference:

                    new_groups.append(group)
                    continue


                new_groups.append(intersection)
                new_groups.append(difference)


                group_frozen=frozenset(group)

                if group_frozen in worklist:

                    worklist.remove(group_frozen)

                    worklist.append(frozenset(intersection))
                    worklist.append(frozenset(difference))

                else:

                    if len(intersection)<=len(difference):

                        worklist.append(frozenset(intersection))

                    else:

                        worklist.append(frozenset(difference))


            groups=new_groups


    minimized=MinimizedDFA()

    minimized.states={frozenset(group) for group in groups}


    group_of={}

    for group in minimized.states:

        for state in group:

            group_of[state]=group


    minimized.start=group_of[dfa.start]


    for group in minimized.states:

        if group & dfa.accepts:

            minimized.accepts.add(group)


    for group in minimized.states:

        representative=next(iter(group))

        for char in alphabet:

            destination=dfa.transitions.get((representative,char))

            if destination is not None:

                target_group=group_of[destination]

                minimized.transitions[(group,char)]=target_group


    return minimized