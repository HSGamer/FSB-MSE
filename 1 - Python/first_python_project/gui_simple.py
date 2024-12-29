import tkinter as tk

window = tk.Tk()

window.title("Simple GUI")
window.geometry("300x200")
window.grid_columnconfigure(0, weight=1)
window.grid_columnconfigure(1, weight=1)

label = tk.Label(window, text="Hello, World!")
label.grid(row=0, column=0, columnspan=2)

button = tk.Button(window, text="Click Me!")
button.grid(row=1, column=0, sticky="e")

entry = tk.Entry(window)
entry.grid(row=1, column=1, sticky="ew")

window.mainloop()