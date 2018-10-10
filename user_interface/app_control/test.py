
a = [60,50,40]
b = [30]

c = a + b
d = ''

for element in c:
    d += str(element) + ','

d = d[:-1]
print(d)
