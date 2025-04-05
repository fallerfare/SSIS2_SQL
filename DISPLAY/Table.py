from tkinter import ttk
from DATA import GlobalDFs

# ==========================================
#     DYNAMIC TABLE, ADD ANY DATAFRAME
# ==========================================
class Table():
        def __init__(self, root, dataframe):
                self.root = root
                self.dataframe = GlobalDFs.updateDF(dataframe)

                # Scrollbar
                self.treeScroll = ttk.Scrollbar(self.root)
                self.treeScroll.pack(side="right", fill='y', anchor="center")

                # Treeview
                self.tree = ttk.Treeview(self.root,  selectmode =        "browse", 
                                                show =              'headings', 
                                                yscrollcommand =    self.treeScroll.set, 
                                                style =             "Treeview"
                                        )
                self.tree['columns'] = list(self.dataframe.columns)
                
                for col in self.dataframe.columns:
                        self.tree.heading(col, text = col)
                        self.tree.column(col, width = 100, anchor = 'center')


                self.tree.tag_configure('evenrow', background="#9ce3ff")

                self.PopulateTable(self.tree, self.dataframe)

        def PopulateTable(self, tree, dataframe):
                # Clear table
                self.dataframe = dataframe
                # print("Populating")
                for row in self.tree.get_children():
                        self.tree.delete(row)

                for index, row in self.dataframe.iterrows():
                        if index % 2 == 0:
                                self.tree.insert("", "end", values=list(row), tags=('evenrow', ))
                        else:
                                self.tree.insert("", "end", values=list(row), tags=('oddrow', ))

                self.tree.pack(side="left", fill="both", anchor = "center", expand=True)
                self.treeScroll.config(command=self.tree.yview)                                                                                                                                                                         
# ==========================================
#     DYNAMIC TABLE, ADD ANY DATAFRAME
# ==========================================