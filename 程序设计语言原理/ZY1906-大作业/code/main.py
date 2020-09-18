from scanner.scanner import scan, ScanError
from parser import lr1
from parser.symbol import Productions, Terminal
from parser.tools import NullableSet, First, Follow, LR1_parse_table
import pickle
import sys


def make_LR1_parse_table():
    nullable_set = NullableSet(Productions)
    first_set = First(Productions, Terminal, nullable_set)
    productions, parse_tab = LR1_parse_table(
        Productions, first_set, Terminal, nullable_set, start_symbol='Program')
    pickle.dump((productions, dict(parse_tab)),
                open('./data/LR1_parse_table.dat', 'wb'))

def main():
    try:
        fp = open('./data/LR1_parse_table.dat', 'rb')
    except FileNotFoundError:
        print(
            "Please run \"python3 %s make-parse-table\" before you first use this program." % sys.argv[0])
        return

    show_tree_after_iteration = True if 'show-tree-animation' in sys.argv else False
    show_simplify_tree = True if 'show-simplify-tree' in sys.argv else False

    productions, parse_tab = pickle.load(fp)
    try:
        tokens, symbol_table, const_string_table = scan(sys.argv[1])
        res = lr1.prase(tokens, parse_tab, productions, Terminal, symbol_table, const_string_table,
                        simpify=show_simplify_tree, show_tree_after_iteration=show_tree_after_iteration)
        lr1.show_tree(res, symbol_table, const_string_table)
        print('符号表:')
        for s in symbol_table:
            print('\t',s)
        print('字符串表:')
        for s in const_string_table:
            print("\t'%s'"%s)
    except ScanError as e:
        e.show_error(sys.argv[1])
    except lr1.ParseError as e:
        e.show_error(sys.argv[1])

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print(
            'Usage: \tpython3 %s src_path [show-tree-animation] [show-simplify-tree]' % sys.argv[0])
        print('\tpython3 %s make-parse-table' % sys.argv[0])
        sys.exit()
    if sys.argv[1] == 'make-parse-table':
        make_LR1_parse_table()
    else:
        main()
