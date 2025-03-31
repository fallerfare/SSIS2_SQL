from tkinter import ttk
from DATA import GlobalDFs

class Filter():
    def __init__(self, root, dataframe, table):
        self.root = root
        self.dataframe = GlobalDFs.updateDF(dataframe)
        self.table = table

        self.searchnsortframe = ttk.Frame(root)
        self.searchnsortframe.pack(anchor="center")

        self.searchlabel = ttk.Label(self.searchnsortframe, text="Search", font=('Arial', 12))
        self.searchbylabel = ttk.Label(self.searchnsortframe, text="by: ", font=('Arial', 12))
        self.sortwithlabel = ttk.Label(self.searchnsortframe, text="Sort with", font=('Arial', 12))
        self.sortbylabel = ttk.Label(self.searchnsortframe, text="Sort by", font=('Arial', 12))

        self.searchbar = ttk.Entry(self.searchnsortframe, font=('Arial', 9), width=20)
        self.searchbychoose = ttk.Combobox(self.searchnsortframe, state="readonly",
                                         values=list(self.dataframe.columns),
                                        width=15)

        self.sortwithbar = ttk.Combobox(self.searchnsortframe, state="readonly",
                                        values=list(self.dataframe.columns),
                                        width=15)

        self.sortbybar = ttk.Combobox(self.searchnsortframe, state="readonly",
                                      values=["Ascending", "Descending"],
                                      width=15)

        self.searchbar.bind("<KeyRelease>", self.perform_searchandsort)
        self.searchbychoose.bind("<<ComboboxSelected>>", self.perform_searchandsort)
        self.sortwithbar.bind("<<ComboboxSelected>>", self.perform_searchandsort)
        self.sortbybar.bind("<<ComboboxSelected>>", self.perform_searchandsort)

        self.searchlabel.grid(row=0, column=0)
        self.searchbar.grid(row=0, column=1)
        self.searchbylabel.grid(row=0, column=2)
        self.searchbychoose.grid(row=0, column=3)
        self.sortwithlabel.grid(row=0, column=4)
        self.sortwithbar.grid(row=0, column=5)
        self.sortbylabel.grid(row=0, column=6)
        self.sortbybar.grid(row=0, column=7)

        self.filtered_df = self.table.dataframe = GlobalDFs.updateDF(self.table.dataframe)  # Ensure table has updated dataframe

    def perform_searchandsort(self, event):
        self.search_term = self.searchbar.get().strip().lower()
        self.search_type = self.searchbychoose.get().strip()
        self.sortwithkey = self.sortwithbar.get().strip()
        self.sortbykey = self.sortbybar.get().strip()

        self.filtered_df = GlobalDFs.updateDF(self.table.dataframe)  # Ensure table has updated dataframe

        if self.filtered_df.empty:
            return

        # Filtering logic
        if self.search_term:
            if self.search_type:
                self.filtered_df = self.filtered_df[self.filtered_df[self.search_type].astype(str)
                    .str.lower().str.contains(self.search_term, na=False)]
            else:
                mask = self.filtered_df.astype(str).apply(lambda row: row.str.lower().str.contains(self.search_term), axis=1)
                self.filtered_df = self.filtered_df[mask.any(axis=1)]

        # Sorting logic
        if self.sortwithkey and self.sortbykey:
            ascending = self.sortbykey == "Ascending"
            self.filtered_df = self.filtered_df.sort_values(by=[self.sortwithkey], ascending=ascending)

        self.table.Populate(self.table.tree, self.filtered_df, "Filter")