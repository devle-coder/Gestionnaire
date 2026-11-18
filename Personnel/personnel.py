from Administration.enregistrement import Ecole

class Personnels(Ecole):
    __tablename__ = 'Personnels'

    def __init__(self, nom, prenom, age, metier):
        super().__init__(nom, prenom, age, metier)

    def _nom(self):
        return f"Nom: {super().nom()}"
    
    def _prenom(self):
        return f"Prenom: {super().prenom()}" # pyright: ignore[reportCallIssue]
    
    def get_age(self):
        return f"Age: {super().get_age}"
    
    def metier(self):
        return f"Métier: {super().metier()}"
    
    def __str__(self):
        return super().__str__()

    def to_dict(self) :
        data = super().to_dict()
        return data

if __name__ == '__main__':
    personnels = Personnels('ali','issa',22,"main-d'œuvre")
    print(personnels)
    print(personnels.to_dict())
    
    
