from tkinter import ttk
from DATA import GlobalDFs
from sqlalchemy import create_engine
import pandas as pd

class Filter():
    def __init__(self, root, dataframe, table, tab):
        self.root = root
        self.dataframe = GlobalDFs.updateDF(dataframe)
        self.table = table
        self.columns = self.dataframe.columns
        self.tab = tab

        self.searchlabel = ttk.Label(self.root, text="Search", font=('Arial', 12))
        self.searchbylabel = ttk.Label(self.root, text="by: ", font=('Arial', 12))
        self.sortwithlabel = ttk.Label(self.root, text="Sort with", font=('Arial', 12))
        self.sortbylabel = ttk.Label(self.root, text="Sort by", font=('Arial', 12))

        self.searchbar = ttk.Entry(self.root, font=('Arial', 9), width=20)
        self.searchbychoose = ttk.Combobox(self.root, state="readonly",
                                         values=list(self.dataframe.columns),
                                        width=15)

        self.sortwithbar = ttk.Combobox(self.root, state="readonly",
                                        values=list(self.dataframe.columns),
                                        width=15)

        self.sortbybar = ttk.Combobox(self.root, state="readonly",
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

    def perform_searchandsort(self, event):

        self.search_term = self.searchbar.get().strip().lower()
        self.search_type = self.searchbychoose.get().strip()
        self.sortwithkey = self.sortwithbar.get().strip()
        self.sortbykey = self.sortbybar.get().strip()

        self.dataframe = df = GlobalDFs.filterDF(self.search_term, self.search_type, self.sortwithkey, self.sortbykey, self.tab)

        self.table.PopulateTable(self.table.tree, df)


        # # self.basequery = "SELECT * FROM students "
        # # self.searchquery = ""
        # # self.sortquery = ""
        # # self.params = ()

        # if self.dataframe.empty:
        #     return

        # # # Filtering logic
        # # if self.search_term:
        # #     if self.search_type:
        # #         self.searchquery = f"WHERE `{self.search_type}` LIKE %s"
        # #         self.params = (f"%{self.search_term}%", )
        # #     else: 
        # #         self.searchquery = f"WHERE ("
        # #         for column in self.columns:
        # #             self.searchquery += f"`{column}` LIKE %s"
        # #             self.params = (f"%{self.search_term}%", )
        # #         self.searchquery += f")"
                
        # # self.query = self.basequery + self.searchquery + self.sortquery
        # # print(self.query)
        # # df = pd.read_sql(self.query, con=db_connection, params = tuple(self.params))

        # # Filtering logic

        # self.filtered_df = GlobalDFs.readStudentsDF()

        # if self.search_term:
        #     if self.search_type:
        #         self.filtered_df = self.filtered_df[self.filtered_df[self.search_type].astype(str)
        #             .str.lower().str.contains(self.search_term, na=False)]
        #     else:
        #         mask = self.filtered_df.astype(str).apply(lambda row: row.str.lower().str.contains(self.search_term), axis=1)
        #         self.filtered_df = self.filtered_df[mask.any(axis=1)]

        # # Sorting logic
        # if self.sortwithkey and self.sortbykey:
        #     ascending = self.sortbykey == "Ascending"
        #     self.filtered_df = self.filtered_df.sort_values(by=[self.sortwithkey], ascending=ascending)

        # self.table.PopulateTable(self.table.tree, self.filtered_df)