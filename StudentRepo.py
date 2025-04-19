from tkinter import ttk
import tkinter as tk
import TKinterModernThemes as TKMT
from DISPLAY.Repo import Repo
from DATA import GlobalDFs

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

      # Tabs
      notebook = ttk.Notebook(window.root)
      notebook.pack(padx = 35, pady = 35, anchor= "center")

      Students = Repo(notebook, notebook, GlobalDFs.readStudentsDF(), "students") # Students Tab
      Programs = Repo(notebook, notebook, GlobalDFs.readProgramsDF(), "programs") # Programs Tab
      Colleges = Repo(notebook, notebook, GlobalDFs.readCollegesDF(), "colleges") # Colleges Tab

      notebook.add(Students.returnFrame(), text="Students")
      notebook.add(Programs.returnFrame(), text="Programs")
      notebook.add(Colleges.returnFrame(), text="Colleges")

      window.root.mainloop()
# =======================
#     MAIN FUNCTIONS
# =======================