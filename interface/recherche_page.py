from PySide6 import QtCore, QtWidgets
from PySide6.QtCore import QSize, QRect
from PySide6.QtGui import QPixmap, Qt
from PySide6.QtWidgets import (QLabel, QHBoxLayout, QVBoxLayout, QWidget, QApplication, QPushButton,
                               QLineEdit, QListWidget, QButtonGroup, QRadioButton, QMessageBox)

from Services.service import Service
import sys

class RecherchePage(QWidget):
    retour_demande = QtCore.Signal()

    def __init__(self):
        super().__init__()
        self.form = None
        self.radio_eleve = None
        self.radio_prof = None
        self.radio_perso = None
        self.champ_recherche = None
        self.listes_apercu = None



        self.setWindowTitle("Recherche")
        self.setGeometry(800, 400, 800, 400)
        self.setup_ui()
        self.connexion()

    def setup_ui(self):
        main_layout = QVBoxLayout(self)
        layout_btn = QHBoxLayout()
        main_layout.addLayout(layout_btn)

        self.BtnRetour = QPushButton("Retour")
        layout_btn.addWidget(self.BtnRetour)


        layout_radio = QVBoxLayout() # < page
        layout_radio.setContentsMargins(16, 16, 16, 16)
        layout_radio.setSpacing(12)
        st = """background-color: #298E75FF; border: 3px solid #334155; border-radius: 5px, 5px;"""

        self.radio_eleve = QRadioButton("Élève")
        self.radio_eleve.setStyleSheet(st)
        self.radio_prof = QRadioButton("Prof")
        self.radio_prof.setStyleSheet(st)
        self.radio_perso = QRadioButton("Personnel")
        self.radio_perso.setStyleSheet(st)
        self.radio_prof.setChecked(True)

        self.radio_group = QButtonGroup(self)

        self.radio_group.addButton(self.radio_eleve)
        self.radio_group.addButton(self.radio_prof)
        self.radio_group.addButton(self.radio_perso)

        layout_btn.addWidget(self.radio_eleve)
        layout_btn.addWidget(self.radio_prof)
        layout_btn.addWidget(self.radio_perso)



        main_layout.addStretch()

        layout_champ = QHBoxLayout()

        layout_champ.addWidget(self.recherche_champ())
        layout_champ.addWidget(self.affichageInfo())
        main_layout.addLayout(layout_champ)

    def recherche_champ(self):
        card = QWidget()
        card.setStyleSheet(
            "background-color: #151E32; border: 1px solid #334155; border-radius: 20px;"
        )
        layout = QVBoxLayout(card)

        self.champ_recherche = QLineEdit()
        self.champ_recherche.setPlaceholderText(f"Recherche..., Nom ou ID")
        self.champ_recherche.setStyleSheet("padding:6px; border-radius:8px; background-color:#0F1724; color:#F1F5F9;")

        self.listes_apercu = QListWidget()


        self.listes_apercu.setStyleSheet("font-size: 20px; font-weight: 700; color: B2F6A1;")
        layout.addWidget(self.champ_recherche)

        layout.addWidget(self.listes_apercu)
        layout.addStretch()
        return card

    def affichageInfo(self):

        conteneur = QtWidgets.QFrame()

        conteneur.setMinimumHeight(300)
        conteneur.setMinimumWidth(300)
        conteneur.setStyleSheet(
            "background-color: #151E32; border: 1px solid #334155; border-radius: 20px;"
        )
        conteneur.setContentsMargins(QtCore.QMargins(10, 10, 10, 10))

        layout = QVBoxLayout(conteneur)

        self.form = QtWidgets.QFormLayout()


        layout.addLayout(self.form)

        return conteneur

    def check_btn_clicked(self, bouton):
        self.apercu_des_users()
        self.deletelater(self.form)
        return bouton.text()



    def connexion(self):
        self.apercu_des_users()
        self.BtnRetour.clicked.connect(self.retour_demande.emit)
        self.champ_recherche.textChanged.connect(self.filtrer_apercu)

        self.listes_apercu.itemClicked.connect(self.get_user_click)
        self.radio_group.buttonClicked.connect(self.check_btn_clicked)



    # ajouter les elements de l'aperçue
    def apercu_des_users(self):
        items = self.get_users()

        self.listes_apercu.clear()
        if isinstance(items, list):
            for i in items:
                text = f"ID: {i[0]}: {i[1]}  {i[2]}"
                item = QtWidgets.QListWidgetItem(text)
                item.setData(QtCore.Qt.UserRole, i[0])
                item.setData(QtCore.Qt.UserRole + 1, self.get_choix())
                self.listes_apercu.addItem(item)


    def get_choix(self):
        bouton = self.radio_group.checkedButton()
        if bouton is None:
            return "Prof"
        return bouton.text()


    def get_users(self):
        service = Service()
        choix = self.get_choix()
        if choix == "Élève":
            return service.get_eleves()
        if choix == "Prof":
            return service.get_profs()
        if choix == "Personnel":
            return service.get_personnels()
        return service.get_eleves()


    def get_user_click(self, item):
        user_click = item.data(QtCore.Qt.UserRole)
        choix = item.data(QtCore.Qt.UserRole + 1)
        service = Service()
        if choix == "Élève":
            users = service.get_eleve_by_id(int(user_click))
        elif choix == "Prof":
            users = service.get_prof_by_id(int(user_click))
        elif choix == "Personnel":
            users = service.get_personnel_by_id(int(user_click))
        else:
            users = []

        if isinstance(users, list) and users:
            user = users[0]
            ID = user[0]
            nom = user[1]
            prenom = user[2]
            age = user[3]
            metier = user[4]

            self.deletelater(self.form)
            self.form.addRow("<b>ID</b>", QLabel(f"<b>{ID}</b>"))
            self.form.addRow("<b>Nom</b>", QLabel(f"<b>{nom}</b>"))
            self.form.addRow("<b>Prénom</b>", QLabel(f"<b>{prenom}</b>"))
            self.form.addRow("<b>Âge</b>", QLabel(f"<b>{age}</b>"))
            self.form.addRow("<b>Métier</b>", QLabel(f"<b>{metier}</b>"))
            if choix == "Élève" and len(user) > 5:
                self.form.addRow("<b>Classe</b>", QLabel(f"<b>{user[5]}</b>"))
            elif choix == "Prof" and len(user) > 6:
                self.form.addRow("<b>Matière</b>", QLabel(f"<b>{user[5]}</b>"))
                self.form.addRow("<b>Classe</b>", QLabel(f"<b>{user[6]}</b>"))





    # Le filtrage du texte tapé
    def filtrer_apercu(self, texte: str):
        users = self.get_users()

        q = (texte or '').strip().lower()

        filtres = []
        if isinstance(users, list):
            if not q:
                filtres = users
            else:
                for i in users:
                    if q in str(i[1]).lower() or q in str(i[2]).lower() or q in str(i[0]):
                        filtres.append(i)
        self.listes_apercu.clear()
        for user in filtres:
            text = f"ID: {user[0]}: {user[1]}  {user[2]}"
            item = QtWidgets.QListWidgetItem(text)
            item.setData(QtCore.Qt.UserRole, user[0])
            item.setData(QtCore.Qt.UserRole + 1, self.get_choix())
            self.listes_apercu.addItem(item)



    def deletelater(self, layout) -> None:
        if layout is not None:
            while layout.count():
                item = layout.takeAt(0)
                if item.widget() is not None:
                    item.widget().deleteLater()




if __name__ == "__main__":

    app = QApplication(sys.argv)
    window = RecherchePage()
    with open('../assets/styles.qss', 'r') as f:
        styles = f.read()
        window.setStyleSheet(styles)

    window.show()
    sys.exit(app.exec())
