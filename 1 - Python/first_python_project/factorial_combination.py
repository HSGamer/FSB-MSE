def factorial(n, recursive=True):
    if n < 0:
        raise ValueError('n must be a non-negative integer')
    if recursive:
        if n == 0:
            return 1
        else:
            return n * factorial(n - 1)
    else:
        result = 1
        for i in range(1, n + 1):
            result *= i
        return result

def combination(n, k):
    if n < 0 or k < 0:
        raise ValueError('n and k must be non-negative integers')
    if k > n:
        return 0
    return factorial(n) // (factorial(k) * factorial(n - k))

print(combination(5, 2))