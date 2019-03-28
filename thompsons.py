# Thompsons Construction
# Mark Gilmore


# represents a state with two arrows, labelled by label
# use none for a label representing "e" arrows
class state:
    label = None
    edge1 = None
    edge2 = None

# an nfa is represented by its initial and accept states
class nfa:
    initial = None
    accept = None

    def __init__(self, initial, accept):
        self.initial = initial
        self.accept = accept

def compile(postfix):
    nfastack = []

    for c in postfix:
        if c == '.':
            # pop two nfa's off the stack
            nfa2 = nfastack.pop()
            nfa1 = nfastack.pop()

            # connect first nfa's accept state to the second's initial state
            nfa1.accept.edge1 = nfa2.initial

            # push nfa to the stack
            # nfastack.append(nfa1.initial, nfa2.accept)
            newnfa = nfa(nfa1.initial, nfa2.accept)
            nfastack.append(newnfa)

        elif c == '|':
            # pop two nfa's off the stack
            nfa2 = nfastack.pop()
            nfa1 = nfastack.pop()

            # create a new initial state, connect it to the initial states
            # of the two nfa's popped from the stack
            initial = state()
            initial.edge1 = nfa1.initial
            initial.edge2 = nfa2.initial

            # create a new accept state, connect it to the accept states
            # of the two nfa's popped from the stack, to the new state
            accept = state()
            nfa1.accept.edge1 = accept
            nfa2.accept.edge1 = accept

            # push the new nfa to the stack
            # nfastack.append(nfa(initial, accept))
            newnfa = nfa(initial, accept)
            nfastack.append(newnfa)

        elif c == '*':
            # pop a single nfa from the stack
            nfa1 = nfastack.pop()

            # create new initial and accept states
            accept = state()
            initial = state()

            # join the new initial state to nfa1's initial state to the new accept state
            initial.edge1 = nfa1.initial
            initial.edge2 = accept

            # join the old accept state to the new accept state and nfa1's initial state
            nfa1.accept.edge1 = nfa1.initial
            nfa2.accept.edge2 = accept

            # push the new nfa to the stack
            # nfastack.append(nfa(initial, accept))
            newnfa = nfa(initial, accept)
            nfastack.append(newnfa)

        else:
            # create new initial and accept states
            accept = state()
            initial = state()
        
            # join the initial state and the accept state using an arrow labelled c
            initial.label = c
            initial.edge1 = accept

            # push the new nfa to the stack
            # nfastack.append(nfa(initial, accept))
            newnfa = nfa(initial, accept)
            nfastack.append(newnfa)

    # nfastack should only have a single nfa at this point
    return nfastack.pop()

print(compile("ab.cd.|"))
print(compile("aa.*"))

