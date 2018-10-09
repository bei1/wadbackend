a = {1:False,
     2:True,
     3:True,
     4:False}

b = {1:True,
     2:False,
     3:False,
     4:False}

c = {1:True,
     2:True,
     3:True}

# if(c.items() - b.items()):
#     print('changed')
# else:
#     print('unchange')
#
# print(len(c))
obj = a.items() - b.items()
for item in obj:
    if(item[1]):
        print("node:",item[0])
        print("value", item[1])
        print("time","bbbbb")

#print(a.items() - b.items())