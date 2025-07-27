import customtkinter as ctk
from tkinter import messagebox, simpledialog
import os
from datetime import datetime
from PIL import Image, ImageTk # Keep this if you plan to add images later, otherwise it can be removed
import threading # Keep this if you plan to use threading later, otherwise it can be removed

# Set appearance mode and color theme
ctk.set_appearance_mode("dark")  # Modes: "System" (standard), "Dark", "Light"
ctk.set_default_color_theme("blue")  # Themes: "blue" (standard), "green", "dark-blue"

# --- File Paths ---
ITEMS_FILE = "DATA.txt"
CUSTOMERS_FILE = "customerData.txt"

# --- Helper Functions for Data Handling ---
def load_items():
    """Loads items from DATA.txt. Format: code#name#price#quantity"""
    if not os.path.exists(ITEMS_FILE):
        return []
    items = []
    with open(ITEMS_FILE, "r") as f:
        for line in f:
            line = line.strip()
            if line:
                data = line.split("#")
                if len(data) == 4:
                    items.append(data)
                elif len(data) == 3:
                    # Old format without quantity, add a default quantity '0'
                    items.append(data + ['0'])
    return items

def save_items(items):
    """Saves items back to DATA.txt."""
    with open(ITEMS_FILE, "w") as f:
        for item in items:
            f.write("#".join(map(str, item)) + "\n")

def load_customers():
    """Loads customer data from customerData.txt. Format: Name ---- reg on: Date"""
    if not os.path.exists(CUSTOMERS_FILE):
        return []
    customers = []
    with open(CUSTOMERS_FILE, "r") as f:
        for line in f:
            line = line.strip()
            if line:
                customers.append(line)
    return customers

def save_customers(customers):
    """Saves customer data back to customerData.txt."""
    with open(CUSTOMERS_FILE, "w") as f:
        for customer_line in customers:
            f.write(customer_line + "\n")

class ModernInventoryApp:
    def __init__(self):
        self.root = ctk.CTk()
        self.root.geometry("1000x700")
        self.root.title("🏪 Advanced Inventory Management System")
        self.root.resizable(True, True)
        
        # Configure grid weight for main window
        self.root.grid_columnconfigure(0, weight=1)
        self.root.grid_rowconfigure(0, weight=1)
        
        self.setup_ui()
        
    def setup_ui(self):
        """Setup the main user interface"""
        # Main container frame
        main_frame = ctk.CTkFrame(self.root, corner_radius=15)
        main_frame.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")
        main_frame.grid_columnconfigure(0, weight=1)
        main_frame.grid_rowconfigure(1, weight=1) # Allow button frame to expand
        
        # Header section
        self.setup_header(main_frame)
        
        # Button container grid
        self.setup_buttons(main_frame)
        
        # Status bar at the bottom
        self.setup_status_bar(main_frame)
        
    def setup_header(self, parent):
        """Setup the header section with title and subtitle"""
        header_frame = ctk.CTkFrame(parent, height=100, corner_radius=10, fg_color="transparent")
        header_frame.grid(row=0, column=0, padx=20, pady=(20, 10), sticky="ew")
        header_frame.grid_columnconfigure(0, weight=1)
        
        # Main title label
        title_label = ctk.CTkLabel(
            header_frame, 
            text="🏪 Advanced Inventory Management", 
            font=ctk.CTkFont(size=32, weight="bold")
        )
        title_label.grid(row=0, column=0, pady=(10, 5))
        
        # Subtitle label
        subtitle_label = ctk.CTkLabel(
            header_frame, 
            text="Streamline your inventory operations with a modern interface",
            font=ctk.CTkFont(size=16),
            text_color=("gray60", "gray40")
        )
        subtitle_label.grid(row=1, column=0, pady=(0, 10))
        
    def setup_buttons(self, parent):
        """Setup the main button grid for actions"""
        button_frame = ctk.CTkFrame(parent, corner_radius=10)
        button_frame.grid(row=1, column=0, padx=20, pady=10, sticky="nsew")
        # Configure columns and rows to expand evenly
        button_frame.grid_columnconfigure((0, 1, 2), weight=1)
        button_frame.grid_rowconfigure((0, 1, 2), weight=1)
        
        # Button configurations: (text, command, row, column, color)
        buttons = [
            ("➕ Add New Item", self.add_item_gui, 0, 0, "#1f538d"), # Blue
            ("🗑️ Remove Item", self.remove_item_gui, 0, 1, "#d32f2f"), # Red
            ("✏️ Update Item", self.update_item_gui, 0, 2, "#f57c00"), # Orange
            ("🔍 Search Items", self.search_items_gui, 1, 0, "#388e3c"), # Green
            ("🧾 Create Bill", self.create_bill_gui, 1, 1, "#7b1fa2"), # Purple
            ("👤 Remove Customer", self.remove_customer_gui, 1, 2, "#c2185b"), # Pink/Red
            ("🚪 Exit Application", self.exit_application, 2, 1, "#424242") # Dark Gray
        ]
        
        for text, command, row, col, color in buttons:
            btn = ctk.CTkButton(
                button_frame,
                text=text,
                command=command,
                font=ctk.CTkFont(size=16, weight="bold"),
                height=80, # Fixed height for uniform buttons
                corner_radius=10,
                hover_color=self.lighten_color(color), # Lighter color on hover
                fg_color=color # Background color
            )
            btn.grid(row=row, column=col, padx=15, pady=15, sticky="nsew") # Pad and make sticky
    
    def setup_status_bar(self, parent):
        """Setup the status bar at the bottom of the main window"""
        self.status_var = ctk.StringVar(value="Ready") # Variable to hold status message
        status_frame = ctk.CTkFrame(parent, height=40, corner_radius=10)
        status_frame.grid(row=2, column=0, padx=20, pady=(10, 20), sticky="ew")
        status_frame.grid_columnconfigure(0, weight=1)
        
        status_label = ctk.CTkLabel(
            status_frame, 
            textvariable=self.status_var,
            font=ctk.CTkFont(size=12)
        )
        status_label.grid(row=0, column=0, padx=10, pady=10)
    
    def lighten_color(self, color):
        """Helper function to create a slightly lighter version of a given hex color for hover effects."""
        # This is a simplified approach. For more robust color manipulation,
        # consider a dedicated color library or more complex logic.
        color_map = {
            "#1f538d": "#2e6db0",
            "#d32f2f": "#e57373",
            "#f57c00": "#ff9800",
            "#388e3c": "#4caf50",
            "#7b1fa2": "#9c27b0",
            "#c2185b": "#e91e63",
            "#424242": "#616161"
        }
        return color_map.get(color, color) # Return lighter color if mapped, else original

    def update_status(self, message):
        """Updates the status bar message and clears it after 3 seconds."""
        self.status_var.set(message)
        self.root.after(3000, lambda: self.status_var.set("Ready")) # Clear after 3 seconds
    
    def show_success_message(self, title, message):
        """Displays a success message box and updates the status bar."""
        messagebox.showinfo(title, message)
        self.update_status(f"✅ {message}")
    
    def show_error_message(self, title, message):
        """Displays an error message box and updates the status bar."""
        messagebox.showerror(title, message)
        self.update_status(f"❌ {message}")

    def add_item_gui(self):
        """Handles adding a new item through a custom dialog."""
        dialog = ctk.CTkToplevel(self.root)
        dialog.geometry("400x500")
        dialog.title("Add New Item")
        dialog.transient(self.root) # Make dialog dependent on root window
        dialog.grab_set() # Make dialog modal
        
        # Center the dialog relative to the screen
        dialog.update_idletasks() # Ensure window dimensions are calculated
        screen_width = dialog.winfo_screenwidth()
        screen_height = dialog.winfo_screenheight()
        window_width = dialog.winfo_width()
        window_height = dialog.winfo_height()
        x = (screen_width // 2) - (window_width // 2)
        y = (screen_height // 2) - (window_height // 2)
        dialog.geometry(f"+{x}+{y}")
        
        # Main frame for padding and structure
        main_frame = ctk.CTkFrame(dialog, corner_radius=15)
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Dialog title
        title_label = ctk.CTkLabel(main_frame, text="Add New Item", font=ctk.CTkFont(size=24, weight="bold"))
        title_label.pack(pady=(20, 30))
        
        # Entry fields for item details
        entries = {}
        fields = [
            ("Item Code", "number"),
            ("Item Name", "text"),
            ("Item Price", "decimal"),
            ("Quantity", "number")
        ]
        
        for field_name, field_type in fields:
            label = ctk.CTkLabel(main_frame, text=field_name, font=ctk.CTkFont(size=14, weight="bold"))
            label.pack(anchor="w", padx=20, pady=(10, 5))
            
            entry = ctk.CTkEntry(main_frame, height=40, font=ctk.CTkFont(size=14))
            entry.pack(fill="x", padx=20, pady=(0, 10))
            entries[field_name.lower().replace(" ", "_")] = entry
        
        def submit_item():
            """Submits the new item data after validation."""
            try:
                item_code = int(entries["item_code"].get())
                item_name = entries["item_name"].get().strip()
                item_price = float(entries["item_price"].get())
                item_quantity = int(entries["quantity"].get())
                
                if not item_name:
                    raise ValueError("Item name cannot be empty.")
                if item_code <= 0 or item_price < 0 or item_quantity < 0:
                    raise ValueError("Code, price, and quantity must be non-negative.")
                
                items = load_items()
                
                # Check for existing item code
                for item in items:
                    if int(item[0]) == item_code:
                        self.show_error_message("Error", f"Item Code {item_code} already exists.")
                        return
                
                # Add new item to list and save
                items.append([str(item_code), item_name, str(item_price), str(item_quantity)])
                save_items(items)
                
                self.show_success_message("Success", f"Item '{item_name}' (Code: {item_code}) added successfully.")
                dialog.destroy() # Close dialog on success
                
            except ValueError as e:
                self.show_error_message("Input Error", f"Invalid input: {str(e)}")
            except Exception as e:
                self.show_error_message("Error", f"An unexpected error occurred: {e}")
        
        # Buttons for submit and cancel
        button_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        button_frame.pack(fill="x", padx=20, pady=20)
        # Configure grid for two columns, both expanding
        button_frame.grid_columnconfigure((0, 1), weight=1) 

        cancel_btn = ctk.CTkButton(
            button_frame, text="Cancel", 
            command=dialog.destroy,
            fg_color="gray", hover_color="darkgray"
        )
        # Use grid for button placement, sticky="ew" to expand horizontally
        cancel_btn.grid(row=0, column=0, padx=(0, 10), sticky="ew") 

        submit_btn = ctk.CTkButton(
            button_frame, text="Add Item", 
            command=submit_item,
            fg_color="#1f538d"
        )
        # Use grid for button placement, sticky="ew" to expand horizontally
        submit_btn.grid(row=0, column=1, sticky="ew") 

    def remove_item_gui(self):
        """Handles removing an item by its code."""
        dialog = ctk.CTkInputDialog(text="Enter item code to remove:", title="Remove Item")
        item_code_str = dialog.get_input()
        
        if not item_code_str: # User cancelled or entered nothing
            return
        
        try:
            item_code_to_remove = int(item_code_str)
        except ValueError:
            self.show_error_message("Input Error", "Item code must be an integer.")
            return
        
        items = load_items()
        removed_item_details = None
        updated_items = []
        
        for item in items:
            try:
                if int(item[0]) == item_code_to_remove:
                    removed_item_details = item
                else:
                    updated_items.append(item)
            except ValueError:
                # If an item in the file has an invalid code, keep it in the list
                updated_items.append(item)
        
        if removed_item_details:
            save_items(updated_items)
            self.show_success_message(
                "Success",
                f"Item: '{removed_item_details[1]}' (Code: {removed_item_details[0]}) has been successfully removed."
            )
        else:
            self.show_error_message("Error", f"Item with code {item_code_to_remove} not found.")

    def update_item_gui(self):
        """Handles updating details of an existing item."""
        def submit_update_dialog(item_code_str):
            try:
                item_code_to_update = int(item_code_str)
            except ValueError:
                self.show_error_message("Input Error", "Item Code must be an integer.")
                return

            items = load_items()
            item_found = False
            target_item_index = -1

            for i, item in enumerate(items):
                if int(item[0]) == item_code_to_update:
                    item_found = True
                    target_item_index = i
                    break
            
            if not item_found:
                self.show_error_message("Error", f"Item with code {item_code_to_update} not found.")
                return

            # Found item, now open a new dialog for specific updates
            update_dialog = ctk.CTkToplevel(self.root)
            update_dialog.geometry("400x550")
            update_dialog.title(f"Update Item: {items[target_item_index][1]}")
            update_dialog.transient(self.root)
            update_dialog.grab_set()

            # Center the dialog relative to the screen
            update_dialog.update_idletasks()
            screen_width = update_dialog.winfo_screenwidth()
            screen_height = update_dialog.winfo_screenheight()
            window_width = update_dialog.winfo_width()
            window_height = update_dialog.winfo_height()
            x = (screen_width // 2) - (window_width // 2)
            y = (screen_height // 2) - (window_height // 2)
            update_dialog.geometry(f"+{x}+{y}")

            update_frame = ctk.CTkFrame(update_dialog, corner_radius=15)
            update_frame.pack(fill="both", expand=True, padx=20, pady=20)

            ctk.CTkLabel(update_frame, text=f"Updating Item: {items[target_item_index][1]} (Code: {items[target_item_index][0]})",
                         font=ctk.CTkFont(size=18, weight="bold")).pack(pady=(10, 20))

            # Current values
            current_name = items[target_item_index][1]
            current_price = items[target_item_index][2]
            current_qty = items[target_item_index][3]

            ctk.CTkLabel(update_frame, text=f"Current Name: {current_name}", font=ctk.CTkFont(size=12)).pack(anchor="w", padx=10, pady=2)
            name_entry = ctk.CTkEntry(update_frame, placeholder_text="New Name (leave blank to keep current)", height=35, font=ctk.CTkFont(size=14))
            name_entry.pack(fill="x", padx=10, pady=(0, 10))

            ctk.CTkLabel(update_frame, text=f"Current Price: ${current_price}", font=ctk.CTkFont(size=12)).pack(anchor="w", padx=10, pady=2)
            price_entry = ctk.CTkEntry(update_frame, placeholder_text="New Price (leave blank to keep current)", height=35, font=ctk.CTkFont(size=14))
            price_entry.pack(fill="x", padx=10, pady=(0, 10))

            ctk.CTkLabel(update_frame, text=f"Current Quantity: {current_qty}", font=ctk.CTkFont(size=12)).pack(anchor="w", padx=10, pady=2)
            qty_entry = ctk.CTkEntry(update_frame, placeholder_text="New Quantity (leave blank to keep current)", height=35, font=ctk.CTkFont(size=14))
            qty_entry.pack(fill="x", padx=10, pady=(0, 20))

            def perform_update():
                updated_name = name_entry.get().strip()
                updated_price_str = price_entry.get().strip()
                updated_qty_str = qty_entry.get().strip()

                changes_made = False

                if updated_name:
                    items[target_item_index][1] = updated_name
                    changes_made = True
                
                if updated_price_str:
                    try:
                        updated_price = float(updated_price_str)
                        if updated_price < 0:
                            self.show_error_message("Input Error", "Price cannot be negative.")
                            return
                        items[target_item_index][2] = str(updated_price)
                        changes_made = True
                    except ValueError:
                        self.show_error_message("Input Error", "New Price must be a number.")
                        return
                
                if updated_qty_str:
                    try:
                        updated_qty = int(updated_qty_str)
                        if updated_qty < 0:
                            self.show_error_message("Input Error", "Quantity cannot be negative.")
                            return
                        items[target_item_index][3] = str(updated_qty)
                        changes_made = True
                    except ValueError:
                        self.show_error_message("Input Error", "New Quantity must be an integer.")
                        return
                
                if changes_made:
                    save_items(items)
                    self.show_success_message("Success", f"Item '{current_name}' details updated successfully.")
                else:
                    self.show_error_message("No Changes", "No changes were made to the item.")
                
                update_dialog.destroy()

            ctk.CTkButton(update_frame, text="Apply Changes", command=perform_update,
                          fg_color="#388e3c", hover_color="#4caf50").pack(pady=10)
            ctk.CTkButton(update_frame, text="Cancel", command=update_dialog.destroy,
                          fg_color="gray", hover_color="darkgray").pack(pady=5)

        # Initial dialog to get item code
        item_code_input_dialog = ctk.CTkInputDialog(text="Enter item code to update:", title="Update Item")
        item_code_for_update = item_code_input_dialog.get_input()
        
        if item_code_for_update:
            submit_update_dialog(item_code_for_update)


    def search_items_gui(self):
        """Opens a dialog for searching and viewing items."""
        dialog = ctk.CTkToplevel(self.root)
        dialog.geometry("600x500")
        dialog.title("Search & View Items")
        dialog.transient(self.root)
        dialog.grab_set()
        
        # Center the dialog relative to the screen
        dialog.update_idletasks()
        screen_width = dialog.winfo_screenwidth()
        screen_height = dialog.winfo_screenheight()
        window_width = dialog.winfo_width()
        window_height = dialog.winfo_height()
        x = (screen_width // 2) - (window_width // 2)
        y = (screen_height // 2) - (window_height // 2)
        dialog.geometry(f"+{x}+{y}")

        main_frame = ctk.CTkFrame(dialog, corner_radius=15)
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        title_label = ctk.CTkLabel(main_frame, text="Search & View Items", font=ctk.CTkFont(size=24, weight="bold"))
        title_label.pack(pady=(20, 30))
        
        # Search options buttons
        option_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        option_frame.pack(fill="x", padx=20, pady=10)
        
        price_range_btn = ctk.CTkButton(
            option_frame, text="Search by Price Range",
            command=lambda: self.search_by_price_range(results_text),
            fg_color="#1f538d", hover_color="#2e6db0"
        )
        price_range_btn.pack(side="left", expand=True, padx=(0, 10))
        
        view_all_btn = ctk.CTkButton(
            option_frame, text="View All Items",
            command=lambda: self.view_all_items(results_text),
            fg_color="#388e3c", hover_color="#4caf50"
        )
        view_all_btn.pack(side="right", expand=True)
        
        # Textbox to display results
        results_text = ctk.CTkTextbox(main_frame, height=300, font=ctk.CTkFont(size=12))
        results_text.pack(fill="both", expand=True, padx=20, pady=20)
        
        close_btn = ctk.CTkButton(main_frame, text="Close", command=dialog.destroy,
                                  fg_color="gray", hover_color="darkgray")
        close_btn.pack(pady=(0, 20))

    def search_by_price_range(self, results_widget):
        """Performs search by price range and displays results in the provided widget."""
        try:
            start_dialog = ctk.CTkInputDialog(text="Enter start price:", title="Price Range Start")
            start_price_str = start_dialog.get_input()
            if start_price_str is None: return # User cancelled
            start_price = float(start_price_str)
            
            end_dialog = ctk.CTkInputDialog(text="Enter end price:", title="Price Range End") 
            end_price_str = end_dialog.get_input()
            if end_price_str is None: return # User cancelled
            end_price = float(end_price_str)
            
            items = load_items()
            results = []
            
            for item in items:
                try:
                    item_price = float(item[2])
                    if start_price <= item_price <= end_price:
                        results.append(f"Code: {item[0]} | Name: {item[1]} | Price: ${item[2]} | Qty: {item[3]}")
                except ValueError:
                    continue # Skip items with invalid price data
            
            results_widget.delete("0.0", "end") # Clear previous results
            if results:
                results_widget.insert("0.0", "\n".join(results))
            else:
                results_widget.insert("0.0", "No items found in the specified price range.")
                
        except (ValueError, TypeError):
            self.show_error_message("Input Error", "Please enter valid numeric prices.")

    def view_all_items(self, results_widget):
        """Displays all items in the provided widget."""
        items = load_items()
        results_widget.delete("0.0", "end") # Clear previous results
        
        if not items:
            results_widget.insert("0.0", "No items found in inventory.")
            return
        
        results = []
        for item in items:
            results.append(f"Code: {item[0]} | Name: {item[1]} | Price: ${item[2]} | Qty: {item[3]}")
        
        results_widget.insert("0.0", "\n".join(results))

    def create_bill_gui(self):
        """Handles the creation of a customer bill, including item selection and stock update."""
        customer_name_dialog = ctk.CTkInputDialog(text="Enter customer name:", title="Create Bill")
        customer_name = customer_name_dialog.get_input()
        if not customer_name:
            return # User cancelled

        # Ask to register customer
        register_status = messagebox.askyesno("Customer Registration", f"Do you want to register '{customer_name}' as a customer?")
        if register_status:
            customers = load_customers()
            now = datetime.now()
            date_time = now.strftime("%m/%d/%Y, %H:%M:%S")
            customers.append(f"{customer_name} ---- reg on: {date_time}")
            save_customers(customers)
            self.show_success_message("Customer Registered", f"Customer '{customer_name}' registered successfully.")

        bill_file_name = f"BILL-{customer_name.replace(' ', '_')}.txt"
        bill_items_list = []
        total_bill = 0.0

        try:
            # Open bill file in append mode, create if not exists
            with open(bill_file_name, "a+") as bill_file:
                now = datetime.now()
                date_time = now.strftime("%m/%d/%Y, %H:%M:%S")
                bill_file.write(f"--- Bill for {customer_name} ---\n")
                bill_file.write(f"Date: {date_time}\n\n")

                items_in_stock = load_items() # Load current stock

                while True:
                    item_code_str_dialog = ctk.CTkInputDialog(text="Enter item code (or leave empty to finish billing):", title="Billing - Add Item")
                    item_code_str = item_code_str_dialog.get_input()
                    if not item_code_str: # User finished adding items
                        break

                    try:
                        item_code = int(item_code_str)
                    except ValueError:
                        self.show_error_message("Input Error", "Item code must be an integer.")
                        continue

                    found_item = None
                    item_index = -1
                    for i, item in enumerate(items_in_stock):
                        try:
                            if int(item[0]) == item_code:
                                found_item = item
                                item_index = i
                                break
                        except ValueError:
                            continue # Skip invalid item codes in file

                    if not found_item:
                        self.show_error_message("Error", "Item not found in stock.")
                        continue

                    try:
                        qty_str_dialog = ctk.CTkInputDialog(text=f"Enter quantity for {found_item[1]} (Available: {found_item[3]}):", title="Billing - Quantity")
                        qty_str = qty_str_dialog.get_input()
                        if qty_str is None: continue # User cancelled quantity input
                        qty = int(qty_str)
                        if qty <= 0:
                            self.show_error_message("Input Error", "Quantity must be a positive integer.")
                            continue
                    except ValueError:
                        self.show_error_message("Input Error", "Invalid quantity.")
                        continue

                    available_qty = int(found_item[3])
                    if qty > available_qty:
                        self.show_error_message("Stock Error", f"Not enough stock for {found_item[1]}. Available: {available_qty}")
                        continue
                    
                    item_price = float(found_item[2])
                    item_subtotal = item_price * qty
                    total_bill += item_subtotal
                    
                    bill_line = f"{found_item[1]} ({found_item[0]}) - ${found_item[2]} x {qty} = ${item_subtotal:.2f}"
                    bill_items_list.append(bill_line)
                    bill_file.write(bill_line + "\n")
                    
                    # Update stock in memory
                    items_in_stock[item_index][3] = str(available_qty - qty) 
                    
                    self.show_success_message("Item Added to Bill", f"{found_item[1]} x{qty} added to bill.")
                
                bill_file.write(f"\nTotal Bill: ${total_bill:.2f}\n")
            
            self.show_success_message("Bill Created", f"Your Total bill has successfully printed to {bill_file_name}")
            save_items(items_in_stock) # Save updated stock quantities back to DATA.txt

        except Exception as e:
            self.show_error_message("Billing Error", f"An error occurred during billing: {e}")

    def remove_customer_gui(self):
        """Handles removing a customer from the customer data file."""
        customer_name_to_remove_dialog = ctk.CTkInputDialog(text="Enter the customer name you want to remove:", title="Remove Customer")
        customer_name_to_remove = customer_name_to_remove_dialog.get_input()
        if not customer_name_to_remove:
            return # User cancelled

        customers = load_customers()
        updated_customers = []
        removed_status = False
        
        for line in customers:
            data = line.strip().split("---- reg on:")
            # Check if the name part of the line matches the customer to remove
            if data and data[0].strip().lower() == customer_name_to_remove.strip().lower():
                removed_status = True
            else:
                updated_customers.append(line)

        if removed_status:
            save_customers(updated_customers)
            self.show_success_message("Success", f"Customer: '{customer_name_to_remove}' has been successfully removed from the customer data list.")
        else:
            self.show_error_message("Error", f"Customer '{customer_name_to_remove}' not found.")

    def exit_application(self):
        """Exits the application after confirmation."""
        if messagebox.askyesno("Exit Application", "Are you sure you want to exit?"):
            self.root.quit()

    def run(self):
        """Starts the main application loop."""
        self.update_status("Application started successfully")
        self.root.mainloop()

def main():
    """Main function to run the application."""
    app = ModernInventoryApp()
    app.run()

if __name__ == "__main__":
    main()
