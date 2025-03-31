from DISPLAY.Table import Table
from DISPLAY.Filter import Filter
from tkinter import ttk
from DISPLAY.BUTTONS.Buttons import Buttons
from DATA import GlobalDFs

class Repo:
    def __init__(self, root, notebook, dataframe):
        self.root = root
        self.notebook = notebook
        self.dataframe = GlobalDFs.updateDF(dataframe)
        # Table Display
        self.RepoTable = ttk.Frame(self.root, width=990, height=600)  
        self.RepoTable.grid_rowconfigure(0, weight=1) 
        self.RepoTable.grid_columnconfigure(0, weight=1)

        self.createitems()

    def createitems(self):
        # Display Elements

        # Search Display
        self.searchpane = ttk.Frame(self.RepoTable)
        self.searchpane.grid(row = 1, column=0, sticky="nsew", pady=15)

        # Table Display
        self.tablepane = ttk.Frame(self.RepoTable)
        self.tablepane.grid(row = 2, column=0, sticky="nsew", pady=15)

        # Button
        self.buttonframe = ttk.Frame(self.RepoTable)
        self.buttonframe.grid(row = 3, column=0, sticky="e", pady=15)

        self.dataframe = GlobalDFs.updateDF(self.dataframe)

        # Create items
        self.table = Table(self.tablepane, self.dataframe, self.notebook)
        self.search = Filter(self.searchpane, self.dataframe, self.table)
        self.button = Buttons(self.buttonframe, self.dataframe, self.table)

        self.table.dataframe = GlobalDFs.updateDF(self.table.dataframe)

    def returnFrame(self):
        return self.RepoTable
