from tkinter import ttk
from DATA import GlobalDFs

# =====================
#    REFRESH BUTTON
# =====================
class Refresh:
    def __init__(self, root, dataframe, table):
        # ye
        self.root = root
        self.dataframe = GlobalDFs.updateDF(dataframe)
        self.table = table

        self.Button = ttk.Button(self.root, text="Refresh", command=self.refresh)

    def refresh(self):
        self.table.Populate(self.table.tree, GlobalDFs.updateDF(self.table.dataframe), "Update")
# =====================
#    REFRESH BUTTON
# =====================