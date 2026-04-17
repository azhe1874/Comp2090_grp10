# 🏭 Warehouse Management System (WMS)
> COMP8090SEF — Data Structures, Algorithms and Problem Solving

**Course Project — Task 1 | HKMU Spring 2026**
## 📦 Project Overview
The **Warehouse Management System (WMS)** is a desktop Python application that solves real-life inventory management challenges. It enables businesses to:
1.	Track stock in multiple warehouses 
2.	Record stock incoming and outgoing 
3.	Show low-stock warnings automatically 
4.	Manage suppliers and user accounts with role permissions
The app used MVC design, stores data with SQLite, has a Tkinter/ttk interface, and uses all main OOP ideas from the course.

## ▶️ How to Run
python main.py
The application window will open automatically.
## 🧙 First-Time Setup
On the **very first launch**, no users exist in the database. A setup wizard will appear automatically:
1. **Create an Admin account** (required)
   - Enter a username, full name, contact email, and password
2. **Create a Staff account** (optional)
   - Leave the username blank to skip
3. Click **"Complete Setup"**
   - Sample data (items, suppliers, warehouse, locations) will be auto-loaded
4. You will be redirected to the **Login screen**
> ⚠️ Keep your admin credentials safe — there is currently no password recovery feature.
## 📖 User Guide
### Login
Enter your **Username** and **Password**, then click **Login** (or press `Enter`).
| Role | Permissions |
| **Admin** | Full access: manage items, suppliers, users, transactions |
| **Staff** | View inventory, process inbound/outbound transactions, view suppliers 
### Dashboard Tab

Displays a real-time summary:
- **Total Items** in the system
- **Total Inventory Value** (quantity × unit price)
- **Low-Stock Alerts** — items below their minimum threshold
- **Recent Transactions** — last 10 operations

### Inventory Tab
| Button | Action |
| Add Item | Opens form to create a new item |
| Edit Item | Select a row, then click to modify name, price, or threshold |
| Delete Item | Select a row, then click to permanently remove |
| Refresh | Reload the list from database |

**Item Types:**
- **Perishable** — requires `shelf_life_days` in the Extra Data field as JSON, e.g. `{"shelf_life_days": 14}`
- **NonPerishable** — requires `warranty_months` in the Extra Data field as JSON, e.g. `{"warranty_months": 12}`

### Transactions Tab
#### Inbound (Receive Stock)
1. Enter the **Item ID** (e.g. `I001`)
2. Enter the **Quantity** to receive
3. Select the **Warehouse** from the dropdown
4. Select the **Location** (auto-populated based on warehouse)
5. Optionally enter a **Supplier ID**
6. Click **Process Inbound**

#### Outbound (Ship Stock)
1. Enter the **Item ID** and **Quantity**
2. Select the **Warehouse**
3. Optionally select a specific **Location** (leave blank to auto-distribute)
4. Click **Process Outbound**

> The system will raise an error if stock is insufficient or warehouse capacity is exceeded.

---

### Suppliers Tab *(Admin only to add)*
**Add Supplier** — Enter Supplier ID, Name, Contact, and Categories
- **Refresh** — Reload supplier list

### Users Tab *(Admin only)*
- **Add User** — Create new Admin or Staff accounts
- **Refresh** — Reload user list

📺 **Watch the 5-minute introduction video here:**
👉 [https://drive.google.com/drive/folders/1JJKPRNY5W6xoUDkxoutw_6eZFlk7nO75?usp=sharing]
## 👤 Author/Info
| **Name** | [KEUNG Hoi Ching] [Lam Wai] [Wong Hiu Ching] |
| **Student ID** | [13882355] [13877984] [13884686] |
| **Course** | COMP8090SEF |
| **Institution** | Hong Kong Metropolitan University (HKMU) |

