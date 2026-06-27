import sqlite3
import os
from  Eleves.eleve import Eleve


CURRENT_DIR = os.path.dirname(os.path.realpath(__file__))
DIR_PATH = os.path.join(CURRENT_DIR, '../data/DATABASE.db')



class Base:
    __base__ = 'DATABASE'
    def __init__(self) :
        self.conn = sqlite3.connect(DIR_PATH)
        self.cursor = self.conn.cursor()

    class Student :
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
        notes INTEGER
        );
        """)
            self.cursor.execute('INSERT INTO Student (nom,prenom,age,metier,classe,notes) VALUES (:nom, :prenom, :age, :metier,:classe,:notes)',User)
            self.conn.commit()
            self.conn.close()
            return


        def save_student(self,student) :
            data ={
                'nom': student.nom,
                'prenom': student.prenom,
                'age': student.age,
                'metier': student.metier,
                'classe': student.classe,
                'notes': student.note
            }
            self.__table__(data)
            return student


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


    class Prof :
        def __init__(self):
            self.conn = Base().conn
            self.cursor = Base().cursor
        def __table__(self, prof):
            self.cursor.execute("""CREATE TABLE IF NOT exists Prof (
        id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
        nom VARCHAR,
        prenom VARCHAR,
        age INTEGER,
        metier VARCHAR,
        classe VARCHAR,
        matier VARCHAR
        );
        """)
            self.cursor.execute('INSERT INTO Student (nom,prenom,age,metier,classe,matier) VALUES (:nom, :prenom, :age, :metier,:classe,:matier)',prof)
            self.conn.commit()
            self.conn.close()
            return



if __name__ == '__main__':
    base = Base.Student()
    eleve = Eleve(nom='issa',prenom='mike',age=33,metier='student',classe='second',note=10)
    print(base.get_all_students())
