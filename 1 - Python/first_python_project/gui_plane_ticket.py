import tkinter as tk
from tkinter import ttk, messagebox

# pip install tkcalendar
from tkcalendar import Calendar

# region Locations
locations = ["New York", "Los Angeles", "Chicago", "Houston", "Phoenix"]
# endregion

# region Elements
app = tk.Tk()
app.title("Plane Ticket Booking")

title_label = tk.Label(app, text="PLANE TICKET BOOKING", font=("Arial", 16, "bold"), fg="blue")
title_label.grid(row=0, column=0, columnspan=3)

from_frame = tk.Frame(app)
from_frame.grid(row=1, column=0, padx=10, pady=10)
from_label = tk.Label(from_frame, text="From:", fg="green")
from_label.pack()
from_combobox = ttk.Combobox(from_frame, values=locations)
from_combobox.pack()

to_frame = tk.Frame(app)
to_frame.grid(row=1, column=2, padx=10, pady=10)
to_label = tk.Label(to_frame, text="To:", fg="green")
to_label.pack()
to_combobox = ttk.Combobox(to_frame, values=locations)
to_combobox.pack()

from_date_frame = tk.Frame(app)
from_date_frame.grid(row=2, column=0, padx=10, pady=10)
from_date_label = tk.Label(from_date_frame, text="From Date:", fg="purple")
from_date_label.pack()
from_calendar = Calendar(from_date_frame, selectmode="day", date_pattern="dd/mm/yyyy")
from_calendar.pack()

return_var = tk.IntVar()

return_date_frame = tk.Frame(app)
return_date_frame.grid(row=2, column=2, padx=10, pady=10)
return_checkbutton = tk.Checkbutton(return_date_frame, text="Return Date:", variable=return_var, fg="purple")
return_checkbutton.pack()
return_calendar = Calendar(return_date_frame, selectmode="day", date_pattern="dd/mm/yyyy", state="disabled")
return_calendar.pack()

ticket_type_canvas = tk.Canvas(app, width=100, height=100)
ticket_type_canvas.grid(row=1, column=1, padx=10, pady=10)

button_frame = tk.Frame(app)
button_frame.grid(row=2, column=1, padx=10, pady=10)
save_button = tk.Button(button_frame, text="Save", bg="lightgreen")
save_button.grid(row=0, column=0, sticky="ew")
quit_button = tk.Button(button_frame, text="Quit", command=app.quit, bg="lightcoral")
quit_button.grid(row=1, column=0, sticky="ew")

app.grid_columnconfigure(0, weight=1)
app.grid_columnconfigure(2, weight=1)


# endregion

# region Functions
def draw_arrow(one_way=True):
    ticket_type_canvas.delete("all")
    ticket_type_canvas.create_line(10, 50, 90, 50, arrow=tk.LAST if one_way else tk.BOTH)


draw_arrow()


def toggle_return():
    if return_var.get():
        return_calendar.config(state="normal")
        draw_arrow(False)
    else:
        return_calendar.config(state="disabled")
        draw_arrow()


return_checkbutton.config(command=toggle_return)


def save_info():
    from_location = from_combobox.get()
    to_location = to_combobox.get()
    from_date = from_calendar.get_date()
    return_date = return_calendar.get_date() if return_var.get() else None

    if not from_location or not to_location:
        messagebox.showerror("Error", "Please select both from and to locations.")
        return

    if from_location == to_location:
        messagebox.showerror("Error", "From and To locations cannot be the same.")
        return

    if return_var.get() and from_date >= return_date:
        messagebox.showerror("Error", "Return date must be after the from date.")
        return

    with open("booking_info.txt", "w") as file:
        file.write(f"From: {from_location}\n")
        file.write(f"To: {to_location}\n")
        file.write(f"From Date: {from_date}\n")
        if return_date:
            file.write(f"Return Date: {return_date}\n")

    messagebox.showinfo("Success",
                        (
                            f"Your booking information has been saved.\n"
                            f"You can find the details in the file booking_info.txt\n"
                            f"\n"
                            f"From: {from_location}\n"
                            f"To: {to_location}\n"
                            f"From Date: {from_date}\n"
                            f"Return Date: {return_date if return_date else "N/A"}\n"
                            f"\n"
                            f"Thank you for booking with us!\n"
                        )
                        )


save_button.config(command=save_info)
# endregion

app.mainloop()
