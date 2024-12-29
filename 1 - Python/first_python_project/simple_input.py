x = int(input("Enter a number: "))
if x % 2 == 0:
    print(x, "is Even")
else:
    print(x, "is Odd")

if x > 0:
    print(x, "is Positive")
elif x < 0:
    print(x, "is Negative")
else:
    print(x, "is Zero")