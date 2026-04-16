# main.py
import sys
import traceback

# Check Tkinter availability
try:
    from tkinter import *
    from tkinter import ttk, messagebox
    TKINTER_AVAILABLE = True
except ImportError as e:
    TKINTER_AVAILABLE = False
    print("ERROR: Tkinter is not available. Please install python3-tk.")
    print(f"Import error: {e}")
    sys.exit(1)

from gui import WarehouseApp

if __name__ == "__main__":
    try:
        print("Initializing application...")
        app = WarehouseApp()
        app.run()
    except Exception as e:
        print("FATAL ERROR: Application crashed.")
        print(traceback.format_exc())
        try:
            root = Tk()
            root.withdraw()
            messagebox.showerror("Fatal Error", f"Application failed to start:\n\n{str(e)}")
            root.destroy()
        except:
            pass
        sys.exit(1)