
import argparse
import sys
import re


def output(line):
    print(line)   

def inverting(pattern, lst, line):
    temp = re.compile(pattern)
    if temp.search(line) == None:
        lst.append(line)

def ignoring_case(pattern, lst, line):
    pattern = pattern.lower()
    temp = re.compile(pattern)
    if temp.search(line.lower()):
        lst.append(line)

def separator(temp_pattern, value):
    sep = "-"
    if temp_pattern.search(value):
        sep = ":"
    return sep

def processing(params):
    pattern = params.pattern.replace('?', '.')
    pattern = pattern.replace('*', '.*')
    return pattern

def intersection(index, lines, lst, temp_lst, line_num, temp_pattern):
    lst_inter = []
    if temp_lst:
        if line_num:
            lst_inter = [(str(lines.index(value)+1) + separator(temp_pattern, value) + value) for value in temp_lst 
                if (str(lines.index(value)+1) + separator(temp_pattern, value) + value) not in lst]
        else:
            lst_inter = [value for value in temp_lst if (value not in lst)]
    return lst_inter


def contexts(params, pattern, lines, index, lst):
    temp_lst = []
    temp_pattern = re.compile(pattern)
    if temp_pattern.search(lines[index]):
        if params.context:
            temp_lst = lines[index-params.context:index+params.context+1]
        elif params.before_context:
            temp_lst = lines[index-params.context:index+1]
        elif params.after_context:
            temp_lst = lines[index:index+params.context+1]
        else:
            temp_lst.append(lines[index])
    lst.extend(intersection(index, lines, lst, temp_lst, params.line_number, temp_pattern))


def grep(lines, params):
    counter = 0
    lst = []
    for index in range(len(lines)):
        line = lines[index]
        pattern = processing(params)

        if params.invert:
            inverting(pattern, lst, line)
        elif params.ignore_case:
            ignoring_case(pattern, lst, line)
        elif params.count:
            temp = re.compile(pattern)
            if temp.search(line):
                counter += 1
        elif params.line_number:
            contexts(params, pattern, lines, index, lst)
        elif params.context or params.before_context or params.after_context:
            contexts(params, pattern, lines, index, lst)
        else:
            temp = re.compile(pattern)
            if temp.search(line):
                lst.append(line)
    if params.count:
        output(str(counter))
    else:
        for line_num in range(len(lst)):
            output(lst[line_num].strip())


def parse_args(args):
    parser = argparse.ArgumentParser(description='This is a simple grep on python')
    parser.add_argument(
        '-v', action="store_true", dest="invert", default=False, help='Selected lines are those not matching pattern.')
    parser.add_argument(
        '-i', action="store_true", dest="ignore_case", default=False, help='Perform case insensitive matching.')
    parser.add_argument(
        '-c',
        action="store_true",
        dest="count",
        default=False,
        help='Only a count of selected lines is written to standard output.')
    parser.add_argument(
        '-n',
        action="store_true",
        dest="line_number",
        default=False,
        help='Each output line is preceded by its relative line number in the file, starting at line 1.')
    parser.add_argument(
        '-C',
        action="store",
        dest="context",
        type=int,
        default=0,
        help='Print num lines of leading and trailing context surrounding each match.')
    parser.add_argument(
        '-B',
        action="store",
        dest="before_context",
        type=int,
        default=0,
        help='Print num lines of trailing context after each match')
    parser.add_argument(
        '-A',
        action="store",
        dest="after_context",
        type=int,
        default=0,
        help='Print num lines of leading context before each match.')
    parser.add_argument('pattern', action="store", help='Search pattern. Can contain magic symbols: ?*')
    return parser.parse_args(args)


def main():
    params = parse_args(sys.argv[1:])
    grep(sys.stdin.readlines(), params)


if __name__ == '__main__':
    main()
