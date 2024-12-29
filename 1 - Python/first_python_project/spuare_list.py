def square_list(l):
    # def square(n):
    #     return n * n
    # return list(map(square, l))
    return map(lambda x: x * x, l)

print(list(square_list([1, 2, 3, 4, 5, 6, 7, 8, 9, 10])))