from Administration.enregistrement import Ecole

class Professeurs(Ecole):
    def __init__(self, nom, prenom, age, metier, matier):
        self.matiere = list(matier)
        self.metier = list(metier)
        super().__init__(nom, prenom, age, metier)
        self.metier = metier

    def _nom(self):
        return super().nom()
    
    def _prenom(self):
        return super().prenom()
    
    def get_age(self):
        return super().get_age
    
    def metier(self):   
        return super().metier()

    def matier(self):
        return self.matiere
    
    def __str__(self):
        return super().__str__()    
