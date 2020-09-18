from os.path import abspath, dirname

curr_dir = dirname(abspath(__file__))

Productions_text = open('%s/bnf.txt' % curr_dir).read()

Productions_text = Productions_text.splitlines()

Productions_text = [i.strip().split() for i in Productions_text if len(i.strip())]

Productions = []

curr_head = None
for i in Productions_text:
    if '::=' in i:
        curr_head = i[0]
        Productions.append([curr_head] + i[2:])
    elif '|' == i[0]:
        Productions.append([curr_head] + i[1:])
    else:
        print('error:', i)

NT = set([i[0] for i in Productions])

Terminal = set()

for i in Productions:
    for a in i:
        if a not in NT:
            Terminal.add(a)

Terminal.remove('ε')

t = Terminal

__all__ = ['Terminal', 'Productions']
