from Administration.enregistrement import Ecole

class Eleve(Ecole):
    def __init__(self, nom, prenom, age, metier, classe, note, id=None):
        self.note = note
        self.classe = classe
        super().__init__(nom, prenom, age, metier,_id=id)

    def _nom(self):
        return f"Mon nom est: {super()._nom()}"
    
    def _prenom(self):
        return f"Mon prenom est: {super()._prenom()}"
    
    def get_age(self):
        return f"Mon get_age est: {super().get_age}"
    
    def metier(self):
        return f"Métier: {super().metier()}"
    
    def __str__(self):
        return super().__str__()

if __name__ == '__main__':
    pass




    
    
    