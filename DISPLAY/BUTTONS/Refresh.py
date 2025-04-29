from tkinter import ttk
from DATA import GlobalSQL

# =====================
#    REFRESH BUTTON
# =====================
class Refresh:
    def __init__(self, root, dataframe, table):
        # ye
        self.root = root
        self.dataframe = GlobalSQL.updateDF(dataframe)
        self.table = table

        self.Button = ttk.Button(self.root, text="Refresh", command=self.refresh)

    def refresh(self):
        self.table.PopulateTable(self.table.tree, GlobalSQL.updateDF(self.table.dataframe))
# =====================
#    REFRESH BUTTON
# =====================