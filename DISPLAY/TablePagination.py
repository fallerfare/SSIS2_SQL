from tkinter import ttk
import tkinter as tk
from DATA import GlobalDFs
import math

# ==========================================
#     DYNAMIC TABLE, ADD ANY DATAFRAME
# ==========================================
class Table():
        def __init__(self, root, dataframe):
                self.root = root
                self.dataframe = GlobalDFs.updateDF(dataframe)

                self.rows_page = 11
                self.items = len(self.dataframe)
                self.pages = math.ceil(self.items/self.rows_page)
                self.curr_page = 1
                self.curr_page_var = tk.IntVar(value=(self.curr_page)) 
                self.pageList = []

                # Treeview
                self.treeFrame = ttk.Frame(self.root)
                self.treeFrame.pack(anchor = "center")
                self.tree = ttk.Treeview(self.root,  selectmode =        "browse", 
                                                show =              'headings', 
                                                style =             "Treeview"
                                        )
                self.tree['columns'] = list(self.dataframe.columns)
                
                for col in self.dataframe.columns:
                        self.tree.heading(col, text = col)
                        self.tree.column(col, width = 100, anchor = 'center')


                self.tree.tag_configure('evenrow', background="#9ce3ff")

                self.pageButtons = ttk.Frame(self.root)
                self.pageButtons.pack(side = "bottom", anchor = "center", pady = 5)

                self.PopulateTable(self.tree, self.dataframe, self.curr_page)

        def PopulateTable(self, tree, dataframe, page = 1):
                # Clear table
                self.dataframe = dataframe
                self.items = len(self.dataframe)
                self.pages = math.ceil(self.items/self.rows_page)
                self.curr_page = page
                self.curr_page_var = tk.IntVar(value=(self.curr_page)) 

                # print("Populating")
                
                for row in self.tree.get_children():
                        self.tree.delete(row)
                for button in self.pageList:
                        button.destroy()

                start_idx = (self.curr_page - 1) * self.rows_page
                end_idx = start_idx + self.rows_page
                page_data = self.dataframe.iloc[start_idx:end_idx]

                for index, row in page_data.iterrows():
                        if index % 2 == 0:
                                self.tree.insert("", "end", values=list(row), tags=('evenrow', ))
                        else:
                                self.tree.insert("", "end", values=list(row), tags=('oddrow', ))

                self.tree.pack(side="top", fill="both", anchor = "center", expand=True)       

                self.prevTenButt = ttk.Button(self.pageButtons, text = "<<10", command = lambda: self.PrevTenPage(), width = 5)
                self.prevTenButt.pack(side = "left", padx = 2)
                self.pageList.append(self.prevTenButt)

                self.prevButt = ttk.Button(self.pageButtons, text = "<", command = lambda: self.PrevPage(), width = 3)
                self.prevButt.pack(side = "left", padx = 2)
                self.pageList.append(self.prevButt)

                for i in range(1, self.pages + 1):
                        if self.pages+1 < 10 or i < 5 or (i == 5 and self.curr_page <=5) or i == self.curr_page or (i == (self.pages - 4) and self.curr_page >=(self.pages - 4)) or i > (self.pages - 4):
                                numButt = ttk.Button(self.pageButtons, text = str(i), command = (lambda i=i: self.GotoPage(i)), width = 3)
                                numButt.pack(side = "left", padx = 2)
                                self.pageList.append(numButt)

                self.nextButt = ttk.Button(self.pageButtons, text = ">", command = lambda: self.NextPage(), width = 3)
                self.nextButt.pack(side = "left", padx = 2)
                self.pageList.append(self.nextButt)

                self.nextTenButt = ttk.Button(self.pageButtons, text = "10>>", command = lambda: self.NextTenPage(), width = 5)
                self.nextTenButt.pack(side = "left", padx = 2)
                self.pageList.append(self.nextTenButt)

                self.pageJump = ttk.Combobox(self.pageButtons, state = "readonly", values = list(range(1, self.pages + 1)), textvariable = self.curr_page_var, width = 5)
                self.pageJump.pack(side = "right", padx = 3)

                def jump(event):
                        page = int(self.pageJump.get())
                        if page > 0: self.GotoPage(page)

                self.pageJump.bind("<<ComboboxSelected>>", jump)
                self.pageJump.bind("<KeyRelease>", jump)
                self.pageList.append(self.pageJump)

                self.prevButt.config(state = "disabled") if self.curr_page <= 1 else self.prevButt.config(state = "normal")
                self.nextButt.config(state = "disabled") if self.curr_page >= self.pages else self.nextButt.config(state = "normal")  
                self.prevTenButt.config(state = "disabled") if self.curr_page <= 10 else self.prevTenButt.config(state = "normal")
                self.nextTenButt.config(state = "disabled") if self.curr_page+10 >= self.pages else self.nextTenButt.config(state = "normal")     

        def NextPage(self):
                if self.curr_page < self.pages: 
                        self.curr_page += 1
                        self.PopulateTable(self.tree, self.dataframe, self.curr_page) 

        def NextTenPage(self):
                if self.curr_page < self.pages+10: 
                        self.curr_page += 10
                        self.PopulateTable(self.tree, self.dataframe, self.curr_page) 

        def PrevPage(self):
                if self.curr_page > 1: 
                        self.curr_page -= 1
                        self.PopulateTable(self.tree, self.dataframe, self.curr_page) 

        def PrevTenPage(self):
                if self.curr_page > 10: 
                        self.curr_page -= 10
                        self.PopulateTable(self.tree, self.dataframe, self.curr_page)                            

        def GotoPage(self, page):
                self.PopulateTable(self.tree, self.dataframe, page)                                                                                                                        
# ==========================================
#     DYNAMIC TABLE, ADD ANY DATAFRAME
# ==========================================