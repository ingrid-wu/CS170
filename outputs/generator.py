x = []
y = []
a = []
b = []
c = []
d = []
e = []
f = []
g = []
h = []

for i in range(50):
    x += [str(i)]
for j in range(50):
    y += [str(j + 50)]
for j in range(50):
    a += [str(j + 100)]
for j in range(50):
    b += [str(j + 150)]
for j in range(50):
    c += [str(j + 200)]
for j in range(50):
    d += [str(j + 250)]
for j in range(50):
    e += [str(j + 300)]
for j in range(50):
    f += [str(j + 350)]
for j in range(50):
    g += [str(j + 400)]
for j in range(50):
    h += [str(j + 450)]

f = open("large-input.out", "a")
f.write(str(x))
f.write('\n')
f.write(str(y))
f.write('\n')
f.write(str(a))
f.write('\n')
f.write(str(b))
f.write('\n')
f.write(str(c))
f.write('\n')
f.write(str(d))
f.write('\n')
f.write(str(e))
f.write('\n')
f.write(str(f))
f.write('\n')
f.write(str(g))
f.write('\n')
f.write(str(h))
