

from Administration.enregistrement import Ecole

class Eleve(Ecole):

    __tablename__ = 'Eleves'

    def __init__(self, nom, prenom, age, metier, classe, id=None):
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

    def to_dict(self):
        data = super().to_dict()
        data['metier'] = self.metier
        data['classe'] = self.classe



        return data
    
    def __str__(self):
        return super().__str__()

if __name__ == '__main__':
    eleve = Eleve('Ali', 'moussa', 23,'Etudiant' ,"Terminale")
    print(eleve.to_dict())




    
    
    