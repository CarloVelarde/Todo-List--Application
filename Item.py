class Item:
    def __init__(self, header):
        self.header = header
        self.description = None
        self.date = None

    def add_description(self, description):
        if not isinstance(description, str):
            return False
        self.description = description
        return True

    def add_date(self, param: str):
        if not isinstance(param, str):
            return False
        self.date = param
        return True

    def add_header(self, header):
        if not isinstance(header, str):
            return False
        self.header = header
        return True



