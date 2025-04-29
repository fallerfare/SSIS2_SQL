from tkinter import ttk
from DATA import GlobalSQL

# =====================
#    REFRESH BUTTON
# =====================
class Refresh:
    def __init__(self, root, dataframe, table, search):
        # ye
        self.root = root
        self.dataframe = GlobalSQL.updateDF(dataframe)
        self.table = table
        self.search = search

        self.Button = ttk.Button(self.root, text="Refresh", command=self.refresh)

    def refresh(self):
        self.table.PopulateTable(self.table.tree, GlobalSQL.updateDF(self.table.dataframe))
        self.search.searchbar.delete(0, "end")
        self.search.searchbychoose.set("--Default--")
        self.search.sortwithbar.set("--Default--")
        self.search.sortbybar.set("--Default--")

# =====================
#    REFRESH BUTTON
# =====================