class User:
    def __init__(self, name, nickname, password):
        self.name = name
        self.nickname = nickname
        self.password = password


class Filament:
    def __init__(self, id, color, brand, description, amount, activate):
        self.id = id
        self.color = color
        self.brand = brand
        self.description = description
        self.amount = amount
        self.activate = activate
