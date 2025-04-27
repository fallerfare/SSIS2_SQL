from tkinter import ttk
from DATA import GlobalDFs
import pandas as pd

class Filter():
    def __init__(self, root, dataframe, table, tab):
        self.root = root
        self.dataframe = GlobalDFs.updateDF(dataframe)
        self.table = table
        self.columns = self.dataframe.columns
        self.tab = tab

        self.frame = ttk.Frame(self.root)
        self.frame.pack(anchor = "center")

        self.searchlabel = ttk.Label(self.frame, text="Search", font=('Arial', 12))
        self.searchbylabel = ttk.Label(self.frame, text="by: ", font=('Arial', 12))
        self.sortwithlabel = ttk.Label(self.frame, text="Sort with", font=('Arial', 12))
        self.sortbylabel = ttk.Label(self.frame, text="Sort by", font=('Arial', 12))

        self.searchbar = ttk.Entry(self.frame, font=('Arial', 9), width=20)
        self.searchbychoose = ttk.Combobox(self.frame, state="readonly",
                                         values=["--Default--"] + list(self.columns),
                                        width=15)

        self.sortwithbar = ttk.Combobox(self.frame, state="readonly",
                                        values=["--Default--"] + list(self.columns),
                                        width=15)

        self.sortbybar = ttk.Combobox(self.frame, state="readonly",
                                      values=["--Default--", "Ascending", "Descending"],
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

    def perform_searchandsort(self, event):

        self.search_term = self.searchbar.get().strip().lower()
        self.search_type = self.searchbychoose.get().strip()
        self.sortwithkey = self.sortwithbar.get().strip()
        self.sortbykey = self.sortbybar.get().strip()

        connection = GlobalDFs.engine.connect()

        self.basequery = f"SELECT * FROM  {self.tab} "
        self.searchquery = ""
        self.sortquery = ""
        self.params = []

        if self.dataframe.empty:
            return

        # Filtering logic
        if self.search_term:
            if self.search_type and not "--Default--":
                self.searchquery = f"WHERE `{self.search_type}` LIKE %s"
                self.params.append(f"%{self.search_term}%", )
            else: 
                self.searchquery = f"WHERE ("

                searchAll = []
                self.params = []

                for column in self.columns:
                    searchAll.append(f"`{column}` LIKE %s")
                    self.params.append(f"%{self.search_term}%", )

                self.searchquery += " OR ".join(searchAll) + ")"
                
        # Sorting logic
        if self.sortwithkey:
            order = "ASC"
            if self.sortwithkey == "--Default--": self.sortwithkey = f"{self.columns[0]}"
            if self.sortbykey == "Descending": order = "DESC"

            self.sortquery = f"ORDER BY `{self.sortwithkey}` {order}"

        self.query = self.basequery + self.searchquery + self.sortquery
        # print(self.query)
        df = pd.read_sql(self.query, con=connection, params = tuple(self.params))

        self.table.PopulateTable(self.table.tree, df)