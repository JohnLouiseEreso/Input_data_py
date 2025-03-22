import tkinter as tk
from tkinter import ttk, messagebox
from tkcalendar import DateEntry

day_count = 1  # Initialize the day counter
all_data = []  # List to store past days' data
total_amount = 0  # Initialize total amount

def insert_data():
    """Inserts data into the table and updates the total amount."""
    global total_amount

    date = date_entry.get()
    category = category_combo.get()
    item = item_entry.get()
    amount = amount_entry.get()
    
    if date and category and item and amount:
        try:
            amount = float(amount)  # Convert amount to float for summation
            tree.insert("", "end", values=(date, category, item, f"{amount:.2f}"))
            total_amount += amount  # Update total
            update_total_label()  # Refresh the total amount display
            reset_inputs()  # Reset input fields after inserting data
        except ValueError:
            messagebox.showerror("Input Error", "Amount must be a number.")
    else:
        messagebox.showerror("Missing Data", "Please complete all fields before inserting.")

def reset_inputs():
    """Clears input fields for new entry."""
    date_entry.set_date(None)  # Reset date field correctly
    category_combo.set("")  # Reset category selection
    item_entry.delete(0, tk.END)  # Clear item field
    amount_entry.delete(0, tk.END)  # Clear amount field

def next_day():
    """Progresses the day count, saves current data, resets table, and keeps total."""
    global day_count, all_data, total_amount
    
    # Check if there is at least one entry before proceeding
    if not tree.get_children():
        messagebox.showwarning("No Data Entered", "Please insert at least one expense before moving to the next day.")
        return

    # Save the current day's data
    day_data = []
    for item in tree.get_children():
        day_data.append(tree.item(item)["values"])  # Store row data
    
    if day_data:
        all_data.append((f"Day {day_count}", day_data))  # Store with day label
    
    # Increment the day count
    day_count += 1
    day_label.config(text=f"Day {day_count}")
    
    # Clear the table for the new day
    tree.delete(*tree.get_children())

    # Reset input fields
    reset_inputs()

def update_total_label():
    """Updates the total amount label."""
    total_label.config(text=f"Total: {total_amount:.2f}")  # Format to 2 decimal places

def create_gui():
    global date_entry, category_combo, item_entry, amount_entry, tree, day_label, total_label
    
    root = tk.Tk()
    root.title("Expense Tracker")
    root.configure(bg="purple")
    
    # Style Configuration
    style = ttk.Style()
    style.configure("Treeview.Heading", font=("Arial", 12, "bold"))  # Bold headers

    
    # Day Label
    day_label = tk.Label(root, text=f"Day {day_count}", font=("Arial", 16, "bold"), fg="white", bg="purple")
    day_label.place(x=100, y=15)
    
    # Input Form
    form_frame = tk.Frame(root, bg="purple")
    form_frame.place(x=10, y=50)
    
    tk.Label(form_frame, text="Date", font=("Arial", 12, "bold"), fg="white", bg="purple").grid(row=0, column=0, sticky="w")
    date_entry = DateEntry(form_frame, font=("Arial", 12), width=18, background='darkblue', foreground='white', borderwidth=2)
    date_entry.grid(row=1, column=0, pady=5)
    
    tk.Label(form_frame, text="Category", font=("Arial", 12, "bold"), fg="white", bg="purple").grid(row=2, column=0, sticky="w")
    category_combo = ttk.Combobox(form_frame, font=("Arial", 12), width=18, values=["Food", "Transport", "Entertainment", "Rent", "Utilities", "Others"])
    category_combo.grid(row=3, column=0, pady=5)
    
    tk.Label(form_frame, text="Item", font=("Arial", 12, "bold"), fg="white", bg="purple").grid(row=4, column=0, sticky="w")
    item_entry = tk.Entry(form_frame, font=("Arial", 12), width=20, bg="lightyellow")
    item_entry.grid(row=5, column=0, pady=5)
    
    tk.Label(form_frame, text="Amount", font=("Arial", 12, "bold"), fg="white", bg="purple").grid(row=6, column=0, sticky="w")
    amount_entry = tk.Entry(form_frame, font=("Arial", 12), width=20, bg="lightyellow")
    amount_entry.grid(row=7, column=0, pady=5)
    
    # Button Frame (Insert & Next Side by Side)
    button_frame = tk.Frame(form_frame, bg="purple")
    button_frame.grid(row=8, column=0, pady=10, columnspan=2)
    
    tk.Button(button_frame, text="Insert", font=("Arial", 12, "bold"), bg="lightyellow", command=insert_data).pack(side=tk.LEFT, padx=5)
    tk.Button(button_frame, text="Next", font=("Arial", 12, "bold"), bg="lightyellow", command=next_day).pack(side=tk.LEFT, padx=5)
    
    # Table Frame
    table_frame = tk.Frame(root, bg="lightgray", bd=2)
    table_frame.place(x=250, y=50, width=600, height=300)
    
    # Table Header and Treeview
    columns = ("Date", "Category", "Item", "Amount")
    tree = ttk.Treeview(table_frame, columns=columns, show="headings")
    
    for col in columns:
        tree.heading(col, text=col)  # Bold headers
        tree.column(col, width=140, anchor="center")  # Center align data
    
    tree.pack(expand=True, fill="both")
    
    # Remaining & Total Section
    footer_frame = tk.Frame(root, bg="lightyellow", padx=10, pady=5)
    footer_frame.place(x=250, y=360, width=600)
    
    tk.Label(footer_frame, text="Remaining:\t\t", font=("Arial", 12, "bold"), bg="lightyellow").grid(row=0, column=0, sticky="w")
    
    # Total Amount Label (Updated Dynamically)
    total_label = tk.Label(footer_frame, text="Total: 0.00", font=("Arial", 12, "bold"), bg="lightyellow")
    total_label.grid(row=0, column=1, sticky="e")

    root.geometry("880x450")
    root.mainloop()

create_gui()
