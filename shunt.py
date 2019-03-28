# Shunting Yard Algorithm
# Mark Gilmore
# http://www.oxfordmathcenter.com/drupal7/node/628

def shunt(infix):

    specials = { '*': 50, '.': 40, '|': 30 }

    postfix = ""
    stack = ""

    for char in infix:
        if char == '(':
            stack = stack + char

        elif char == ')':
            while stack[-1] != '(':
                postfix = postfix + stack[-1]
                stack = stack[:-1]
            stack = stack[:-1]

        elif char in specials:
            while stack and specials.get(char, 0) <= specials.get(stack[-1], 0):
                postfix = postfix + stack[-1]
                stack = stack[:-1]
            stack = stack + char
        else:
            postfix = postfix + char

    while stack:
        postfix = postfix + stack[-1]
        stack = stack[:-1]

    return postfix

print(shunt("(a.b)|(c*.d)"))