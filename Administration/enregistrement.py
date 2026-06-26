
class ErreurPersonne(Exception):
    pass

class Ecole:
    _id = 0
    def __init__(self, nom: str, prenom: str, age: int, metier: str, _id=None):
        if _id is None:
            self.id = Ecole._id
            Ecole._id = Ecole._id + 1

        self.nom = nom
        self.prenom = prenom
        self.age = age
        self.metier = metier



    def to_dict(self) :
        return {
            "id" : self.id,
            "nom" : self.nom,
            "prenom" : self.prenom,
            "age" : self.age,
            "métier" : self.metier,
        }



    def _nom(self):
        caracter = " -'"
        resultat = all(c.isalpha() or c in caracter for c in self.nom)
        if resultat:
            return self.nom
        raise ErreurPersonne("Nom invalide")


    def _prenom(self):
        caracter = " -'"
        resultat = all(c.isalpha() or c in caracter for c in self.prenom)
        if resultat:
            return self.prenom
        raise ErreurPersonne("Prenom invalide")


    def metier(self):
        return self.metier


    @property
    def get_age(self):
        return self.age

    def get_user(self):
        return f"{self.nom,} {self.prenom}, {self.age}, {self.metier}"


    def __str__(self):
        return f"ID : {self._id} | Nom : {self.nom} | Prenom : {self.prenom} | age : {self.age} | Métier : {self.metier}"

if __name__ == '__main__':
    print(Ecole.__dict__)
