from collections import deque, namedtuple
import sys

IDENTIFIER = 'Identifier'
INTEGER = 'Integer_Literal'
BOOL = 'Integer_Literal'
REAL = 'Integer_Literal'
CHAR = 'Character_Literal'

# keywords = {'and', 'array', 'begin', 'bool', 'call', 'case', 'char', 'constant', 'do', 'else', 'end', 'for',
#             'if', 'input', 'integer', 'not', 'of', 'or', 'output', 'procedure', 'program', 'read', 'real', 'repeat',
#             'set', 'then', 'to', 'until', 'var', 'wgile', 'write', 'while'}
keywords = {'begin', 'proc', 'while', 'var', 'func', 'is',
            'do', 'array', 'in', 'record', 'if', 'let', 'then',
            'of', 'type', 'end', 'else', 'const', 'Char', 'Boolean', 'Integer', 'Real'}

double_separator = {':=', '<=', '>=', ':=', '==', '!='}
# single_separator = {'+', '-', '*', '/', '=', '<', '>',
#                     '(', ')', '[', ']', ':', '.', ';', ',', "'", '_'}

single_separator = {')', '+', '=', '(', '*', '[', ',', '%', ']', ':', '/', '}', '{', '-', ';', '>', '<', '!', '.'}


class ScanError(Exception):
    def __init__(self, msg):
        self.msg = msg
        self.line_no = None

    def show_error(self, file):
        print('ScanError\nTraceback:\tFile "{}", line {}'.format(file, self.line_no))
        with open(file, 'r') as f:
            for l_no, l in enumerate(f, 1):
                if l_no == self.line_no:
                    print('    -> {}'.format(l), end='')
                elif l_no > self.line_no - 3 and l_no < self.line_no + 3:
                    print('{:6d} {}'.format(l_no, l), end='')
                elif l_no >= self.line_no + 3:
                    break
        print('\nScanError: {}'.format(self.msg))


class Symbol:
    """ 符号表中的符号类
    保存的信息有:
        标识符名称、
        标识符类型、
        数组类型、数组维数 （如果当前符号类型为数组）
        过程参数表类型 （如果当前符号类型为过程）
        常量类型、常量值 （如果当前符号类型为常量）
    """
    __slot__ = ['name', 'type', 'array_type', 'array_len',
                'arg_types', 'const_type', 'const_value']
    Integer = 0
    Bool = 1
    Real = 2
    Char = 3
    Const = 4
    Array = 5
    Procedure = 6
    Program = 7

    def __init__(self, name, type_=None):
        self.name = name
        self.type = type_
        self.array_type = None  # 数组类型
        self.array_len = None  # 数组维数
        self.arg_types = None  # 过程参数表类型
        self.const_type = None  # 常量类型
        self.const_value = None  # 常量值

    def __repr__(self):
        type_map = {self.Integer: 'integer', self.Bool: 'bool', self.Real: 'real',
                    self.Char: 'char', self.Program: 'program', None: ''}
        if self.type == self.Array:
            return 'Symbol("{:s}", array[{:d}] of {:s})'.format(self.name, self.array_len, type_map[self.array_type])
        elif self.type == self.Const:
            return 'Symbol("{:s}", {:s} const, {})'.format(self.name, type_map[self.const_type], self.const_value)
        elif self.type == self.Procedure:
            return 'Symbol("{:s}", procedure )'.format(self.name)
        elif self.type == self.Program:
            return 'Symbol("{:s}", program )'.format(self.name)
        else:
            return 'Symbol("{:s}", {:s})'.format(self.name, type_map[self.type])

    def __eq__(self, other):
        return self.name == other.name


Token = namedtuple('Token', 'terminal value line_no')


def char_seq_gen(path):
    # 文件换成字符生成器
    for line in open(path):
        yield from line


def check_and_ignore_comment(q):
    """
    检测当前字符队列接下来的字符是否是注释，是的话则一直弹出队列元素，直到注释结束
    :param q: 字符队列
    :return int 注释所跨的行数, 为-1时表示未检测到注释, 0表示注释未跨行
    """
    c1 = q.popleft()
    c2 = q.popleft()
    if c1 != '/' or c2 != '*':
        q.insert(0, c2)
        q.insert(0, c1)
        return -1

    line_n = 0
    while q:
        c = q.popleft()
        if c == '*':
            c = q.popleft()
            if c == '/':
                return line_n
            else:
                q.insert(0, c)
        elif c == '\n':
            line_n += 1

    raise ScanError('注释没有闭合')


def read_alpha(q):
    """
    读取以字母开头的token，有标识符、关键字、布尔常数
    :param q: 字符队列
    :return: （token类别，token值）
    """
    res = []
    while q:
        c = q.popleft()
        if not c.isalnum():
            q.insert(0, c)
            break
        else:
            res.append(c)
    res = ''.join(res)
    if res in keywords:
        return res, None
    elif res in ('true', 'false'):
        return BOOL, 1 if res == 'true' else 0
    else:
        return IDENTIFIER, Symbol(res)


def read_digit(q):
    """
    读取以数字开头的token，有整型常量、实数
    :param q: 字符队列
    :return: （token类别，token值）
    """
    res = []
    dot = 0
    while q:
        c = q.popleft()
        if c.isdigit():
            res.append(c)
        elif c == '.' and not (dot):
            f2 = (q.popleft(), q.popleft())
            if f2 == ('.', '.'):
                q.insert(0, '.')
                q.insert(0, '.')
                q.insert(0, '.')
                break
            elif not f2[0].isdigit():
                raise ScanError('Can\'t get a real number!')
            q.insert(0, f2[1])
            q.insert(0, f2[0])
            res.append(c)
            dot = 1
        elif c == '.' and dot:
            raise ScanError('Get two \'.\' when try to scan a real number!')
        else:
            q.insert(0, c)
            break

    res = ''.join(res)
    if dot:
        return REAL, float(res)
    else:
        return INTEGER, int(res)


def read_separator(q):
    """
    读取分隔符token
    :param q: 字符队列
    :return: （token类别，token值）
    """
    c1 = q.popleft()
    if not q:
        if c1 not in single_separator:
            raise ScanError('Unvalid char \'%s\'!' % c1)
        else:
            return c1, None

    c2 = q.popleft()
    if c1 + c2 in double_separator:
        return c1 + c2, None
    # if c1 + c2 == '..':
    #     c3 = q.popleft()
    #     if c3 == '.':
    #         return '...', None
    #     else:
    #         raise ScanError('\'%s\' is not a valid token!!' % c1 + c2)
    elif c1 in single_separator:
        q.insert(0, c2)
        return c1, None
    else:
        raise ScanError('Can\'t get a valid token!! Error char "%s"'%c1)


def read_string(q):
    """
    读取字符常量token
    :param q: 字符队列
    :return: （STRING，token值）
    """
    q.popleft()
    res = []
    escape = 0
    while q:
        c = q.popleft()
        if escape:
            if c in ('\'', '\\',):
                res.append(c)
                escape = 0
            else:
                raise ScanError('Can\'t recognize \\%s in string!!' % c)
        elif c == '\\':
            escape = 1
        elif c == '\'':
            break
        else:
            res.append(c)
    else:
        raise ScanError('字符串没有闭合')

    res = ''.join(res)
    return CHAR, res


def scan(src_path):
    """
    对simple源文件进行词法扫描分析
    :param src_path: 源文件路径
    :return: （token序列，符号表，字符串表）
    """

    line_no = 1  # 当前token所在的行号
    tokens = []  # (type, attr)
    symbols = []  # 符号表
    const_string = []  # 字符串表
    q = deque(char_seq_gen(src_path))  # 根据源文件路径构造出字符队列
    while q:
        c = q.popleft()
        if c.isspace():
            if c == '\n':
                line_no += 1
            continue
        q.insert(0, c)  # 重新保存读出的字符
        try:
            if c == '/':
                res = check_and_ignore_comment(q)
                if res != -1:
                    line_no += res
                    continue
            if c.isalpha():
                token_type, value = read_alpha(q)
            elif c.isdigit():
                token_type, value = read_digit(q)
            elif c == "'":
                token_type, value = read_string(q)
            else:
                token_type, value = read_separator(q)
        except ScanError as e:
            e.line_no = line_no
            raise e

        if token_type == IDENTIFIER:  # 当前读到的token为标识符， 要把读到的结果写入符号表
            if value in symbols:
                tokens.append(Token(token_type, symbols.index(value), line_no))
            else:
                symbols.append(value)
                tokens.append(Token(token_type, len(symbols) - 1, line_no))
        elif token_type == CHAR:  # 当前读到的token为字符串常量， 要把读到的结果写如字符串表
            if value in const_string:
                tokens.append(
                    Token(token_type, const_string.index(value), line_no))
            else:
                const_string.append(value)
                tokens.append(
                    Token(token_type, len(const_string) - 1, line_no))
        else:
            tokens.append(Token(token_type, value, line_no))

    return tokens, symbols, const_string


def main():
    try:
        tokens, symbols, const_string = scan(sys.argv[1])
    except ScanError as e:
        e.show_error(sys.argv[1])
        return None, None, None

    for name, attr, line_no in tokens:
        print('#%03d %-14s' % (line_no, (name)), end='')
        if name == IDENTIFIER:
            print(symbols[attr])
        elif name == CHAR:
            print(const_string[attr])
        else:
            print(attr or '')

    return tokens, symbols, const_string


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('Usage: python3 %s source_file' % (sys.argv[0],))
    else:
        tokens, symbols, const_string = main()
