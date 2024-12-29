import random

path = "Random.txt"
n = 1_000_000
with open(path, "w") as file:
    for i in range(n):
        file.write(str(random.randint(0, 10)))
        if random.random() > 0.5:
            file.write("\n")