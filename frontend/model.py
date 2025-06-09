class User:
    def __init__(self, name, nickname, password):
        self.name = name
        self.nickname = nickname
        self.password = password


class Filament:
    def __init__(self, id, color, supplier, description, amount, activate):
        self.id = id
        self.color = color
        self.supplier = supplier
        self.description = description
        self.amount = amount
        self.activate = activate
