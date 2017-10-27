#!/usr/bin/python3

def match_brackets(text):
    """
    Checks, whether brackets in the given string are in correct sequence.
    Any opening bracket should have closing bracket of the same type.
    Bracket pairs should not overlap, though they could be nested.

    Returns true if bracket sequence is correct, false otherwise.
    """

    # http://www.codeabbey.com/index/task_view/matching-brackets

    assert isinstance(text, str)

    opening = '([{<'
    closing = ')]}>'
    bracket_stack = []
    stack_length = 0

    for char in text:
        if char in opening:
            bracket = closing[opening.index(char)]
            bracket_stack.append(bracket)
            stack_length += 1
        elif char in closing:
            if (stack_length < 1) or (char != bracket_stack.pop()):
                return False
            stack_length -= 1

    if stack_length or bracket_stack:
        return False
    return True