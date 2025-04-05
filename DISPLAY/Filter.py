from tkinter import ttk
from DATA import GlobalDFs
from sqlalchemy import create_engine
import pandas as pd

class Filter():
    def __init__(self, root, table):
        self.root = root
        self.dataframe = GlobalDFs.readStudents()
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

    def perform_searchandsort(self, event):

        db_connection_str = 'mysql+pymysql://root:root@localhost/studentdbms'
        db_connection = create_engine(db_connection_str)

        self.search_term = self.searchbar.get().strip().lower()
        self.search_type = self.searchbychoose.get().strip()
        self.sortwithkey = self.sortwithbar.get().strip()
        self.sortbykey = self.sortbybar.get().strip()

        if self.dataframe.empty:
            return

        # Filtering logic
        if self.search_term:
            if self.search_type:
                query = "SELECT * FROM students WHERE " + self.search_type + " = " + self.search_term

            else:
                query = "SELECT * FROM students WHERE " + self.search_type + " = " + self.search_term

        df = pd.read_sql(query, con=db_connection)

        # Sorting logic
        if self.sortwithkey and self.sortbykey:
            ascending = self.sortbykey == "Ascending"
            self.dataframe = self.dataframe.sort_values(by=[self.sortwithkey], ascending=ascending)

        self.table.PopulateTable(self.table.tree)