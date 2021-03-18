from solution import Wire

w1 = Wire(3)
w2 = Wire(4)

print(w1)
print(w2)

print(~w1)
print(~w2)
print(w1 ^ w2)
print(w1 | w2)
print(w1 & w2)
print(w2 >> 1)
print(w2 << 2)