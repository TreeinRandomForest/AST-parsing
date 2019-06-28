import re


def string_hashcode(s):
    h = 0
    for c in s:
        h = (31 * h + ord(c)) & 0xFFFFFFFF
    return ((h + 0x80000000) & 0xFFFFFFFF) - 0x80000000


# strip_docstring
def strip_docstring(code_string):
    a = []
    for y in re.finditer('"""', code_string):
        a.append(y)
    if len(a) == 0:
        return code_string
    output = ''
    output = output + code_string[0:a[0].start()]
    for i in range(int(len(a) / 2 - 1)):
        output = output + code_string[a[2 * i + 1].end():a[2 * i + 2].start()]
    output = output + code_string[a[len(a)-1].end():]
    return output