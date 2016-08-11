import sys
import argparse
import itertools
import operator

def line_format(stream, char):
    """
    Yield formatted lines from stream input
    """
    for line in stream:
        line = line.rstrip('\n').split(char)
        yield line

def print_record(record, field):
    """
    Write data to stdout
    """
    if field != None:
        record = [ record[f] for f in field ]
    record = '\t'.join(str(i) for i in record)
    sys.stdout.write(record + '\n')

def sum_records(group, sum_col):
    """
    Sum records in group
    """
    first = True
    for record in group:
        if first:
            last_record = record
            first = False
        else:
            for i in sum_col:
                record[i] = int(record[i]) + int(last_record[i])
            last_record = record
    return record

def split_args(arg):
    """
    Split out comma delim input arg
    """
    if arg is None:
        return arg
    else:
        return [ int(i) for i in arg.split(',') ]

def group_input(stream, args):
    """
    Group input by the groupby key, sum, and output results
    """
    groupby = split_args(args.groupby)
    sum_col = split_args(args.sum_col)
    group_key = operator.itemgetter(*groupby)

    for key, group in itertools.groupby(line_format(stream, args.char),
                                        key=lambda x: group_key(x)):
        record = sum_records(group, sum_col)
        print_record(record, split_args(args.field))

def cmd_line_parser(args):
    """
    Parse cmd line args
    """
    parser = argparse.ArgumentParser()

    parser.add_argument("-g", "--groupby", action="store",
                        help="Comma delim list of columns to group by", dest="groupby")
    parser.add_argument("-s", "--sum_col", action="store",
                        help="Comma delim list of columns to sum on", dest="sum_col")
    parser.add_argument("-f", "--field", action="store",
                        help="Comma delim list of fields to be printed", dest="field")
    parser.add_argument("-c", "--char", action="store", default="\t",
                        help="Input field delimiter, defaults to tab", dest="char")

    return parser.parse_args(args)

if __name__ == '__main__':
    args = cmd_line_parser(sys.argv[1:])
    group_input(sys.stdin, args)

