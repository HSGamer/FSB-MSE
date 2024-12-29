weight = float(input("Enter your weight in kg: "))
height = float(input("Enter your height in meters: "))

bmi = weight / (height ** 2)
print("Your BMI is: ", bmi)

if bmi < 18.5:
    print("You are underweight.")
elif bmi <= 24.9:
    print("You are normal weight.")
elif bmi <= 29.9:
    print("You are overweight.")
elif bmi <= 34.9:
    print("You are obese (class 1).")
elif bmi <= 39.9:
    print("You are obese (class 2).")
else:
    print("You are obese (class 3).")