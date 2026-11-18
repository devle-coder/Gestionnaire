import sqlite3
import os
from sqlite3 import Error

from  Eleves.eleve import Eleve
from Personnel.personnel import Personnels
from Prof.professeurs import Professeurs

CURRENT_DIR = os.path.dirname(os.path.realpath(__file__))
DIR_PATH = os.path.join(CURRENT_DIR, '../data/DATABASE.db')


class Database:
    __tablename__ = 'DATABASE'
    def __init__(self, db_path=DIR_PATH):
        self.db_path = db_path
        self.conn = None

    def __enter__(self):
        self.conn = sqlite3.connect(self.db_path)
        return self


    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.conn:
            self.conn.close()



class RepotStudents:
    __tablename__ = 'RepotStudents'
    def __init__(self, db: Database):
        self.db = db

    def create_table(self):
        query = """CREATE TABLE IF NOT exists Student (
                    id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
                    nom TEXT,
                    prenom TEXT,
                    age INTEGER,
                    metier TEXT,
                    classe TEXT,
                    image BLOB
                    
                    );
    """
        with self.db as db:
            try:
                db.conn.execute(query)
                db.conn.commit()
                return True
            except Error as e :
                return str(e)




    def save_student(self,student) :
        data ={
            'nom': student.nom,
            'prenom': student.prenom,
            'age': student.age,
            'metier': student.metier,
            'classe': student.classe,
        }
        query = """
                INSERT INTO Student (nom, prenom, age, metier, classe) VALUES (:nom, :prenom, :age, :metier, :classe)
        """
        if self.create_table():
            with self.db as db:
                db.conn.execute(query, data)
                db.conn.commit()
                return True
        return False


    def get_student_nom(self, nom : str):
        query = """SELECT * FROM Student WHERE nom == ?
         """
        with self.db as db:
            try:
                data = db.conn.execute(query, (nom,)).fetchall()
                return data
            except Error as e :
                return str(e)



    def get_student_by_id(self, id : int):
        query = f"""SELECT * FROM Student WHERE id == ?
                 """
        with self.db as db:
            try:
                data = db.conn.execute(query, (id,)).fetchall()
                return data
            except Error as e:
                return str(e)

    @property
    def get_all_students(self):
        query = f"""SELECT * FROM Student"""
        self.create_table()
        with self.db as db:
            try:
                return db.conn.execute(query).fetchall()
            except Error as e :
                return str(e)


    def delete_student(self, id : int):
        query = f"""DELETE FROM Student WHERE id == ?
                         """
        with self.db as db:
            try:
                db.conn.execute(query, (id,))
                db.conn.commit()
                return True
            except Error as e:
                return str(e)


class RepotProfs:
    __tablename__ = 'Professeurs'

    def __init__(self, db : Database):
        self.db = db


    def create_table(self):
        query = """CREATE TABLE IF NOT exists Professeurs (
                    id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
                    nom TEXT,
                    prenom TEXT,
                    age INTEGER,
                    metier TEXT,
                    matiere TEXT,
                    classe TEXT
                    );
    """
        with self.db as db:
            try:
                db.conn.execute(query)
                db.conn.commit()
                return True
            except Error as e:
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

        query = """
            INSERT INTO Professeurs (nom, prenom, age, metier, matiere, classe) VALUES (:nom, :prenom, :age, :metier, :matiere, :classe)
        """
        if self.create_table():
            with self.db as db:
                try:
                    db.conn.execute(query, data)
                    db.conn.commit()
                    return True
                except Error as e :
                    return str(e)
        return False


    def get_prof_by_nom(self, nom : str) :
        query = """SELECT * FROM Professeurs WHERE nom == ?
                 """
        with self.db as db:
            try:
                data = db.conn.execute(query, (nom,)).fetchall()
                return data
            except Error as e:
                return str(e)



    def get_prof_by_id(self, id : int) :
        query = """SELECT * FROM Professeurs WHERE id == ?
                         """
        with self.db as db:
            try:
                data = db.conn.execute(query, (id,)).fetchall()
                return data
            except Error as e:
                return str(e)



    def get_all_profs(self) :
        query = """SELECT * FROM Professeurs
                        """
        self.create_table()
        with self.db as db:
            try:
                data = db.conn.execute(query).fetchall()
                return data
            except Error as e:
                return str(e)



    def delete_prof_by_id(self, id) :
        query = f"""DELETE FROM Professeurs WHERE id == ?
                                 """
        with self.db as db:
            try:
                db.conn.execute(query, (id,))
                db.conn.commit()
                return True
            except Error as e:
                return str(e)




class RepotPersonnels:
    __tablename__ = 'Personnels'
    def __init__(self, db : Database):
        self.db = db

    def create_table(self):
        query = """CREATE TABLE IF NOT exists Personnels (
                    id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
                    nom TEXT,
                    prenom TEXT,
                    age INTEGER,
                    metier TEXT
                    
                    );
    """
        with self.db as db:
            try:
                db.conn.execute(query)
                db.conn.commit()
                return True
            except Error as e:
                return str(e)

    def save_person(self, person):
        data ={
            'nom' : person.nom,
            'prenom' : person.prenom,
            'age' : person.age,
            'metier' : person.metier,

        }
        query = """
                INSERT INTO Personnels (nom, prenom, age, metier) VALUES (:nom, :prenom, :age, :metier)        
        """
        self.create_table()
        with self.db as db:
            try:
                db.conn.execute(query, data)
                db.conn.commit()
                return True
            except Error as e:
                return str(e)

    def get_person_nom(self, nom) :
        query = """SELECT * FROM Personnels WHERE nom == ?
                         """
        with self.db as db:
            try:
                data = db.conn.execute(query, (nom,)).fetchall()
                return data
            except Error as e:
                return str(e)

    def get_person_by_id(self, id) :
        query = """SELECT * FROM Personnels WHERE id == ?
                         """
        with self.db as db:
            try:
                data = db.conn.execute(query, (id,)).fetchall()
                return data
            except Error as e:
                return str(e)

    def get_all_persons(self) :
        query = """SELECT * FROM Personnels 
                         """
        self.create_table()
        with self.db as db:
            try:
                data = db.conn.execute(query).fetchall()
                return data
            except Error as e:
                return str(e)

    def delete_personnel_by_id(self, id) :
        query = """
                DELETE FROM Personnels WHERE id == ?
                """
        with self.db as db:
            try:
                db.conn.execute(query, (id,)).fetchone()
                db.conn.commit()
                return True
            except Error as e:
                return str(e)







if __name__ == '__main__':
    base =Database()
    repot_stn = RepotProfs(base)

    eleve = Professeurs(nom='sa',prenom='i',age=32, metier='L',classe='P', matier='Chimie')
    eve = Professeurs(nom='sa', prenom='i', age=32, metier='L', classe='P', matier='Chimie')
    eleve2 = Eleve(nom='ALI', prenom='ISSA', age=32, metier='L', classe='P')
    per = Personnels(nom='sa',prenom='i',age=32, metier='L')

    print(repot_stn.get_all_profs())
