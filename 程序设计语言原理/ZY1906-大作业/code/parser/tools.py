from collections import defaultdict, namedtuple, OrderedDict


def remove_left_recursive(productions):
    """
    消除左递归
    """
    productions = sorted(productions)
    P_dict = defaultdict(list)
    r_set = set()
    for left, *right in productions:
        P_dict[left].append(right)
        if left == right[0]:
            r_set.add(left)

    for A in r_set:
        """
        A -> Aa|Ab|...|c|d...
        A -> cA'|dA'|...
        A'-> aA'|bA'|...
        """
        A_ = A+'_'
        P_A = P_dict[A][:]
        P_dict[A] = []
        for pp in P_A:
            if pp[0] == A:  # A -> Aa
                P_dict[A_].append(pp[1:]+[A_])  # A'-> aA'
            else:  # A -> c
                P_dict[A].append(pp+[A_])  # A -> cA'
    return [[left]+right for left in P_dict for right in P_dict[left]]


def NullableSet(productions):
    """
    计算Nullable集
    """
    p = productions
    nulls = set()
    changing = True
    while changing:
        changing = False
        for left, *right in p:
            if left in nulls:
                continue
            if len(right) == 1 and right[-1] == 'ε':
                nulls.add(left)
                changing = True
            elif all(map(lambda i: i in nulls, right)):  # 右部全为nullable
                nulls.add(left)
                changing = True

    return nulls


def First(productions, terminal, nullable):
    """
    计算First集
    """
    p = productions
    first = defaultdict(set)
    changing = True
    while changing:
        changing = False
        for left, *right in p:
            if len(right) == 1 and right[-1] == 'ε':
                continue
            for b in right:
                if b in terminal:
                    if b not in first[left]:
                        first[left].add(b)
                        changing = True
                    break
                else:
                    if first[b]-first[left]:
                        first[left] = first[left].union(first[b])
                        changing = True
                    if b not in nullable:
                        break
    return first


def First_S(ps, first, terminal, nullable, left=None, follow=None):
    """
    计算串的First集合， 如果传入了left（左部），则为计算left->ps推导式的select集
    """
    if len(ps) == 1 and ps[-1] == 'ε':
        return set()
    res = set()
    for b in ps:
        if b in terminal:
            res.add(b)
            return res
        else:
            res = res.union(first[b])
            if b not in nullable:
                return res
    if left and follow:
        res.add(follow[left])
    return res


def Nullable_S(ps, nullable):
    """
    判断串是否可为空
    """
    return all(map(lambda i: i in nullable, ps))


def Follow(productions, fitst, terminal, nullable):
    """
    计算Follow集
    """
    p = productions
    follow = defaultdict(set)
    changing = True
    while changing:
        changing = False
        for left, *right in p:
            if len(right) == 1 and right[-1] == 'ε':
                continue
            temp = follow[left]
            for b in right[::-1]:
                if b in terminal:
                    temp = follow[b]
                else:
                    if temp-follow[b]:
                        follow[b] = temp.union(follow[b])
                        changing = True
                    if b in nullable:
                        temp = temp.union(fitst[b])
                    else:
                        temp = fitst[b]

    return follow


"""
LR(1)项的定义;
(pid, dot, ahead)
即(推导式id， 点的位置， 前看符号集)
"""
Item = namedtuple('Item', 'pid dot ahead')

def closure(items, productions, FIRST, TERMINAL, Nullable):
    """
    计算项集的闭包，并检验闭包是否有移进-规约冲突和规约-规约冲突
    """
    left_lookup = defaultdict(list)  # 每个非终结符的编号列表
    for id, (left, *right) in enumerate(productions):
        left_lookup[left].append(id)

    res = set(items)
    changing = True
    while changing:
        changing = False
        for s in res.copy():
            left, *right = productions[s.pid]
            # 对于每一个形如 A -> a*Bb, c 的项
            if len(right) > s.dot and right[s.dot] not in TERMINAL: # 项可展开
                fs = First_S(right[s.dot+1:], FIRST, TERMINAL, Nullable)
                if Nullable_S(right[s.dot+1:], Nullable):  # Bc可为空
                    fs = fs.union(s.ahead)
                for pid in left_lookup[right[s.dot]]:
                    t = Item(pid, 0, tuple(fs))
                    if t not in res:
                        res.add(t)
                        changing = True

    """
    开始校验闭包是否存在冲突
        规约-规约冲突：规约项前看符号有交集
        移进-规约冲突：规约项前看符号与移进项移入符号有交集
    """
    reduct_ahead = set()  # 规约项前看符号
    shift_symbol = set()  # 移进项移入符号
    for item in res:
        left, *right = productions[item.pid]
        if len(right) == item.dot:  # 规约项
            if set(item.ahead) & reduct_ahead:
                raise ValueError('计算项集闭包时发现规约-规约冲突，冲突闭包：%s' % res,res)
            else:
                reduct_ahead = reduct_ahead.union(item.ahead)
        elif right[item.dot] in TERMINAL:  # 移进项
            shift_symbol.add(right[item.dot])
    if shift_symbol & reduct_ahead:
        raise ValueError('计算项集闭包时发现移进-规约冲突，冲突闭包：%s' % res, res)

    return res


def goto(items, X, productions, FIRST, TERMINAL, Nullable):
    """
    计算当前闭包下输入X后的下一状态（闭包）
    X可以为终结符和非终结符
    """
    res = set()
    for item in items:
        p = productions[item.pid]
        if (item.dot+1) < len(p) and p[item.dot+1] == X:
            c = closure({Item(item.pid, item.dot+1, item.ahead)},
                        productions, FIRST, TERMINAL, Nullable)
            res = res.union(c)
    return res


def LR1_parse_table(productions, FIRST, TERMINAL, Nullable, start_symbol='<程序>'):
    """
    构造状态转换表
    """
    productions = productions[:]
    productions.insert(0, ('S', start_symbol))  # 增广文法
    for i in range(len(productions)):
        if productions[i][-1] == 'ε' and len(productions[i]) == 2:
            productions[i] = (productions[i][0],)
    TERMINAL = TERMINAL.copy()
    TERMINAL.add('$')

    """
    trans_tab 为状态转移表
        {state=>{symbol=> action}, }
        action: (type,attribute), 
        type: 0 for 移进，1 for 规约， 2 for 接受， 3 for goto
    """
    trans_tab = defaultdict(dict)
    c = closure({Item(0, 0, ('$',))}, productions, FIRST, TERMINAL, Nullable)
    states = [c]  # closure
    unresolve = [0]  # closure id that need resolve
    while unresolve:
        cid = unresolve.pop()
        for item in states[cid]:
            left, *right = productions[item.pid]
            if len(right) == item.dot:  # 规约项
                for ahead in item.ahead:
                    trans_tab[cid][ahead] = (1, item.pid)  # 设置action为”规约“
                    if item.pid == 0:
                        trans_tab[cid][ahead] = (2, item.pid)  # 设置action为”接受“
            elif right[item.dot] not in trans_tab[cid]:  # 未处理的移进项目和待归约项目
                c = goto(states[cid], right[item.dot],
                         productions, FIRST, TERMINAL, Nullable)
                try:
                    index = states.index(c)
                except ValueError:
                    states.append(c)
                    index = len(states)-1
                    unresolve.append(index)
                if right[item.dot] in TERMINAL:
                    trans_tab[cid][right[item.dot]] = (
                        0, index)  # 设置action为”移进“
                else:
                    trans_tab[cid][right[item.dot]] = (
                        3, index)   # 设置action为”GOTO“
    return productions, trans_tab