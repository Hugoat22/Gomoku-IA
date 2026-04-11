class IA:
    def __init__(self, Attaque, Defense, Profondeur) -> None:
        self.Attaque = Attaque
        self.Defense = Defense
        self.Profondeur = Profondeur

    def taux(self) -> list[int | float]:
        return [self.Attaque,self.Defense]