import sys

from Services.service import Service
from PySide6 import QtCore, QtWidgets
from PySide6.QtWidgets import (QWidget, QPushButton,QLabel, QApplication,
                               QListWidget, QVBoxLayout, QHBoxLayout,
                               QLineEdit,QMessageBox, QFormLayout
                               )

class PageSupprimeEleves(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("MainWindow")
        self.setFixedSize(800,600)

        self.setupUi()
        self.connexion()


    def setupUi(self):
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(10, 10, 10, 10)
        main_layout.setSpacing(5)

        layout = QHBoxLayout()
        title = QLabel("<h1>Élèves</h1>".title())

        main_layout.addLayout(layout)

        self.BtnRetour = QPushButton("Retour")
        self.BtnRetour.setFixedWidth(100)
        layout.addWidget(self.BtnRetour)
        main_layout.stretch(0)
        layout.addWidget(title, alignment=QtCore.Qt.AlignCenter)
        main_layout.stretch(10)
        form = QFormLayout()
        form.setContentsMargins(5, 5, 5, 5)
        form.setSpacing(5)

        self.champ_de_recherche = QLineEdit()
        self.champ_de_recherche.setPlaceholderText("Récherche")
        self.btn_supprimer = QPushButton("Supprimer")
        self.btn_supprimer.setObjectName('btn-sup')


        form.addRow("Récherche", self.champ_de_recherche)

        main_layout.addLayout(form)


        self.listes = QListWidget()
        self.listes.setFocus()
        main_layout.addWidget(self.listes)
        main_layout.addWidget(self.btn_supprimer)

    def connexion(self):
        self.apercu_des_users()
        self.champ_de_recherche.textChanged.connect(self.filtrer_apercu)
        self.btn_supprimer.clicked.connect(self.supprimer)

    def supprimer(self):
        service = Service()
        try:
            user_id = self.listes.currentItem().data(QtCore.Qt.UserRole)
            service.delete_eleve_by_id(user_id)
            QMessageBox.information(self, 'Succès', 'Supprimé')
            self.apercu_des_users()
            return True
        except Exception as e:
            QMessageBox.warning(self, 'Échouè', 'Échec veuillez sélectionné une personne ')
            return False

    def apercu_des_users(self):
        items = Service().get_eleves()
        self.listes.clear()
        for i in items:
            text = f"{i[0]} • {i[1]} • {i[2]}"
            item = QtWidgets.QListWidgetItem(text)
            item.setData(QtCore.Qt.UserRole, i[0])
            self.listes.addItem(item)

    def filtrer_apercu(self, texte: str):
        q = (texte or '').strip().lower()
        users = Service()
        users = users.get_eleves()
        filtres = []
        if not q:
            filtres = users[:10]
        else:
            for i in users:
                if q in str(i[1]).lower() or q in str(i[2]).lower() or q in str(i[0]):
                    filtres.append(i)
        self.listes.clear()
        for user in filtres[:10]:
            self.listes.addItem(f"{user[0]} • {user[1]} {user[2]}")





if __name__ == "__main__":

    app = QApplication(sys.argv)
    window = PageSupprimeEleves()
    with open('../assets/styles.qss', 'r') as f:
        styles = f.read()
        app.setStyleSheet(styles)
    window.show()
    sys.exit(app.exec())

