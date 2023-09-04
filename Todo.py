from Item import Item


class Todo:
    def __init__(self, name):
        self.name = name
        self.TodoList = []
        self.length = 0

    # Add a to-do item to list
    def add_item(self, header):
        new_item = Item(header)
        self.TodoList.append(new_item)
        self.length += 1

    # Take an index of what item to remove from the list
    def remove_item(self, index):
        if self.length > index >= 0:
            self.TodoList.pop(index)
            self.length -= 1
            return True

        return False

    # Changes to do list title
    def change_name(self, name):
        self.name = name
