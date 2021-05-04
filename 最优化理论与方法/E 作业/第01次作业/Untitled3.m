[x,y]=fmincon('fun1',rand(2,1),[],[],[],[],[],[],'fun2')
print([x,y])