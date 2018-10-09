

f = open('./test', 'r+b')

print(f.read())

f.write(b'what?')

print(f.read())

f.close()