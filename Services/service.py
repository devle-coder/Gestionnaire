from Eleves.eleve import Eleve
from database.database import Database, RepotStudents, RepotProfs, RepotPersonnels


class Service:

    __tablename__ = 'Service'

    def __init__(self, db=None):
        if db is None:
            self.base = Database()
        else:
            self.base = db
    @staticmethod
    def __checker__(objet):
        if objet.__tablename__ == 'Personnels':
            return 1

        elif objet.__tablename__ == 'Professeurs':
            return 2

        elif objet.__tablename__ == 'Eleves':
            return 3

        else: return 0

    @staticmethod
    def verifie_les_informations_des_eleves(objet) -> bool:
        objet = objet.to_dict()
        nom = objet.get('nom', '')
        prenom = objet.get('prenom', '')
        if not isinstance(nom, str)\
                or not isinstance(prenom, str)\
                or not isinstance(objet.get('age', 0), int)\
                or not isinstance(objet.get('metier', 0), str)\
                or not isinstance(objet.get('classe', 0), str):
            return False
        elif len(nom) < 3 or len(prenom) < 3:
            return False
        return True

    @staticmethod
    def __verifie_les_information_des_profs__(objet) -> bool:
        objet = objet.to_dict()
        nom = objet.get('nom', '')
        prenom = objet.get('prenom', '')
        age = objet.get('age', 0)
        metier = objet.get('metier', '')
        matier = objet.get('matier', '')
        classe = objet.get('classe', '')
        if not isinstance(nom, str)\
                or not isinstance(prenom, str)\
                or not isinstance(age, int)\
                or not isinstance(metier, str)\
                or not isinstance(matier, str)\
                or not isinstance(classe, str):
            return False
        elif len(nom) < 3 or len(prenom) < 3:
            return False
        return True

    @staticmethod
    def __verifie_les_informations_du_personnels__(objet) ->bool:
        objet = objet.to_dict()
        nom = objet.get('nom', '')
        prenom = objet.get('prenom', '')
        age = objet.get('age', 0)
        metier = objet.get('metier', '')
        if not isinstance(nom, str)\
                or not isinstance(prenom, str)\
                or not isinstance(age, int)\
                or not isinstance(metier, str):
            return False
        if len(nom) < 3 or len(prenom) < 3:
            return False
        return True

    def save_personel(self, objet):

        base = RepotPersonnels(self.base)

        if self.__checker__(objet) == 1:
            if self.__verifie_les_informations_du_personnels__(objet):
                base.save_person(objet)
                return True
            raise ValueError("Information incomplete")
        raise False

    def save_tech(self, objet):

        base = RepotProfs(self.base)
        if self.__checker__(objet) == 2:
            if self.__verifie_les_information_des_profs__(objet):
                base.save_prof(objet)
                return True
            raise ValueError("Information incomplete")
        raise False

    def save_student(self, objet):

        base = RepotStudents(self.base)
        if self.__checker__(objet) == 3:
            if self.verifie_les_informations_des_eleves(objet):
                base.save_student(objet)
                return True
            raise ValueError("Information incomplete")
        raise False


    def delete_eleve_by_id(self, id):
        base = RepotStudents(self.base)
        return base.delete_student(int(id))



    def get_eleves(self):
        base = RepotStudents(self.base)
        return base.get_all_students



    def get_eleve_by_id(self, id):
        base = RepotStudents(self.base)
        return base.get_student_by_id(int(id))


    def get_profs(self):
        base = RepotProfs(self.base)
        return base.get_all_profs()

    def get_prof_by_id(self, id):
        base = RepotProfs(self.base)
        return base.get_prof_by_id(int(id))

    def delete_prof_by_id(self, id):
        base = RepotProfs(self.base)
        return base.delete_prof_by_id(int(id))



    def get_personnels(self):
        base = RepotPersonnels(self.base)
        return base.get_all_persons()

    def get_personnel_by_id(self, id):
        base = RepotPersonnels(self.base)
        return base.get_person_by_id(int(id))

    def delete_personnel_by_id(self, id):
        base = RepotPersonnels(self.base)
        return base.delete_personnel_by_id(int(id))






if __name__ == '__main__':
    el = Eleve('sal', 'touré', 23, 'student', 'L1')
    ser = Service()
    print(ser.get_profs())


