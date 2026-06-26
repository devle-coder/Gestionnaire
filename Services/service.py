from Administration.enregistrement import Ecole
from Eleves.eleve import Eleve
from Personnel.personnel import personnels
from Prof.professeurs import Professeurs
from database.database import Base


class Servicec:
    __tablename__ = 'service'


print(Servicec.__tablename__)


# class Service:
#     class Eleve:
#         def __init__(self, nom, prenom, age, metier):
#             self.nom = nom
#             self.prenom = prenom
#             self._age = age
#             self.metier = metier
#             super().__init__(nom=nom,prenom=prenom, age=age, metier=metier)
#
#         def __str__(self):
#             return super().__str__()
#
#
# print(Service.Eleve)



