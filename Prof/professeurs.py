from Administration.enregistrement import Ecole

class Professeurs(Ecole):
    __tablename__ = "Professeurs"

    def __init__(self, nom, prenom, age, metier, matier, classe):
        self.matier = matier
        self.classe = classe
        super().__init__(nom, prenom, age, metier)

    def _nom(self):
        return super()._nom()
    
    def _prenom(self):
        return super()._prenom()
    
    def get_age(self):
        return super().get_age
    
    def metier(self):   
        return super().metier()

    def to_dict(self):
        data = super().to_dict()
        data['matier'] = self.matier
        data['classe'] = self.classe
        return data

    
    def __str__(self):
        return super().__str__()    
if __name__ == "__main__":
    pr = Professeurs(nom='rk', prenom='kl', age=22, metier='', matier=['0,0 f,f f',], classe='termia, .d nl')
    print(pr.to_dict())