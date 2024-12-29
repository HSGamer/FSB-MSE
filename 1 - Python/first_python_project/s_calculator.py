x = int(input("X: "))
n = int(input("N: "))

sum = 0

for i in range(1, n + 1):
    exp = x ** i
    fac = 1
    for j in range(1, i + 1):
        fac *= j

    sum += exp / fac

print("S:", sum)