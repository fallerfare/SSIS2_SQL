from tkinter import ttk
from DATA import GlobalDFs

# ==========================================
#     DYNAMIC TABLE, ADD ANY DATAFRAME
# ==========================================
class Table():
        def __init__(self, root, dataframe, notebook):
                self.root = root
                self.dataframe = GlobalDFs.updateDF(dataframe)
                self.notebook = notebook

                # Scrollbar
                self.treeScroll = ttk.Scrollbar(root)
                self.treeScroll.pack(side="right", fill='y', anchor="center")

                # Treeview
                self.tree = ttk.Treeview(root,  selectmode =        "browse", 
                                                show =              'headings', 
                                                yscrollcommand =    self.treeScroll.set, 
                                                style =             "Treeview"
                                        )
                self.tree['columns'] = list(self.dataframe.columns)
                
                for col in self.dataframe.columns:
                        self.tree.heading(col, text = col)
                        self.tree.column(col, width = 100, anchor = 'center')

                self.Populate(self.tree, self.dataframe, "Update")

                self.tree.pack(side="left", fill="both", anchor = "center", expand=True)
                self.treeScroll.config(command=self.tree.yview)

        # Separate populating function to be accessed by other functions
        def Populate(self, tree, dataframe, source):
                self.dataframe = dataframe
                self.tree.tag_configure('evenrow', background="#9ce3ff")

                # Clear table
                for row in self.tree.get_children():
                        self.tree.delete(row)

                if(source == "Filter"):
                        for index, row in dataframe.iterrows():
                                if index % 2 == 0:
                                        tree.insert("", "end", values=list(row), tags=('evenrow', ))
                                else:
                                        tree.insert("", "end", values=list(row), tags=('oddrow', ))

                if(source == "Update"):
                        self.dataframe = GlobalDFs.updateDF(self.dataframe)
                        for index, row in self.dataframe.iterrows():
                                if index % 2 == 0:
                                        tree.insert("", "end", values=list(row), tags=('evenrow', ))
                                else:
                                        tree.insert("", "end", values=list(row), tags=('oddrow', ))
# ==========================================
#     DYNAMIC TABLE, ADD ANY DATAFRAME
# ==========================================