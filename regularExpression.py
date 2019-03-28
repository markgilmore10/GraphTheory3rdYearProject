# Shunting Yard Algorithm
# Mark Gilmore
# http://www.oxfordmathcenter.com/drupal7/node/628

def shunt(infix):

    specials = { '*': 50, '.': 40, '|': 30 }

    postfix = ""
    stack = ""

    for c in infix:
        if c == '(':
            stack = stack + c

        elif c == ')':
            while stack[-1] != '(':
                postfix = postfix + stack[-1]
                stack = stack[:-1]
            stack = stack[:-1]

        elif c in specials:
            while stack and specials.get(c, 0) <= specials.get(stack[-1], 0):
                postfix = postfix + stack[-1]
                stack = stack[:-1]
            stack = stack + c
        else:
            postfix = postfix + c

    while stack:
        postfix = postfix + stack[-1]
        stack = stack[:-1]

    return postfix


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

def followes(state):
    """Return the set of states that can be reached from state following e arrows"""

    # create a new set with state as its only member
    states = set()
    states.add(state)

    # check if state has arrows labelled e from it
    if state.label is None:
        # check if edge1 is a state
        if state.edge1 is not None:
            # if theres an edge1 then follow it
            states |= followes(state.edge1)

         # check if edge2 is a state
        if state.edge2 is not None:
            # if theres an edge2 then follow it
            states |= followes(state.edge2)

    # return set of states
    return states

def match(infix, string):
    """Matches the string to the infix regular expression"""

    # shunt and compile the regular expression
    postfix = shunt(infix)
    nfa = compile(postfix)

    # current set of states and the next set of states
    current = set()
    next = set()

    # add the initial state to the current set
    current |= followes(nfa.initial)

    # loop through each character in the string
    for s in string:
        # loop through the current set of states
        for c in current:
            # check if that state is labelled s
            if c.label == s:
                # add the edge1 state to the next set
                next |= followes(c.edge1)
        # set current to next and clear out next
        current = next
        next = set()

    # check if the accept state is in the set of current states
    return (nfa.accept in current)

infixes = ["a.b.c*", "a.(b|d).c*", "(a.(b|d))*", "a.(b.b)*.c"]
strings = ["", "abc", "abbc", "abcc", "abad", "abbbc"]

for i in infixes:
    for s in strings:
        print(match(i, s), i, s)
