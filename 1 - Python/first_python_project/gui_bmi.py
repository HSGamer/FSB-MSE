import tkinter as tk
from tkinter import messagebox

bmi_status = {
    1: "Underweight",
    2: "Normal weight",
    3: "Overweight",
    4: "Obese (class 1)",
    5: "Obese (class 2)",
    6: "Obese (class 3)",
}

bmi_colors = {
    1: "#FFD700",
    2: "#00FF00",
    3: "#FFFF00",
    4: "#FFA500",
    5: "#FF4500",
    6: "#FF0000",
}


def calculate_bmi(weight, height):
    return weight / (height ** 2)


def get_bmi_status(bmi):
    if bmi < 18.5:
        return 1
    elif bmi <= 24.9:
        return 2
    elif bmi <= 29.9:
        return 3
    elif bmi <= 34.9:
        return 4
    elif bmi <= 39.9:
        return 5
    else:
        return 6


window = tk.Tk()
window.title("BMI Calculator")

logo = tk.Canvas(window, width=50, height=50)
logo.grid(row=0, column=0, rowspan=2)
logo.create_oval(0, 0, 50, 50, fill="blue")
logo.create_text(25, 25, text="BMI", fill="white")

weight_label = tk.Label(window, text="Weight (kg):")
weight_label.grid(row=0, column=1, padx=10)

weight_entry = tk.Entry(window)
weight_entry.grid(row=0, column=2, pady=5, sticky="EW")

height_label = tk.Label(window, text="Height (m):")
height_label.grid(row=1, column=1, padx=10)

height_entry = tk.Entry(window)
height_entry.grid(row=1, column=2, pady=5, sticky="EW")

calculate_button = tk.Button(window, text="Calculate BMI")
calculate_button.grid(row=2, column=1, columnspan=2, sticky="NEW")

bmi_label = tk.Label(window, text="BMI:")
bmi_label.grid(row=3, column=1)

bmi_value = tk.Entry(window, state="readonly")
bmi_value.grid(row=3, column=2, sticky="EW")

status_label = tk.Label(window, text="Status:")
status_label.grid(row=4, column=1)

status_value = tk.Entry(window, state="readonly")
status_value.grid(row=4, column=2, sticky="EW")

window.columnconfigure(2, weight=1)
window.rowconfigure(2, weight=1)


def on_calculate():
    try:
        weight = float(weight_entry.get())
        height = float(height_entry.get())
        if weight <= 0 or height <= 0:
            raise ValueError
    except ValueError:
        messagebox.showerror("Error", "Invalid input")
        return

    bmi = calculate_bmi(weight, height)
    bmi_value.config(state="normal")
    bmi_value.delete(0, tk.END)
    bmi_value.insert(0, "{:.2f}".format(bmi))
    bmi_value.config(state="readonly")

    status = get_bmi_status(bmi)
    status_value.config(state="normal")
    status_value.delete(0, tk.END)
    status_value.insert(0, bmi_status[status])
    status_value.config(state="readonly")
    status_value.config(readonlybackground=bmi_colors[status])


calculate_button.config(command=on_calculate)

window.mainloop()
