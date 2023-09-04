# Main Program
import tkinter as tk
from tkinter import simpledialog, messagebox, ttk
from Todo import Todo
import json

from todoList.Item import Item


class TodoApp(tk.Tk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Initialize the data structure
        self.todo = Todo("My Todo List")
        self.title(self.todo.name)
        self.geometry("500x600")

        # Define light and dark mode colors
        self.define_colors()

        # Initialize and pack GUI components
        self.create_gui_components()

        self.load_from_file()
        self.update_display()

    def define_colors(self):
        # Light and dark mode colors
        self.dark_mode = False
        self.light_colors = {
            'bg': 'white',
            'fg': 'black',
            'btn': '#e0e0e0',
            'entry': '#f5f5f5'
        }
        self.dark_colors = {
            'bg': '#2c3e50',
            'fg': 'white',
            'btn': '#34495e',
            'entry': '#34495e'
        }
        self.update_colors()

    def create_gui_components(self):
        # Creating the gui elements
        # Create header, list, and control frames
        self.header_frame = tk.Frame(self, bg=self.colors['bg'])
        self.header_frame.pack(pady=10, fill=tk.X)

        self.list_frame = tk.Frame(self, bg=self.colors['bg'])
        self.list_frame.pack(pady=20, fill=tk.BOTH, expand=True)

        self.controls_frame = tk.Frame(self, bg=self.colors['bg'])
        self.controls_frame.pack(pady=10, fill=tk.X)

        # Header Frame Widgets
        self.mode_button = tk.Button(self.header_frame, text="Toggle Dark Mode", command=self.toggle_mode,
                                     bg=self.colors['btn'], fg=self.colors['fg'])
        self.mode_button.pack(side=tk.RIGHT, padx=10)

        # List Frame Widgets: Use Treeview for structured data presentation
        self.columns = ("Header", "Description", "Date")
        self.item_treeview = ttk.Treeview(self.list_frame, columns=self.columns, show="headings")
        for col in self.columns:
            self.item_treeview.heading(col, text=col)
            self.item_treeview.column(col, width=150)

        self.item_treeview.pack(fill=tk.BOTH, expand=True, padx=10)

        # Control Frame Widgets
        self.add_item_entry = tk.Entry(self.controls_frame, width=50, bg=self.colors['entry'], fg=self.colors['fg'])
        self.add_item_entry.pack(pady=10)

        self.add_item_button = tk.Button(self.controls_frame, text="Add Item", command=self.add_item,
                                         bg=self.colors['btn'], fg=self.colors['fg'])
        self.add_item_button.pack(pady=10)

        self.modify_dropdown = ttk.Combobox(self.controls_frame, values=self.get_items())
        self.modify_dropdown.pack(pady=10)

        self.remove_item_button = tk.Button(self.controls_frame, text="Remove Item", command=self.remove_item,
                                            bg=self.colors['btn'], fg=self.colors['fg'])
        self.remove_item_button.pack(pady=5)

        self.modify_item_button = tk.Button(self.controls_frame, text="Modify Item", command=self.modify_item_dialog,
                                            bg=self.colors['btn'], fg=self.colors['fg'])
        self.modify_item_button.pack(pady=5)

    # Updates the colors based off previously defined color codes
    def update_colors(self):
        self.colors = self.dark_colors if self.dark_mode else self.light_colors

    # Controls the light and dark mode
    def toggle_mode(self):
        self.dark_mode = not self.dark_mode
        self.update_colors()
        self.config(bg=self.colors['bg'])
        self.header_frame.config(bg=self.colors['bg'])
        self.list_frame.config(bg=self.colors['bg'])
        self.controls_frame.config(bg=self.colors['bg'])
        self.add_item_entry.config(bg=self.colors['entry'], fg=self.colors['fg'])
        self.add_item_button.config(bg=self.colors['btn'], fg=self.colors['fg'])
        self.remove_item_button.config(bg=self.colors['btn'], fg=self.colors['fg'])
        self.modify_item_button.config(bg=self.colors['btn'], fg=self.colors['fg'])
        self.mode_button.config(bg=self.colors['btn'], fg=self.colors['fg'])

    def get_items(self):
        # Gets header using list comprehension
        return [item.header for item in self.todo.TodoList]

    def update_display(self):
        # Updates display in treeview
        for row in self.item_treeview.get_children():
            self.item_treeview.delete(row)
        for item in self.todo.TodoList:
            self.item_treeview.insert("", "end", values=(item.header, item.description, item.date))
        self.modify_dropdown['values'] = self.get_items()
        self.save_file()  # saves to file

    # Add item to the to do list
    def add_item(self):
        header = self.add_item_entry.get()
        if header:
            self.todo.add_item(header)
            self.add_item_entry.delete(0, tk.END)
            self.update_display()
            self.save_file()

    # Remove item from the to do list via drop down menu
    def remove_item(self):
        selected_item = self.modify_dropdown.get()
        if selected_item:
            index = self.get_items().index(selected_item)
            self.todo.remove_item(index)
            self.update_display()

    # Open dialog to modify an item
    def modify_item_dialog(self):
        selected_item = self.modify_dropdown.get()
        if selected_item:
            index = self.get_items().index(selected_item)
            item = self.todo.TodoList[index]

            new_header = simpledialog.askstring("Modify Item", "Enter new header:", initialvalue=item.header)
            if new_header:
                item.add_header(new_header)

            new_description = simpledialog.askstring("Modify Item", "Enter new description:",initialvalue=item.description)
            if new_description:
                item.add_description(new_description)

            new_date = simpledialog.askstring("Modify Item", "Enter new date:", initialvalue=item.date)
            if new_date:
                item.add_date(new_date)

            self.update_display()
            self.save_file()

    # Saves to do list to a file
    def save_file(self, filename='todo_list.json'):
        with open(filename, 'w') as file:
            serialized_items = [{'header': item.header, 'description': item.description, 'date': item.date} for item in
                                self.todo.TodoList]
            json.dump(serialized_items, file)

    # Loads the last state of the to list from a file which then reconstructs
    def load_from_file(self, filename='todo_list.json'):
        try:
            with open(filename, 'r') as file:
                serialized_items = json.load(file)
                # Convert the serialized format back to todo items
                for item_data in serialized_items:
                    item = Item(header=item_data['header'])
                    item.add_description(item_data['description'])
                    item.add_date(item_data['date'])
                    self.todo.TodoList.append(item)
                    self.todo.length += 1
        except FileNotFoundError:
            pass


if __name__ == "__main__":
    app = TodoApp()
    app.mainloop()
