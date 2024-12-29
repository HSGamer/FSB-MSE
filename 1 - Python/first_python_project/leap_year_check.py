year = int(input("Enter a year: "))

is_leap_year = year % 4 == 0 and (year % 100 != 0 or year % 400 == 0)

if is_leap_year:
    print(year, "is a leap year.")
else:
    print(year, "is not a leap year.")