def prime_factor(n):
    list = []
    i = 2
    while i <= n:
        if n % i == 0:
            list.append(i)
            n = n / i
        else:
            i += 1
    return list

print(prime_factor(630))