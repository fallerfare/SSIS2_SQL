from DATA import GlobalSQL
import DISPLAY.BUTTONS.Add as Add  
import DISPLAY.BUTTONS.RemoveSQL as Remove
import DISPLAY.BUTTONS.Edit as Edit
import DISPLAY.BUTTONS.Refresh as Refresh

# =========================
#     BUTTONS FUNCTIONS
# =========================
class Buttons:

    def __init__(self, root, dataframe, table, search):
        self.root = root
        self.dataframe = GlobalSQL.updateDF(dataframe)
        self.table = table
        self.search = search
        self.createbuttons()
        self.tree = self.table.tree
        self.tree.bind("<<TreeviewSelect>>", lambda event: self.on_select(event)) 

    def createbuttons(self):
        
        self.enroll_button  = Add.Add(      self.root, self.dataframe, self.table)  
        self.remove_button  = Remove.Remove(self.root, self.dataframe, self.table)  
        self.edit_button    = Edit.Edit(    self.root, self.dataframe, self.table)  
        self.refresh_button = Refresh.Refresh(self.root, self.dataframe, self.table, self.search)  

        self.remove_button.Button.config(   state="disabled")
        self.edit_button.Button.config(     state="disabled")

        self.refresh_button.Button.grid(    row=0, column=0, padx=10)
        self.enroll_button.Button.grid(     row=0, column=1, padx=10)
        self.remove_button.Button.grid(     row=0, column=2, padx=10)
        self.edit_button.Button.grid(       row=0, column=3, padx=10)

    # Activate Remove and Edit Buttons once treeview has a selected item
    def on_select(self, event):
        
        self.selected_item = self.tree.selection()
        
        if self.selected_item:  
            self.remove_button.Button.config(state="normal")
            self.edit_button.Button.config(state="normal")

            selected_value = self.tree.item(self.selected_item, "values")[0]
            self.remove_button.setremovekey(selected_value) 
            
            # Debugging
            # print(f"Selected: {selected_value}")
        
        else: 
            self.remove_button.Button.config(state="disabled")
            self.edit_button.Button.config(state="disabled")
# =========================
#     BUTTONS FUNCTIONS
# =========================