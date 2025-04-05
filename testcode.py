from tkinter import ttk
import tkinter as tk
from DISPLAY.Table import Table
from DISPLAY.Filter import Filter
import TKinterModernThemes as TKMT

# =======================
#     MAIN FUNCTION
# =======================
if __name__ =="__main__":
        # Style
        window = TKMT.ThemedTKinterFrame("MSU-IIT Students","azure","dark")
        window.root.geometry("1000x860")
        window.root.resizable(width=False, height=False)

        style = ttk.Style()
        style.configure(  "Treeview", 
                            background =        "#ffffff", 
                            foreground =        "#000000",
                            rowheight =         25,
                            fieldbackground =   "#ffffff")

        # Header
        HeaderFrame = tk.Frame(window.root, background = "maroon")
        HeaderFrame.pack()
        Title = ttk.Label(HeaderFrame, text="MSU - IIT Students Repository", font=('Arial', 15), anchor = "center", background = "maroon", width = 800)
        Title.pack(padx = 15, pady = 10)

        studentTable = Table(window.root)
        studentFilter = Filter(window.root, studentTable)

        window.root.mainloop()
# =======================
#     MAIN FUNCTIONS
# =======================