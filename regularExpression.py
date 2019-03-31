# Mark Gilmore
# Shunting Yard Algorithm
# http://www.oxfordmathcenter.com/drupal7/node/628

def shunt(infix):
    """ 
    Developed by Edsger Dijkstra The Shunting Yard Algorithm 
    changes an infix notation to a postfix notation using a stack
    to hold operators.
    The purpose of the stack is to reverse the order of the 
    operators in the expression.
    """

    # setting operator precedence
    opPrecedence = { '*': 60, '+': 50, '?': 50, '.': 40, '|': 30 }

    postfix = ""
    stack = ""

    # looping through the string
    for c in infix:
        # push open bracket to stack
        if c == '(':
            stack = stack + c

        elif c == ')':
            while stack[-1] != '(':
                postfix = postfix + stack[-1]
                stack = stack[:-1]
            # removes closing bracket from the stack
            stack = stack[:-1]

        elif c in opPrecedence:
            while stack and opPrecedence.get(c, 0) <= opPrecedence.get(stack[-1], 0):
                # concat next character to string
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
"""
Thompsons Construction is a method of transforming regular expressions into 
nondeterministic finite automaton (NFA). 
This NFA can be used to match strings against the regular expression.
"""

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

    # NFA constructor
    def __init__(self, initial, accept):
        self.initial = initial
        self.accept = accept

def compile(postfix):
    nfaStack = []

    for c in postfix:
        if c == '.': # concat
            # pop two nfa's off the stack
            nfa2 = nfaStack.pop()
            nfa1 = nfaStack.pop()

            # connect first nfa's accept state to the second's initial state
            nfa1.accept.edge1 = nfa2.initial

            # push to stack
            newnfa = nfa(nfa1.initial, nfa2.accept)
            nfaStack.append(newnfa)

        elif c == '+': # one or more
            # pop one nfa from the stack
            nfa1 = nfaStack.pop()

            # create new initial and accept state
            initial = state()
            accept = state()

            # join the new initial state to nfa's initial state and the new accept state
            initial.edge1 = nfa1.initial
            
            # join the old accept state to the new accept and nfa1's initial state
            nfa1.accept.edge1 = nfa1.initial
            nfa1.accept.edge2 = accept

            # push the new nfa to the stack
            new_nfa = nfa(initial, accept)
            nfaStack.append(new_nfa)
        
        # Operator - 1 or 0
        elif c == "?": # one or zero
            # pop a one nfa from the stack
            nfa1 = nfaStack.pop()

            # create new initial and accept state
            initial = state()
            accept = state()

            # point new initial state edge1 to the popped nfa's initial state 
            initial.edge1 = nfa1.initial

            # point new initial states edge2 to new accept state
            initial.edge2 = accept

            # point popped nfa's accept state edge1 to new accept state 
            nfa1.accept.edge1 = accept

            # push the new nfa to stack
            new_nfa = nfa(initial, accept)
            nfaStack.append(new_nfa)
        

        elif c == '|': # or
            # pop two nfa's off the stack
            nfa2 = nfaStack.pop()
            nfa1 = nfaStack.pop()

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
            newnfa = nfa(initial, accept)
            nfaStack.append(newnfa)

        elif c == '*': # zero or more
            # pop a single nfa from the stack
            nfa1 = nfaStack.pop()

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
            newnfa = nfa(initial, accept)
            nfaStack.append(newnfa)

        else: # deals with any other characters
            # create new initial and accept states
            accept = state()
            initial = state()
        
            # join the initial state and the accept state using an arrow labelled c
            initial.label = c
            initial.edge1 = accept

            # push the new nfa to the stack
            newnfa = nfa(initial, accept)
            nfaStack.append(newnfa)

    # nfaStack should only have a single nfa at this point
    return nfaStack.pop()

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

infixes = ["a.b.c*", "a.b.c+", "a.b.c?", "a.(b|d).c*", "(a.(b|d))*", "a.(b.b)*.c" ]
strings = ["", "abc", "abcd", "abba", "abbc", "abcc", "abad", "abbbc"]

for i in infixes:
    for s in strings:
        print(match(i, s), i, s)
