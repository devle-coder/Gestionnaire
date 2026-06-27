from Administration.enregistrement import Ecole

class Personnels(Ecole):
    def __init__(self, nom, prenom, age, metier):
        super().__init__(nom, prenom, age, metier)

    def _nom(self):
        return f"Nom: {super().nom()}"
    
    def _prenom(self):
        return f"Prenom: {super().prenom()}"
    
    def get_age(self):
        return f"Age: {super().get_age}"
    
    def metier(self):
        return f"Métier: {super().metier()}"
    
    def __str__(self):
        return super().__str__()

    def save_student(self,student) :
        data = dict()
        data['id'] = student.id
        data['nom'] = student.nom
        data['prenom'] = student.prenom
        data['age'] = student.age
        data['metier'] = student.metier
        return data

if __name__ == '__main__':
    personnels = Personnels('s','d',2,'d')
    print(personnels)
    print(personnels.save_student(personnels))
    
    
