class IA:
    def __init__(self,Attaque : int | float ,Defense : int | float) -> None:
        self.Attaque = Attaque
        self.Defense = Defense

    def taux(self) -> list[int | float]:
        return [self.Attaque,self.Defense]