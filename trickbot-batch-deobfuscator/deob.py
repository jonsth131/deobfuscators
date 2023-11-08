#!/usr/bin/env python3
import sys
import re


def variable_pass(data):
    sets = []
    return_data = []
    for line in data.split('\n'):
        if line.startswith('set ') and '%' not in line:
            sets.append(line)
        else:
            return_data.append(line)

    return_data = '\n'.join(return_data)

    if not sets:
        return return_data

    for line in sets:
        match = re.match(r'set (\w+)=(.*)', line)
        variable = f'%{match.group(1)}%'
        value = match.group(2)
        return_data = re.sub(variable, value, return_data)

    return variable_pass(return_data)


def exitcode_pass(data):
    sets = []
    return_data = []

    set_line = None

    for line in data.split('\n'):
        if line.startswith('set /a'):
            set_line = line
        elif line.startswith('cmd'):
            continue
        elif line.endswith('%=exitcodeAscii%'):
            match = re.match(r'set (\w+)=.*', line)
            variable = f'%{match.group(1)}%'
            match = re.match(r'set \/a \w+=(\d+) %% (\d+)', set_line)
            value = chr(int(match.group(1)) % int(match.group(2)))
            sets.append((variable, value))
            set_line = None
        else:
            return_data.append(line)

    return_data = '\n'.join(return_data)
    for variable, value in sets:
        return_data = re.sub(variable, value, return_data)

    return return_data


def clear_rem_lines(data):
    return '\n'.join([line for line in data.split('\n') if not line.startswith('rem ')])


def clear_comments(data):
    return '\n'.join([line for line in data.split('\n') if not line.startswith('::')])


if __name__ == '__main__':
    if len(sys.argv) != 3:
        print(f'Usage: {sys.argv[0]} <obfuscated file> <output file>')
        sys.exit(1)

    with open(sys.argv[1], 'r') as f:
        data = f.read()

    data = variable_pass(data)
    data = exitcode_pass(data)
    data = variable_pass(data)
    data = clear_rem_lines(data)
    data = clear_comments(data)

    with open(sys.argv[2], 'w') as f:
        f.write(data)

    sys.exit(0)
