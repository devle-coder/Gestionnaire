import sqlite3
import os

CURRENT_DIR = os.path.dirname(os.path.realpath(__file__))
DIR_PATH = os.path.join(CURRENT_DIR, '../data/DATABASE.db')



class Base:
    def __init__(self):
        # si la base de données n'est pas fournie ont utilise DATABASE.db #
        self.conn = sqlite3.connect(DIR_PATH)
        self.cursor = self.conn.cursor()

    def __table__(self, User):
        self.cursor.execute("""CREATE TABLE IF NOT exists User (
    id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    nom VARCHAR,
    prenom VARCHAR,
    age INTEGER,
    metier VARCHAR
    );
    """)
        self.cursor.execute('INSERT INTO User (nom,prenom,age,metier) VALUES (:nom, :prenom, :age, :metier)',User)
        self.conn.commit()
        self.conn.close()
        return


    def save_student(self,student) :
        data ={
            'nom': student.nom,
            'prenom': student.prenom,
            'age': student.age,
            'metier': student.metier
        }
        self.__table__(data)
        return True


    def get_student_nom(self,nom):
        data = self.cursor.execute("""SELECT * FROM User """).fetchall()
        user = [row for row in data if row[1] == nom]
        return user

    def get_student_by_id(self,id):
        data = self.cursor.execute("""SELECT * FROM User """).fetchall()
        user = [row for row in data if row[0] == id]
        self.conn.close()
        return user

    def get_all_students(self):
        data = self.cursor.execute("""SELECT * FROM User """).fetchall()
        self.conn.close()
        if data:
            return data
        return None

    def delete_student(self,id):
        self.cursor.execute("""DELETE FROM User where id == ? """,(id,))
        self.conn.commit()
        self.conn.close()
        if self.cursor.rowcount > 0:
            return True
        else:
            return False


if __name__ == '__main__':
    base = Base()
    #print(base.get_student_by_id(0))
    #print(base.delete_student(0))
    # print(base.get_student_nom(d.nom))
    #print(base.get_students())
    #print(base.save_student(d))
    print(base.__dict__)