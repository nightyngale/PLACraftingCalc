import tkinter as tk
from tkinter import ttk
import recipes
import prices

# Creating the root window
root = tk.Tk()
root.title("PLA Crafting Calculator")
root.iconbitmap("./assets/pokeballlegends.ico")
root.geometry("550x350+300+300")
root.resizable(False, False)

# Labelframe for initial input
lf1 = ttk.Labelframe(root, text="Options", borderwidth=1, padding=5, width=40)
lf1.grid(row=0, column=0, rowspan=2, columnspan=2, padx=15, pady=5, sticky=tk.EW)

# Recipe select label
recipe_label = ttk.Label(lf1, text="Recipe:", justify="left")
recipe_label.grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)

# Recipe combobox
recipe_options = list(recipes.rec.keys())
selected_recipe = tk.StringVar(root)
selected_recipe.set("Choose a recipe")
recipe_menu = ttk.Combobox(lf1, textvariable=selected_recipe, values=recipe_options, state="readonly")
recipe_menu.grid(row=0, column=1, padx=5, pady=5, sticky=tk.EW)

# Label and entry for quantity
qty_label = ttk.Label(lf1, text="Quantity:", justify="left")
qty_label.grid(row=1, column=0, padx=5, pady=5, sticky=tk.W)
qty_entry = ttk.Entry(lf1, width=10, justify="right")
qty_entry.grid(row=1, column=1, padx=5, pady=5, sticky=tk.EW)

# Labelframe to input quantity
lf2 = ttk.Labelframe(root, text="Input", borderwidth=1, padding=5, width = 40)
lf2.grid(row=2, column=0, rowspan=6, columnspan=2, padx=15, pady=5, sticky=tk.EW)

# List to hold entries created when recipe is selected
qty_entries = []

# Function to handle recipe selection
def recipe_selected(event):
    # First, clear lf2 and qty_entries if they are not currently empty
    for widget in lf2.winfo_children():
        widget.destroy()
    
    qty_entries.clear()

    # Place instruction label
    infolabel = ttk.Label(lf2, text="How many of these materials do you have?", justify="center", wraplength=200)
    infolabel.grid(row=0, column=0, rowspan=2, columnspan=2, padx=5, pady=3, sticky=tk.EW)

    # Get currently selected recipe and fetch matching dictionary from recipes.py
    current_recipe = selected_recipe.get()
    recipe_dict = recipes.rec.get(current_recipe)

    row = 2
    for key in recipe_dict:
        label = ttk.Label(lf2, text=key, justify="left")
        label.grid(row=row, column=0, padx=5, pady=3, sticky=tk.W)

        entry = ttk.Entry(lf2, justify="right", width=10)
        entry.grid(row=row, column=1, padx=5, pady=3, sticky=tk.E)

        qty_entries.append(entry)

        row += 1

# Bind combobox to function
recipe_menu.bind("<<ComboboxSelected>>", recipe_selected)

# Labelframe for total quantity
lf3 = ttk.Labelframe(root, text="Output", borderwidth=1, padding=5)
lf3.grid(row=0, column=2, rowspan=5, columnspan=2, padx=15, pady=5, sticky=tk.EW)

# Treeview for total quantity
qty_columns = ("material", "qty", "price")
show_qty = ttk.Treeview(lf3, columns=qty_columns, show="headings", padding=5, height=10, selectmode="none")

show_qty.heading("material", text="Material")
show_qty.heading("qty", text="#")
show_qty.heading("price", text="Price")

show_qty.column("material", width=100)
show_qty.column("qty", width=50)
show_qty.column("price", width=50)

show_qty.grid(row=0, rowspan=5, column=0, columnspan=2, padx=5, pady=3, sticky=tk.EW)

# Final price
final_price = tk.StringVar(root)
final_price.set("Enter your information and press Calculate!")

price_label = ttk.Label(lf3, textvariable=final_price, justify="center")
price_label.grid(row=6, column=0, columnspan=2, padx=5, pady=3, sticky=tk.EW)

def calc():
    # First clear show_qty if there are any items inside it
    for child in show_qty.get_children():
        show_qty.delete(child)
    
    current_recipe = selected_recipe.get()
    recipe_dict = recipes.rec.get(current_recipe)

    input_list = []
    input_qty = int(qty_entry.get())

    price_list = []

    for entry in qty_entries:
        input_list.append(int(entry.get()))
    
    index = 0
    for key in recipe_dict:
        material = key
        qty = recipe_dict[key] * input_qty - input_list[index]

        if qty < 0:
            qty = 0

        if prices.price.get(key) == None:
            price = 0
        else:
            price = prices.price.get(key) * qty
        
        price_list.append(price)

        show_qty.insert("", tk.END, values=(material, qty, price))
        
        index += 1
    
    total_price = sum(price_list)

    final_price.set(f"This will cost ${total_price:,}.")

# Calculate button
calc_button = ttk.Button(root, text="Calculate", width=15, command=calc)
calc_button.grid(row=15, column=0, columnspan=4, padx=5, pady=5)

root.mainloop()