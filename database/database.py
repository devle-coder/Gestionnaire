import sqlite3
import os
import traceback
from sqlite3 import Error


from  Eleves.eleve import Eleve
from Prof.professeurs import Professeurs


CURRENT_DIR = os.path.dirname(os.path.realpath(__file__))
DIR_PATH = os.path.join(CURRENT_DIR, '../data/DATABASE.db')



class Base:
    __tablename__ = 'DATABASE'
    conn = sqlite3.connect(DIR_PATH)
    cursor = conn.cursor()

    def __enter__(self):
        return self


    class Student :
        __tablename__ = 'Student'

        def __init__(self):
            self.conn = Base().conn
            self.cursor = Base().cursor

        def __table__(self, User):
            self.cursor.execute("""CREATE TABLE IF NOT exists Student (
        id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
        nom VARCHAR,
        prenom VARCHAR,
        age INTEGER,
        metier VARCHAR,
        classe VARCHAR,
        note INTEGER
        );
        """)
            try:
                self.cursor.execute('INSERT INTO Student (nom,prenom,age,metier,classe,note) VALUES (:nom, :prenom, :age, :metier,:classe,:note)',User)
                self.conn.commit()
                self.conn.close()
                return True
            except Error as e:
                return str(e)



        def save_student(self,student) :
            data ={
                'nom': student.nom,
                'prenom': student.prenom,
                'age': student.age,
                'metier': student.metier,
                'classe': student.classe,
                'note': student.note
            }
            if self.__table__(data):
                return True
            return False


        def get_student_nom(self,nom):
            data = self.cursor.execute("""SELECT * FROM Student """).fetchall()
            user = [row for row in data if row[1] == nom]
            return user

        def get_student_by_id(self,id):
            data = self.cursor.execute("""SELECT * FROM Student """).fetchall()
            user = [row for row in data if row[0] == id]
            self.conn.close()
            return user if user else 'Student not found'

        def get_all_students(self):
            data = self.cursor.execute("""SELECT * FROM Student """).fetchall()
            self.conn.close()
            if data:
                return data
            return None

        def delete_student(self,id):
            self.cursor.execute("""DELETE FROM Student where id == ? """,(id,))
            self.conn.commit()
            self.conn.close()
            if self.cursor.rowcount > 0:
                return True
            else:
                return False

    class Professeurs:
        __tablename__ = 'Professeurs'

        def __init__(self):
            super().__init__()
            self.conn = Base().conn
            self.cursor = Base().cursor


        def __table__(self, User) :
            self.cursor.execute("""CREATE TABLE IF NOT exists Professeurs (
        id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
        nom VARCHAR,
        prenom VARCHAR,
        age INTEGER,
        metier VARCHAR,
        classe VARCHAR,
        matiere INTEGER
        
        );
        """)
            try :
                self.cursor.execute(
                    'INSERT INTO Professeurs (nom,prenom,age,metier,matiere,classe) VALUES (:nom, :prenom, :age, :metier,:matiere,:classe)',
                    User)
                self.conn.commit()
                self.conn.close()
                return True
            except Error as e :
                return str(e)

        def save_prof(self, profs):
            data ={
                'nom' : profs.nom,
                'prenom' : profs.prenom,
                'age' : profs.age,
                'metier' : profs.metier,
                'matiere' : profs.matier,
                'classe' : profs.classe
            }
            if self.__table__(data):
                return True
            return False

        def get_prof_nom(self, nom) :
            data = self.cursor.execute("""SELECT * FROM Professeurs """).fetchall()
            user = [row for row in data if row[1] == nom]
            return user

        def get_prof_by_id(self, id) :
            data = self.cursor.execute("""SELECT * FROM Professeurs """).fetchall()
            user = [row for row in data if row[0] == id]
            self.conn.close()
            return user if user else 'Student not found'

        def get_all_profs(self) :
            data = self.cursor.execute("""SELECT * FROM Professeurs """).fetchall()
            self.conn.close()
            if data :
                return data
            return None

        def delete_prof(self, id) :
            self.cursor.execute("""DELETE FROM Professeurs where id == ? """, (id,))
            self.conn.commit()
            self.conn.close()
            if self.cursor.rowcount > 0 :
                return True
            else :
                return False

        def __exit__(self, exc_type, exc_val, exc_tb):
            self.conn.close()





if __name__ == '__main__':
    repot_stn = Base().Student()
    repot_prof = Base().Professeurs()

    eleve = Eleve(nom='sa',prenom='i',age=32, metier='L',classe='P',note=21)
    prof = Professeurs('djibril', 'daoud',41, 'prof', 'anglais', 'L3')


    try:

        repot_prof.save_prof(prof)
    except Exception as e :
        print(e)
    else:
        print('operation ok')



