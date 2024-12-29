def sum_list(l):
    total = 0
    for i in l:
        total += i
    return total

def min_max_avg(l):
    total = 0
    min_num = l[0]
    max_num = l[0]

    for i in l:
        total += i
        if i < min_num:
            min_num = i
        if i > max_num:
            max_num = i

    avg = total / len(l)

    return min_num, max_num, avg

def do_string_list(l):
    sort_list = sorted(l)
    nguyen_list = [i for i in l if "nguyen" in i.lower()]
    four_word_list = [i for i in l if len(i.split()) >= 4]
    return sort_list, nguyen_list, four_word_list

name_list = [
    "Nguyen Van A",
    "Tran Van B",
    "Le Thi C",
    "Nguyen Thi D",
    "Nguyen Thi Be Xuan",
]

print(sum_list([1, 2, 3, 4, 5]))
print(min_max_avg([1, 2, 3, 4, 5]))
print(do_string_list(name_list))