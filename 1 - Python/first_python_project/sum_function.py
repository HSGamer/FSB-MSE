def my_sum(*args):
    sum = 0
    for i in args:
        sum += i
    return sum

print(my_sum(1, 2, 3, 4, 5))