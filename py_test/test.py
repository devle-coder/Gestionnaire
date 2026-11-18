import unittest

from Eleves.eleve import Eleve
from Personnel.personnel import Personnels
from Prof.professeurs import Professeurs



class ProfesseursTest(unittest.TestCase):
    def test_get_all_profs(self):
        p = Professeurs('dj', 'lm', 22, 'd', 'd','d')
        assert(p.get_age())
        assert(p.to_dict()['age'] == 22)
        assert (p.prenom)

    def test_eleve(self):
        e = Eleve('m', 'd',22,'2', 2,4)
        assert(e.to_dict())

    def test_personnel(self):
        p = Personnels('dj', 'lm', 22, 'd')
        assert(p.get_age())
        assert(p.to_dict())
        assert (p.prenom)
        assert (p.nom)



if __name__ == '__main__':
    unittest.main()
    