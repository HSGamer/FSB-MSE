n = int(input("Enter a number: "))
i = 2
list = []
dict = {}
while i <= n:
    if n % i == 0:
        list.append(i)
        dict[i] = dict.get(i, 0) + 1

        n = n // i
    else:
        i += 1

print("Prime factors:", list)
print("Prime factors with frequency:", dict)