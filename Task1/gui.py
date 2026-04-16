# gui.py
import sys
from tkinter import *
from tkinter import ttk, messagebox

from database import Database
from controller import InventoryController
from models import UserRole
from utils import Utils


class FirstRunSetup:
    """First-time setup wizard for creating admin account."""
    def __init__(self, parent, controller: InventoryController):
        self.controller = controller
        self.dialog = Toplevel(parent)
        self.dialog.title("First-Time Setup")
        self.dialog.geometry("450x350")
        self.dialog.transient(parent)
        self.dialog.grab_set()

        self.dialog.protocol("WM_DELETE_WINDOW", self.on_cancel)

        ttk.Label(self.dialog, text="Welcome to Warehouse Management System",
                  font=("Arial", 14, "bold")).pack(pady=15)
        ttk.Label(self.dialog, text="No users found. Please create an administrator account.",
                  font=("Arial", 10)).pack(pady=5)

        admin_frame = ttk.LabelFrame(self.dialog, text="Administrator Account (required)", padding=10)
        admin_frame.pack(fill=X, padx=20, pady=10)

        ttk.Label(admin_frame, text="Username:").grid(row=0, column=0, padx=5, pady=5, sticky=E)
        self.admin_user = ttk.Entry(admin_frame, width=25)
        self.admin_user.grid(row=0, column=1, padx=5, pady=5)
        self.admin_user.insert(0, "admin")

        ttk.Label(admin_frame, text="Full Name:").grid(row=1, column=0, padx=5, pady=5, sticky=E)
        self.admin_name = ttk.Entry(admin_frame, width=25)
        self.admin_name.grid(row=1, column=1, padx=5, pady=5)
        self.admin_name.insert(0, "Administrator")

        ttk.Label(admin_frame, text="Contact:").grid(row=2, column=0, padx=5, pady=5, sticky=E)
        self.admin_contact = ttk.Entry(admin_frame, width=25)
        self.admin_contact.grid(row=2, column=1, padx=5, pady=5)
        self.admin_contact.insert(0, "admin@company.com")

        ttk.Label(admin_frame, text="Password:").grid(row=3, column=0, padx=5, pady=5, sticky=E)
        self.admin_pass = ttk.Entry(admin_frame, width=25, show="*")
        self.admin_pass.grid(row=3, column=1, padx=5, pady=5)

        ttk.Label(admin_frame, text="Confirm Password:").grid(row=4, column=0, padx=5, pady=5, sticky=E)
        self.admin_pass_confirm = ttk.Entry(admin_frame, width=25, show="*")
        self.admin_pass_confirm.grid(row=4, column=1, padx=5, pady=5)

        staff_frame = ttk.LabelFrame(self.dialog, text="Staff Account (optional)", padding=10)
        staff_frame.pack(fill=X, padx=20, pady=5)

        ttk.Label(staff_frame, text="Username:").grid(row=0, column=0, padx=5, pady=5, sticky=E)
        self.staff_user = ttk.Entry(staff_frame, width=25)
        self.staff_user.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(staff_frame, text="Full Name:").grid(row=1, column=0, padx=5, pady=5, sticky=E)
        self.staff_name = ttk.Entry(staff_frame, width=25)
        self.staff_name.grid(row=1, column=1, padx=5, pady=5)

        ttk.Label(staff_frame, text="Password:").grid(row=2, column=0, padx=5, pady=5, sticky=E)
        self.staff_pass = ttk.Entry(staff_frame, width=25, show="*")
        self.staff_pass.grid(row=2, column=1, padx=5, pady=5)

        btn_frame = ttk.Frame(self.dialog)
        btn_frame.pack(pady=15)
        ttk.Button(btn_frame, text="Complete Setup", command=self.save).pack(side=LEFT, padx=5)
        ttk.Button(btn_frame, text="Cancel", command=self.on_cancel).pack(side=LEFT, padx=5)

        self.success = False

    def save(self):
        if not self.admin_user.get().strip():
            messagebox.showerror("Error", "Admin username is required.")
            return
        if not self.admin_pass.get():
            messagebox.showerror("Error", "Admin password is required.")
            return
        if self.admin_pass.get() != self.admin_pass_confirm.get():
            messagebox.showerror("Error", "Admin passwords do not match.")
            return

        ok = self.controller.create_user(
            self.admin_user.get().strip(),
            self.admin_name.get().strip() or "Admin",
            self.admin_contact.get().strip() or "",
            "admin",
            self.admin_pass.get()
        )
        if not ok:
            messagebox.showerror("Error", f"Username '{self.admin_user.get().strip()}' already exists.")
            return

        staff_user = self.staff_user.get().strip()
        if staff_user:
            if not self.staff_pass.get():
                messagebox.showerror("Error", "Staff password is required if username is provided.")
                return
            ok2 = self.controller.create_user(
                staff_user,
                self.staff_name.get().strip() or "Staff",
                "",
                "staff",
                self.staff_pass.get()
            )
            if not ok2:
                messagebox.showerror("Error", f"Staff username '{staff_user}' already exists.")
                return

        Database.insert_sample_data()

        self.success = True
        self.dialog.destroy()

    def on_cancel(self):
        self.dialog.destroy()


class WarehouseApp:
    """Main GUI application class."""
    def __init__(self):
        print("Creating main window...")
        self.root = Tk()
        self.root.title("Warehouse Management System")
        self.root.geometry("1100x700")
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)

        self.style = ttk.Style()
        self.style.theme_use("clam")

        self.main_frame = None
        self.controller = InventoryController()

        print(f"First run? {Database.is_first_run()}")
        if Database.is_first_run():
            print("Launching first-time setup...")
            setup = FirstRunSetup(self.root, self.controller)
            self.root.wait_window(setup.dialog)
            if not setup.success:
                print("Setup cancelled by user.")
                messagebox.showinfo("Setup Cancelled", "Application will now exit.")
                self.root.destroy()
                return
            print("Setup completed.")

        self.show_login()
        print("Login screen displayed.")

    def run(self):
        print("Entering main event loop...")
        self.root.mainloop()

    def on_close(self):
        print("Application closing.")
        self.root.destroy()

    def clear_frame(self):
        if self.main_frame:
            self.main_frame.destroy()

    def show_login(self):
        self.clear_frame()
        self.main_frame = ttk.Frame(self.root, padding=20)
        self.main_frame.pack(fill=BOTH, expand=True)

        ttk.Label(self.main_frame, text="Warehouse Management System", font=("Arial", 24)).pack(pady=30)

        login_frame = ttk.LabelFrame(self.main_frame, text="Login", padding=20)
        login_frame.pack(pady=20)

        ttk.Label(login_frame, text="Username:").grid(row=0, column=0, padx=5, pady=5, sticky=E)
        username_entry = ttk.Entry(login_frame, width=25)
        username_entry.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(login_frame, text="Password:").grid(row=1, column=0, padx=5, pady=5, sticky=E)
        password_entry = ttk.Entry(login_frame, width=25, show="*")
        password_entry.grid(row=1, column=1, padx=5, pady=5)

        def do_login():
            user = username_entry.get().strip()
            pwd = password_entry.get()
            if self.controller.login(user, pwd):
                self.show_main_menu()
            else:
                messagebox.showerror("Login Failed", "Invalid username or password.")

        ttk.Button(login_frame, text="Login", command=do_login).grid(row=2, column=0, columnspan=2, pady=15)

        username_entry.bind("<Return>", lambda e: do_login())
        password_entry.bind("<Return>", lambda e: do_login())
        username_entry.focus()

    def show_main_menu(self):
        self.clear_frame()
        user = self.controller.get_current_user()
        is_admin = user.get_user_role() == UserRole.ADMIN

        top_frame = ttk.Frame(self.root)
        top_frame.pack(fill=X, padx=5, pady=5)

        ttk.Label(top_frame, text=f"Welcome, {user.get_name()} ({user.get_role()})",
                  font=("Arial", 12)).pack(side=LEFT, padx=10)

        ttk.Button(top_frame, text="Logout", command=self.logout).pack(side=RIGHT, padx=5)

        notebook = ttk.Notebook(self.root)
        notebook.pack(fill=BOTH, expand=True, padx=5, pady=5)

        dash_frame = ttk.Frame(notebook)
        notebook.add(dash_frame, text="Dashboard")
        self.build_dashboard(dash_frame)

        inv_frame = ttk.Frame(notebook)
        notebook.add(inv_frame, text="Inventory")
        self.build_inventory_tab(inv_frame, is_admin)

        trans_frame = ttk.Frame(notebook)
        notebook.add(trans_frame, text="Transactions")
        self.build_transactions_tab(trans_frame)

        supp_frame = ttk.Frame(notebook)
        notebook.add(supp_frame, text="Suppliers")
        self.build_suppliers_tab(supp_frame, is_admin)

        if is_admin:
            user_frame = ttk.Frame(notebook)
            notebook.add(user_frame, text="Users")
            self.build_users_tab(user_frame)

        self.main_frame = notebook

    def logout(self):
        self.controller.logout()
        self.show_login()

    def build_dashboard(self, parent):
        summary = self.controller.get_inventory_summary()
        alerts = self.controller.get_low_stock_alerts()
        recent = self.controller.get_recent_transactions(10)

        cards_frame = ttk.Frame(parent)
        cards_frame.pack(fill=X, padx=10, pady=10)

        ttk.Label(cards_frame, text=f"Total Items: {summary['total_items']}",
                  font=("Arial", 14), relief=RIDGE, padding=10).pack(side=LEFT, padx=20)
        total_value_str = Utils.format_currency(summary['total_value'])
        ttk.Label(cards_frame, text=f"Total Value: {total_value_str}",
                  font=("Arial", 14), relief=RIDGE, padding=10).pack(side=LEFT, padx=20)
        ttk.Label(cards_frame, text=f"Low Stock Items: {summary['low_stock_count']}",
                  font=("Arial", 14), relief=RIDGE, padding=10, foreground="red").pack(side=LEFT, padx=20)

        alert_frame = ttk.LabelFrame(parent, text="Low Stock Alerts", padding=5)
        alert_frame.pack(fill=X, padx=10, pady=5)
        if alerts:
            for alert in alerts:
                ttk.Label(alert_frame, text=f"⚠ {alert}", foreground="red").pack(anchor=W)
        else:
            ttk.Label(alert_frame, text="No low stock alerts.").pack(anchor=W)

        trans_frame = ttk.LabelFrame(parent, text="Recent Transactions", padding=5)
        trans_frame.pack(fill=BOTH, expand=True, padx=10, pady=5)

        tree = ttk.Treeview(trans_frame, columns=("ID", "Type", "Item", "Qty", "User", "Date"), show="headings", height=8)
        tree.heading("ID", text="ID")
        tree.heading("Type", text="Type")
        tree.heading("Item", text="Item")
        tree.heading("Qty", text="Qty")
        tree.heading("User", text="User")
        tree.heading("Date", text="Date")
        tree.column("ID", width=150)
        tree.column("Type", width=60)
        tree.column("Item", width=200)
        tree.column("Qty", width=60)
        tree.column("User", width=120)
        tree.column("Date", width=150)

        scrollbar = ttk.Scrollbar(trans_frame, orient=VERTICAL, command=tree.yview)
        tree.configure(yscrollcommand=scrollbar.set)
        tree.pack(side=LEFT, fill=BOTH, expand=True)
        scrollbar.pack(side=RIGHT, fill=Y)

        for t in recent:
            tree.insert("", END, values=t)

    def build_inventory_tab(self, parent, is_admin):
        btn_frame = ttk.Frame(parent)
        btn_frame.pack(fill=X, padx=5, pady=5)

        if is_admin:
            ttk.Button(btn_frame, text="Add Item", command=self.add_item_dialog).pack(side=LEFT, padx=2)
            ttk.Button(btn_frame, text="Edit Item", command=self.edit_item_dialog).pack(side=LEFT, padx=2)
            ttk.Button(btn_frame, text="Delete Item", command=self.delete_item).pack(side=LEFT, padx=2)

        ttk.Button(btn_frame, text="Refresh", command=lambda: self.refresh_inventory_tree(tree)).pack(side=LEFT, padx=10)

        tree_frame = ttk.Frame(parent)
        tree_frame.pack(fill=BOTH, expand=True, padx=5, pady=5)

        tree = ttk.Treeview(tree_frame, columns=("ID", "Name", "Price", "Qty", "Min", "Type"), show="headings")
        tree.heading("ID", text="ID")
        tree.heading("Name", text="Name")
        tree.heading("Price", text="Unit Price")
        tree.heading("Qty", text="Quantity")
        tree.heading("Min", text="Min Threshold")
        tree.heading("Type", text="Type")
        tree.column("ID", width=80)
        tree.column("Name", width=200)
        tree.column("Price", width=80)
        tree.column("Qty", width=80)
        tree.column("Min", width=80)
        tree.column("Type", width=100)

        scrollbar = ttk.Scrollbar(tree_frame, orient=VERTICAL, command=tree.yview)
        tree.configure(yscrollcommand=scrollbar.set)
        tree.pack(side=LEFT, fill=BOTH, expand=True)
        scrollbar.pack(side=RIGHT, fill=Y)

        self.refresh_inventory_tree(tree)
        parent.tree = tree

    def refresh_inventory_tree(self, tree):
        for row in tree.get_children():
            tree.delete(row)
        items = self.controller.get_all_items()
        for it in items:
            tree.insert("", END, values=it)

    def add_item_dialog(self):
        dialog = Toplevel(self.root)
        dialog.title("Add New Item")
        dialog.geometry("400x350")
        dialog.transient(self.root)
        dialog.grab_set()

        ttk.Label(dialog, text="Item ID:").grid(row=0, column=0, padx=5, pady=5, sticky=E)
        id_entry = ttk.Entry(dialog)
        id_entry.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(dialog, text="Name:").grid(row=1, column=0, padx=5, pady=5, sticky=E)
        name_entry = ttk.Entry(dialog)
        name_entry.grid(row=1, column=1, padx=5, pady=5)

        ttk.Label(dialog, text="Unit Price:").grid(row=2, column=0, padx=5, pady=5, sticky=E)
        price_entry = ttk.Entry(dialog)
        price_entry.grid(row=2, column=1, padx=5, pady=5)

        ttk.Label(dialog, text="Initial Quantity:").grid(row=3, column=0, padx=5, pady=5, sticky=E)
        qty_entry = ttk.Entry(dialog)
        qty_entry.grid(row=3, column=1, padx=5, pady=5)

        ttk.Label(dialog, text="Min Threshold:").grid(row=4, column=0, padx=5, pady=5, sticky=E)
        threshold_entry = ttk.Entry(dialog)
        threshold_entry.insert(0, "10")
        threshold_entry.grid(row=4, column=1, padx=5, pady=5)

        ttk.Label(dialog, text="Type:").grid(row=5, column=0, padx=5, pady=5, sticky=E)
        type_combo = ttk.Combobox(dialog, values=["Perishable", "NonPerishable"], state="readonly")
        type_combo.grid(row=5, column=1, padx=5, pady=5)

        ttk.Label(dialog, text="Extra Info (JSON):").grid(row=6, column=0, padx=5, pady=5, sticky=E)
        extra_entry = ttk.Entry(dialog)
        extra_entry.grid(row=6, column=1, padx=5, pady=5)

        def save():
            try:
                if self.controller.add_item(
                    id_entry.get().strip(),
                    name_entry.get().strip(),
                    float(price_entry.get()),
                    int(qty_entry.get() or 0),
                    int(threshold_entry.get() or 10),
                    type_combo.get(),
                    extra_entry.get().strip() or "{}"
                ):
                    messagebox.showinfo("Success", "Item added.")
                    dialog.destroy()
                    self.refresh_inventory_tree(self.main_frame.master.tree)
                else:
                    messagebox.showerror("Error", "Item ID already exists.")
            except ValueError:
                messagebox.showerror("Error", "Invalid numeric value.")

        ttk.Button(dialog, text="Save", command=save).grid(row=7, column=0, columnspan=2, pady=15)

    def edit_item_dialog(self):
        tree = self.main_frame.master.tree
        selected = tree.selection()
        if not selected:
            messagebox.showwarning("Select Item", "Please select an item to edit.")
            return
        item_values = tree.item(selected[0])['values']
        item_id = item_values[0]

        conn = Database.get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM items WHERE item_id = ?", (item_id,))
        row = cursor.fetchone()
        conn.close()
        if not row:
            return

        dialog = Toplevel(self.root)
        dialog.title("Edit Item")
        dialog.geometry("400x300")
        dialog.transient(self.root)
        dialog.grab_set()

        ttk.Label(dialog, text="Item ID:").grid(row=0, column=0, padx=5, pady=5, sticky=E)
        id_label = ttk.Label(dialog, text=item_id)
        id_label.grid(row=0, column=1, padx=5, pady=5, sticky=W)

        ttk.Label(dialog, text="Name:").grid(row=1, column=0, padx=5, pady=5, sticky=E)
        name_entry = ttk.Entry(dialog)
        name_entry.insert(0, row[1])
        name_entry.grid(row=1, column=1, padx=5, pady=5)

        ttk.Label(dialog, text="Unit Price:").grid(row=2, column=0, padx=5, pady=5, sticky=E)
        price_entry = ttk.Entry(dialog)
        price_entry.insert(0, str(row[2]))
        price_entry.grid(row=2, column=1, padx=5, pady=5)

        ttk.Label(dialog, text="Min Threshold:").grid(row=3, column=0, padx=5, pady=5, sticky=E)
        threshold_entry = ttk.Entry(dialog)
        threshold_entry.insert(0, str(row[4]))
        threshold_entry.grid(row=3, column=1, padx=5, pady=5)

        ttk.Label(dialog, text="Extra Data:").grid(row=4, column=0, padx=5, pady=5, sticky=E)
        extra_entry = ttk.Entry(dialog)
        extra_entry.insert(0, row[6] or "")
        extra_entry.grid(row=4, column=1, padx=5, pady=5)

        def save():
            try:
                self.controller.update_item(
                    item_id,
                    name_entry.get().strip(),
                    float(price_entry.get()),
                    int(threshold_entry.get()),
                    extra_entry.get().strip()
                )
                messagebox.showinfo("Success", "Item updated.")
                dialog.destroy()
                self.refresh_inventory_tree(tree)
            except ValueError:
                messagebox.showerror("Error", "Invalid numeric value.")

        ttk.Button(dialog, text="Save", command=save).grid(row=5, column=0, columnspan=2, pady=15)

    def delete_item(self):
        tree = self.main_frame.master.tree
        selected = tree.selection()
        if not selected:
            messagebox.showwarning("Select Item", "Please select an item to delete.")
            return
        item_id = tree.item(selected[0])['values'][0]
        if messagebox.askyesno("Confirm Delete", f"Delete item {item_id}?"):
            self.controller.delete_item(item_id)
            self.refresh_inventory_tree(tree)

    def build_transactions_tab(self, parent):
        inbound_frame = ttk.LabelFrame(parent, text="Inbound (Receive Stock)", padding=10)
        inbound_frame.pack(fill=X, padx=10, pady=5)

        row1 = ttk.Frame(inbound_frame)
        row1.pack(fill=X, pady=2)
        ttk.Label(row1, text="Item ID:").pack(side=LEFT)
        in_item = ttk.Entry(row1, width=15)
        in_item.pack(side=LEFT, padx=5)
        ttk.Label(row1, text="Quantity:").pack(side=LEFT, padx=(20,0))
        in_qty = ttk.Entry(row1, width=10)
        in_qty.pack(side=LEFT, padx=5)
        ttk.Label(row1, text="Warehouse:").pack(side=LEFT, padx=(20,0))
        in_wh = ttk.Combobox(row1, values=[wh[0] for wh in self.controller.get_warehouses()], width=10, state="readonly")
        in_wh.pack(side=LEFT, padx=5)
        if self.controller.get_warehouses():
            in_wh.current(0)

        row2 = ttk.Frame(inbound_frame)
        row2.pack(fill=X, pady=2)
        ttk.Label(row2, text="Location:").pack(side=LEFT)
        in_loc = ttk.Combobox(row2, width=15)
        in_loc.pack(side=LEFT, padx=5)
        ttk.Label(row2, text="Supplier ID (optional):").pack(side=LEFT, padx=(20,0))
        in_sup = ttk.Entry(row2, width=15)
        in_sup.pack(side=LEFT, padx=5)

        def update_locations(*args):
            wh = in_wh.get()
            if wh:
                locs = self.controller.get_locations(wh)
                in_loc['values'] = locs
                if locs:
                    in_loc.current(0)
        in_wh.bind('<<ComboboxSelected>>', update_locations)
        update_locations()

        def do_inbound():
            try:
                if self.controller.inbound(
                    in_item.get().strip(),
                    int(in_qty.get()),
                    in_wh.get(),
                    in_loc.get(),
                    in_sup.get().strip() or None
                ):
                    messagebox.showinfo("Success", "Inbound transaction completed.")
                    in_item.delete(0, END)
                    in_qty.delete(0, END)
                    self.refresh_inventory_tree(self.main_frame.master.tree)
                else:
                    messagebox.showerror("Error", "Inbound failed.")
            except Exception as e:
                messagebox.showerror("Error", str(e))

        ttk.Button(inbound_frame, text="Process Inbound", command=do_inbound).pack(pady=10)

        outbound_frame = ttk.LabelFrame(parent, text="Outbound (Ship Stock)", padding=10)
        outbound_frame.pack(fill=X, padx=10, pady=5)

        row1 = ttk.Frame(outbound_frame)
        row1.pack(fill=X, pady=2)
        ttk.Label(row1, text="Item ID:").pack(side=LEFT)
        out_item = ttk.Entry(row1, width=15)
        out_item.pack(side=LEFT, padx=5)
        ttk.Label(row1, text="Quantity:").pack(side=LEFT, padx=(20,0))
        out_qty = ttk.Entry(row1, width=10)
        out_qty.pack(side=LEFT, padx=5)
        ttk.Label(row1, text="Warehouse:").pack(side=LEFT, padx=(20,0))
        out_wh = ttk.Combobox(row1, values=[wh[0] for wh in self.controller.get_warehouses()], width=10, state="readonly")
        out_wh.pack(side=LEFT, padx=5)
        if self.controller.get_warehouses():
            out_wh.current(0)

        row2 = ttk.Frame(outbound_frame)
        row2.pack(fill=X, pady=2)
        ttk.Label(row2, text="Location (optional):").pack(side=LEFT)
        out_loc = ttk.Combobox(row2, width=15)
        out_loc.pack(side=LEFT, padx=5)

        def update_out_locations(*args):
            wh = out_wh.get()
            if wh:
                locs = self.controller.get_locations(wh)
                out_loc['values'] = [""] + locs
                out_loc.current(0)
        out_wh.bind('<<ComboboxSelected>>', update_out_locations)
        update_out_locations()

        def do_outbound():
            try:
                loc = out_loc.get().strip()
                if loc == "":
                    loc = None
                if self.controller.outbound(
                    out_item.get().strip(),
                    int(out_qty.get()),
                    out_wh.get(),
                    loc
                ):
                    messagebox.showinfo("Success", "Outbound transaction completed.")
                    out_item.delete(0, END)
                    out_qty.delete(0, END)
                    self.refresh_inventory_tree(self.main_frame.master.tree)
                else:
                    messagebox.showerror("Error", "Outbound failed.")
            except Exception as e:
                messagebox.showerror("Error", str(e))

        ttk.Button(outbound_frame, text="Process Outbound", command=do_outbound).pack(pady=10)

        hist_frame = ttk.LabelFrame(parent, text="Recent Transactions", padding=5)
        hist_frame.pack(fill=BOTH, expand=True, padx=10, pady=5)

        tree = ttk.Treeview(hist_frame, columns=("ID", "Type", "Item", "Qty", "User", "Date"), show="headings", height=10)
        tree.heading("ID", text="ID")
        tree.heading("Type", text="Type")
        tree.heading("Item", text="Item")
        tree.heading("Qty", text="Qty")
        tree.heading("User", text="User")
        tree.heading("Date", text="Date")
        tree.column("ID", width=150)
        tree.column("Type", width=60)
        tree.column("Item", width=200)
        tree.column("Qty", width=60)
        tree.column("User", width=120)
        tree.column("Date", width=150)

        scrollbar = ttk.Scrollbar(hist_frame, orient=VERTICAL, command=tree.yview)
        tree.configure(yscrollcommand=scrollbar.set)
        tree.pack(side=LEFT, fill=BOTH, expand=True)
        scrollbar.pack(side=RIGHT, fill=Y)

        def refresh_history():
            for row in tree.get_children():
                tree.delete(row)
            for t in self.controller.get_recent_transactions(50):
                tree.insert("", END, values=t)

        ttk.Button(hist_frame, text="Refresh", command=refresh_history).pack(anchor=E, pady=2)
        refresh_history()

    def build_suppliers_tab(self, parent, is_admin):
        btn_frame = ttk.Frame(parent)
        btn_frame.pack(fill=X, padx=5, pady=5)

        if is_admin:
            ttk.Button(btn_frame, text="Add Supplier", command=self.add_supplier_dialog).pack(side=LEFT)

        ttk.Button(btn_frame, text="Refresh", command=lambda: self.refresh_supplier_tree(tree)).pack(side=LEFT, padx=10)

        tree_frame = ttk.Frame(parent)
        tree_frame.pack(fill=BOTH, expand=True, padx=5, pady=5)

        tree = ttk.Treeview(tree_frame, columns=("ID", "Name", "Contact", "Categories"), show="headings")
        tree.heading("ID", text="ID")
        tree.heading("Name", text="Name")
        tree.heading("Contact", text="Contact")
        tree.heading("Categories", text="Categories")
        tree.column("ID", width=100)
        tree.column("Name", width=200)
        tree.column("Contact", width=200)
        tree.column("Categories", width=200)

        scrollbar = ttk.Scrollbar(tree_frame, orient=VERTICAL, command=tree.yview)
        tree.configure(yscrollcommand=scrollbar.set)
        tree.pack(side=LEFT, fill=BOTH, expand=True)
        scrollbar.pack(side=RIGHT, fill=Y)

        self.refresh_supplier_tree(tree)
        parent.tree = tree

    def refresh_supplier_tree(self, tree):
        for row in tree.get_children():
            tree.delete(row)
        for sup in self.controller.get_all_suppliers():
            tree.insert("", END, values=sup)

    def add_supplier_dialog(self):
        dialog = Toplevel(self.root)
        dialog.title("Add Supplier")
        dialog.geometry("350x200")
        dialog.transient(self.root)
        dialog.grab_set()

        ttk.Label(dialog, text="Supplier ID:").grid(row=0, column=0, padx=5, pady=5, sticky=E)
        id_entry = ttk.Entry(dialog)
        id_entry.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(dialog, text="Name:").grid(row=1, column=0, padx=5, pady=5, sticky=E)
        name_entry = ttk.Entry(dialog)
        name_entry.grid(row=1, column=1, padx=5, pady=5)

        ttk.Label(dialog, text="Contact:").grid(row=2, column=0, padx=5, pady=5, sticky=E)
        contact_entry = ttk.Entry(dialog)
        contact_entry.grid(row=2, column=1, padx=5, pady=5)

        ttk.Label(dialog, text="Categories:").grid(row=3, column=0, padx=5, pady=5, sticky=E)
        cat_entry = ttk.Entry(dialog)
        cat_entry.grid(row=3, column=1, padx=5, pady=5)

        def save():
            if self.controller.add_supplier(
                id_entry.get().strip(),
                name_entry.get().strip(),
                contact_entry.get().strip(),
                cat_entry.get().strip()
            ):
                messagebox.showinfo("Success", "Supplier added.")
                dialog.destroy()
                self.refresh_supplier_tree(self.main_frame.master.tree)
            else:
                messagebox.showerror("Error", "Supplier ID already exists.")

        ttk.Button(dialog, text="Save", command=save).grid(row=4, column=0, columnspan=2, pady=15)

    def build_users_tab(self, parent):
        ttk.Label(parent, text="User Management", font=("Arial", 12)).pack(pady=10)

        tree = ttk.Treeview(parent, columns=("ID", "Name", "Role", "Contact"), show="headings")
        tree.heading("ID", text="ID")
        tree.heading("Name", text="Name")
        tree.heading("Role", text="Role")
        tree.heading("Contact", text="Contact")
        tree.pack(fill=BOTH, expand=True, padx=10, pady=10)

        def refresh_users():
            for row in tree.get_children():
                tree.delete(row)
            conn = Database.get_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT user_id, name, role, contact FROM users")
            for row in cursor.fetchall():
                tree.insert("", END, values=row)
            conn.close()

        btn_frame = ttk.Frame(parent)
        btn_frame.pack(fill=X, padx=10, pady=5)
        ttk.Button(btn_frame, text="Refresh", command=refresh_users).pack(side=LEFT)
        ttk.Button(btn_frame, text="Add User", command=self.add_user_dialog).pack(side=LEFT, padx=5)

        refresh_users()

    def add_user_dialog(self):
        dialog = Toplevel(self.root)
        dialog.title("Add New User")
        dialog.geometry("350x250")
        dialog.transient(self.root)
        dialog.grab_set()

        ttk.Label(dialog, text="Username:").grid(row=0, column=0, padx=5, pady=5, sticky=E)
        user_entry = ttk.Entry(dialog)
        user_entry.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(dialog, text="Full Name:").grid(row=1, column=0, padx=5, pady=5, sticky=E)
        name_entry = ttk.Entry(dialog)
        name_entry.grid(row=1, column=1, padx=5, pady=5)

        ttk.Label(dialog, text="Contact:").grid(row=2, column=0, padx=5, pady=5, sticky=E)
        contact_entry = ttk.Entry(dialog)
        contact_entry.grid(row=2, column=1, padx=5, pady=5)

        ttk.Label(dialog, text="Role:").grid(row=3, column=0, padx=5, pady=5, sticky=E)
        role_combo = ttk.Combobox(dialog, values=["admin", "staff"], state="readonly")
        role_combo.current(1)
        role_combo.grid(row=3, column=1, padx=5, pady=5)

        ttk.Label(dialog, text="Password:").grid(row=4, column=0, padx=5, pady=5, sticky=E)
        pass_entry = ttk.Entry(dialog, show="*")
        pass_entry.grid(row=4, column=1, padx=5, pady=5)

        def save():
            if not user_entry.get().strip() or not pass_entry.get():
                messagebox.showerror("Error", "Username and password are required.")
                return
            if self.controller.create_user(
                user_entry.get().strip(),
                name_entry.get().strip() or user_entry.get().strip(),
                contact_entry.get().strip() or "",
                role_combo.get(),
                pass_entry.get()
            ):
                messagebox.showinfo("Success", "User created.")
                dialog.destroy()
            else:
                messagebox.showerror("Error", "Username already exists.")

        ttk.Button(dialog, text="Save", command=save).grid(row=5, column=0, columnspan=2, pady=15)