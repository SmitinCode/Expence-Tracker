import tkinter as tk
from tkinter import ttk, messagebox
import pandas as pd
import matplotlib.pyplot as plt

# Global variables
months = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
current_month = pd.Timestamp.now().strftime('%B')  # Get current month
budgets = {current_month: 0}  # Initial budget for the current month
expenses_filename = 'expenses_aaa.csv'

# Check if expenses CSV file exists, if not, create it
try:
    expenses_data = pd.read_csv(expenses_filename)
except FileNotFoundError:
    expenses_data = pd.DataFrame(columns=['Month', 'Category', 'Item', 'Quantity', 'Cost Per Unit', 'Total'])
    expenses_data.to_csv(expenses_filename, index=False)

def add_item():
    global budgets
    item = item_txt.get()
    quantity = qty_txt.get()
    cost = cost_txt.get()
    category = category_var.get()
    total = int(quantity) * int(cost)
    
    selected_month = month_var.get()
    
    # Update budget for the selected month if it's not set
    if selected_month not in budgets or budgets[selected_month] == 0:
        set_budget()
        if budgets[selected_month] == 0:
            return
    
    # Check if adding this item exceeds the budget
    total_expenses_month = total_expenses(selected_month)
    if total > (budgets[selected_month] - total_expenses_month):
        messagebox.showwarning("Budget Alert", f"Adding this item will exceed the budget of ${budgets[selected_month]}.")
        return
    
    esp_lbl.insert("", "end", values=(selected_month, category, item, quantity, cost, total))
    expenses_data.loc[len(expenses_data)] = [selected_month, category, item, quantity, cost, total]
    expenses_data.to_csv(expenses_filename, index=False)  # Save data to CSV

    # Dynamically adjust the height of the Treeview widget
    new_height = min(len(expenses_data), 5)  # Set maximum height to 15 rows
    esp_lbl.configure(height=new_height)


def total_expenses(month):
    return expenses_data[expenses_data['Month'] == month]['Total'].sum()

def set_budget():
    selected_month = month_var.get()
    try:
        budget = float(budget_entry.get())
        budgets[selected_month] = budget
        messagebox.showinfo("Budget Set", f"Budget set to ${budget} for {selected_month}.")
    except ValueError:
        messagebox.showerror("Invalid Budget", "Please enter a valid budget.")

def update_budget(event):
    selected_month = month_var.get()
    budget_entry.delete(0, 'end')
    budget_entry.insert(0, budgets[selected_month])

def delete():
    global expenses_data
    selected_item = esp_lbl.selection()[0]
    index = int(selected_item[1:]) - 1
    expenses_data.drop(index, inplace=True)
    esp_lbl.delete(selected_item)
    expenses_data.to_csv(expenses_filename, index=False)  # Save data to CSV after deletion

def analyze_data():
    # Get the selected month
    selected_month = month_var.get()
    
    # Filter expenses data for the selected month
    selected_month_data = expenses_data[expenses_data['Month'] == selected_month]
    
    if selected_month_data.empty:
        messagebox.showwarning("No Data", f"No expenses data available for {selected_month}.")
        return
    
    # Aggregate expenses by category
    category_totals = selected_month_data.groupby('Category')['Total'].sum()
    
    if category_totals.empty:
        messagebox.showwarning("No Data", f"No expenses data available for categories in {selected_month}.")
        return
    
    # Plot pie chart for the selected month and category
    plt.figure(figsize=(8, 6))
    labels = category_totals.index
    sizes = category_totals.values
    plt.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=140)
    plt.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle
    plt.title(f'{selected_month} Category Expenses')
    plt.show()

root = tk.Tk()
root.geometry('1000x450')
root.configure(bg='#003366')
root.title('Expense Tracker')

# Frame for the left side
left_frame = tk.Frame(root, bg='#003366')
left_frame.pack(side=tk.LEFT, padx=20, pady=20, fill=tk.Y)

title_lbl = tk.Label(left_frame, text="Expense Tracker", bg='#003366', fg='white', font='Helvetica 20')
title_lbl.pack()

month_var = tk.StringVar(root, value=current_month)
month_lbl = tk.Label(left_frame, text="Select Month:", font='Helvetica 16', bg='#003366', fg='white')
month_lbl.pack(pady=(20, 5))

month_menu = ttk.Combobox(left_frame, textvariable=month_var, values=months, font='Helvetica 16')
month_menu.bind("<<ComboboxSelected>>", update_budget)
month_menu.pack()

budget_lbl = tk.Label(left_frame, text="Set Budget:", font='Helvetica 16', bg='#003366', fg='white')
budget_lbl.pack(pady=(20, 5))

budget_entry = tk.Entry(left_frame, font='Helvetica 16')
budget_entry.pack()

set_budget_btn = tk.Button(left_frame, text="Set", bg='black', fg='white', font='Helvetica 16', command=set_budget)
set_budget_btn.pack(pady=5)

item_lbl = tk.Label(left_frame, text="Item", bg='#003366', fg='white', font='Helvetica 16')
item_lbl.pack(pady=(20, 5))
item_txt = tk.Entry(left_frame, font='Helvetica 16')
item_txt.pack()

qty_lbl = tk.Label(left_frame, text="Quantity", bg='#003366', fg='white', font='Helvetica 16')
qty_lbl.pack(pady=(20, 5))
qty_txt = tk.Entry(left_frame, font='Helvetica 16')
qty_txt.pack()

cost_lbl = tk.Label(left_frame, text="Cost Per Unit", bg='#003366', fg='white', font='Helvetica 16')
cost_lbl.pack(pady=(20, 5))
cost_txt = tk.Entry(left_frame, font='Helvetica 16')
cost_txt.pack()

category_lbl = tk.Label(left_frame, text="Category", bg='#003366', fg='white', font='Helvetica 16')
category_lbl.pack(pady=(20, 5))
category_var = tk.StringVar(root, value="Food")
category_menu = ttk.Combobox(left_frame, textvariable=category_var, values=["Food", "Transport", "Utilities", "Entertainment"], font='Helvetica 16')
category_menu.pack()

add_btn = tk.Button(left_frame, text="Add Item", bg='black', fg='white', font='Helvetica 16', command=add_item)
add_btn.pack(pady=20)



# Frame for the right side
right_frame = ttk.Frame(root)
right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

display_lbl = tk.Label(right_frame, text="Expenses", bg='#003366', fg='white', font='Helvetica 16')
display_lbl.pack(pady=(30, 5))

esp_lbl = ttk.Treeview(right_frame, columns=('Month', 'Category', 'Item', 'Quantity', 'Cost Per Unit', 'Total'), show='headings', height=1)
esp_lbl.pack(pady=5, padx=20)

esp_lbl.column('Month', width=100, anchor='center')
esp_lbl.column('Category', width=100, anchor='center')
esp_lbl.column('Item', width=150, anchor='center')
esp_lbl.column('Quantity', width=100, anchor='center')
esp_lbl.column('Cost Per Unit', width=150, anchor='center')
esp_lbl.column('Total', width=100, anchor='center')

esp_lbl.heading('Month', text='Month')
esp_lbl.heading('Category', text='Category')
esp_lbl.heading('Item', text='Item')
esp_lbl.heading('Quantity', text='Quantity')  
esp_lbl.heading('Cost Per Unit', text='Cost Per Unit')
esp_lbl.heading('Total', text='Total')

# Add Buttons for delete and analyze
del_btn = tk.Button(right_frame, text="Delete", bg='black', fg='white', font='Helvetica 16', command=delete)
del_btn.pack(pady=5)

analyze_btn = tk.Button(right_frame, text="Analyze Data", bg='black', fg='white', font='Helvetica 16', command=analyze_data)
analyze_btn.pack(pady=20)

root.mainloop()
