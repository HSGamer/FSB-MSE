import math

n = int(input("Enter a number: "))

is_prime = True
if n == 1:
    is_prime = False
elif n < 1:
    is_prime = False
else:
    for i in range(2, int(math.sqrt(n)) + 1):
        if n % i == 0:
            is_prime = False
            break

if is_prime:
    print(n, "is a prime number.")
else:
    print(n, "is not a prime number.")