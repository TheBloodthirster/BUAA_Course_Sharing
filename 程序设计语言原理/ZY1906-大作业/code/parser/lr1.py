from collections import defaultdict, namedtuple, OrderedDict
from scanner.scanner import scan, IDENTIFIER, CHAR, Token,Symbol
import time


class ParseError(Exception):
    def __init__(self, token, excepted_symbol):
        self.token = token
        self.excepted_symbol = excepted_symbol

    def show_error(self, file):
        print('ParseError\nTraceback:\tFile "{}", line {}'.format(file, self.token.line_no))
        with open(file, 'r') as f:
            for l_no, l in enumerate(f, 1):
                if l_no == self.token.line_no:
                    print('    -> {}'.format(l), end='')
                elif l_no > self.token.line_no-3 and l_no < self.token.line_no+3:
                    print('{:6d} {}'.format(l_no, l), end='')
                elif l_no >= self.token.line_no+3:
                    break
        print('\nParseError: Except \'{}\'\nGot \'{}\''.format(
            "', '".join(self.excepted_symbol), self.token.terminal))


def show_tree(trees, symbols, const_string, delay=0, max_symbol_len=25):
    """
    显示语法分析树
    """
    def show_leaf(leaf):
        try:
            name, attr, line_no = leaf
        except:
            print(leaf)
            return
        if name == IDENTIFIER:
            print(IDENTIFIER, symbols[attr].name)
        elif name == CHAR:
            print(const_string[attr])
        else:
            print(name, attr or '')

    def show_level(node, left_space):
        n = len(node)
        for i in range(n):
            space = ' '*max_symbol_len
            if n == 1:
                print('─', end='')
            elif i == 0:
                print('┬', end='')
                space = '│'+(max_symbol_len-1)*' '
            elif i == n-1:
                print(left_space+'└', end='')
            else:
                space = '│'+(max_symbol_len-1)*' '
                print(left_space+'├', end='')

            if isinstance(node[i], Node):  # 语法树内部节点
                print('─%s%s' % (
                    node[i].NT, '─'*(max_symbol_len-2-len(node[i].NT.encode('gbk')))), end='')
                show_level(node[i].children, left_space + space)
            else:  # 语法树叶子节点
                print('─', end='')
                show_leaf(node[i])

    print('\33[H\33[2J', end='')
    for n in trees:
        print(' ', end='')
        if isinstance(n, Node):  # 语法树内部节点
            print('%s%s' % (n.NT, '─'*((max_symbol_len-2) -
                                       len(n.NT.encode('gbk')))), end='')
            show_level(n.children, ' '*(max_symbol_len-1))
        else:
            show_leaf(n)
    time.sleep(delay)


Node = namedtuple('Node', 'NT children')


def type_recognize(production, reduct_body, symbol_tab, const_string):
    """
    对于标识符的类型进行识别并更新符号表
    """
    def simpify(node):
        if isinstance(node, Node) and len(node.children) == 1:
            return simpify(node.children[0])
        elif isinstance(node, Token):
            return node
        else:
            return [simpify(i) for i in node.children]
    def get_children(node):
        s = set()
        if isinstance(node, Node):
            for n in node.children:
                s = s.union(get_children(n))
        else:
            s = {node}
        return s

    reduct_body = [simpify(i) for i in reduct_body]
    
    if production[0] == '<常数定义>':  # <常数定义> => <标识符>=<常数>;
        symbol = symbol_tab[reduct_body[0].value]
        symbol.type = Symbol.Const
        const_map = {'<整数>':Symbol.Integer ,'<布尔常数>':Symbol.Bool ,'<实数>': Symbol.Real,'<字符常量>':Symbol.Char}
        symbol.const_type = const_map[reduct_body[2].terminal]
        symbol.const_value = reduct_body[2].value
    elif production[0]=='<变量定义>': # <变量定义> => <标识符表>:<类型>;
        type_, array_type, array_len = None,None,None
        type_map = {'integer':Symbol.Integer ,'bool':Symbol.Bool ,'real': Symbol.Real,'char':Symbol.Char}
        if isinstance(reduct_body[2],Token): # 简单类型
            type_ = type_map[reduct_body[2].terminal]
        else: # 复合类型
            t = reduct_body[2]
            type_ = Symbol.Array
            array_type = type_map[t[5].terminal]
            array_len = t[2].value
        for sid in get_children(reduct_body[0]):
            s = symbol_tab[sid.value]
            s.type = type_
            s.array_type = array_type
            s.array_len = array_len
    elif production[0]=='<过程说明>':  # <过程说明>→procedure<标识符>(<形参表>)<分程序>
        symbol = symbol_tab[reduct_body[1].value]
        symbol.type = Symbol.Procedure
    elif production[0]=='<程序>':  # <程序>→program<标识符><分程序>
        symbol = symbol_tab[reduct_body[1].value]
        symbol.type = Symbol.Program

def prase(tokens, trans_tab, productions, terminals, symbol_tab, const_string, simpify=False, show_tree_after_iteration=False):
    """
    LR语法分析程序

    由于符号栈只是暂存最右推导的有效前缀，并不进行读取，所以这里在其中保存了语法生成树
    """
    states = [0]  # 状态栈
    symbols = []  # 符号栈

    tokens.append(Token('$', None, tokens[-1].line_no))
    curr_token_index = 0
    while True:
        token = tokens[curr_token_index]
        terminal = token[0]

        if terminal not in trans_tab[states[-1]]:
            raise ParseError(token, set(trans_tab[states[-1]]) & terminals)
        action, action_data = trans_tab[states[-1]][terminal]
        if action == 0:  # 移进
            symbols.append(token)
            states.append(action_data)
            curr_token_index += 1
            # print('移进', terminal)
        elif action == 1:  # 规约
            left, *right = productions[action_data]
            reduct_body = symbols[-len(right):] if right else [Token('ε', None, None)]
            for _ in range(len(right)):
                states.pop()
                symbols.pop()
            _, new_state = trans_tab[states[-1]][left]
            states.append(new_state)

            try: type_recognize(productions[action_data], reduct_body, symbol_tab, const_string)
            except: pass

            if simpify and len(right) == 1 and isinstance(reduct_body[0][1], list):
                symbols.append(Node(left, reduct_body[0][1]))
            else:
                symbols.append(Node(left, reduct_body))
            # print('规约: {} => {}'.format(left, ''.join(right)))
        elif action == 2:  # 接受
            break
        if show_tree_after_iteration:
            show_tree(symbols, symbol_tab, const_string, delay=0.06)
    return symbols
