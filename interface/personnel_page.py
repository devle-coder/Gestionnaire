import sys

from Personnel.personnel import Personnels
from Services.service import Service
from PySide6 import QtCore
from PySide6.QtCore import Qt
from PySide6.QtGui import QPixmap
from PySide6.QtWidgets import (QWidget, QPushButton,
                               QVBoxLayout, QHBoxLayout,
                               QLineEdit, QFileDialog, QLabel,
                               QTextEdit,  QApplication,
                               QSpinBox, QFormLayout, QMessageBox,
                               )

class PersonnelPage(QWidget):
    retour_demande = QtCore.Signal()

    def __init__(self):
        super().__init__()
        self.setWindowTitle("MainWindow")
        self.setFixedSize(800,600)
        self.stack = None

        self.setupUi()
        self.connexion()


    def setupUi(self):
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(10, 10, 10, 10)
        main_layout.setSpacing(5)

        layout = QHBoxLayout()
        title = QLabel("<h1>Inscription du Personnels</h1>".title())

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


        self.nomEdit = QLineEdit()
        self.nomEdit.setPlaceholderText("Nom")
        self.prenomEdit = QLineEdit()
        self.prenomEdit.setPlaceholderText("Prénom")
        self.ageEdit = QSpinBox()
        self.ageEdit.setRange(0,50)
        self.ageEdit.setValue(0)
        self.metierEdit = QLineEdit()



        self.BtnAjouter = QPushButton("Ajouter")


        form.addRow("Nom", self.nomEdit)
        form.addRow("Prénom", self.prenomEdit)
        form.addRow("Âge", self.ageEdit)
        form.addRow("Métier", self.metierEdit)

        main_layout.addLayout(form)


        # le layout pour les params optionnel
        Layout = QHBoxLayout()

        self.user_description = QTextEdit()
        self.user_description.setPlaceholderText('Déscription')

        self.user_description.setFocus()
        optionnel = QLabel("<p style='text-align:center'> Information Personnel  Optionnel !</p>".title())
        main_layout.addWidget(optionnel)

        self.label_photo = QLabel("Aucune photo")
        self.label_photo.setFixedSize(120, 120)
        self.label_photo.setAlignment(Qt.AlignCenter)
        self.label_photo.setStyleSheet("border: 1px solid gray; border-radius: 60px;")
        main_layout.addWidget(self.label_photo)

        self.btn_choisir = QPushButton("Changer la photo")
        self.btn_choisir.setMaximumSize(QtCore.QSize(150, 150))
        main_layout.addWidget(self.btn_choisir)

        layout.addStretch()

        Layout.addWidget(self.user_description)
        main_layout.addLayout(Layout)
        main_layout.addWidget(self.BtnAjouter)

    def connexion(self):
        self.BtnRetour.clicked.connect(self.retour_demande.emit)
        self.BtnAjouter.clicked.connect(self.ajouter)
        self.btn_choisir.clicked.connect(self.choisir_image)

    def ajouter(self):
        service = Service()
        nom = self.nomEdit.text()
        prenom = self.prenomEdit.text()
        age = self.ageEdit.value()
        metier = self.metierEdit.text()
        eleve = Personnels(nom, prenom, age, metier)
        try:
            service.save_personel(eleve)
            QMessageBox.information(self, 'Ajouter', 'Ajouté')
        except Exception as e:
            QMessageBox.warning(self, "Erreur", str(e))

        self.nomEdit.clear()
        self.prenomEdit.clear()
        self.ageEdit.setValue(0)
        self.metierEdit.clear()
        self.user_description.clear()
        self.label_photo.clear()
        return


    # le signale de retour
    def choisir_image(self):
        chemin_fichier, _ = QFileDialog.getOpenFileName(
            None,
            "Choisir une photo de profil",
            f"/home/devle/Images/Screenshot",
            "Images (*.png *.jpg *.jpeg *.bmp)"
        )

        if chemin_fichier:
            if chemin_fichier:
                pixmap = QPixmap(chemin_fichier).scaled(
                    120, 120, Qt.KeepAspectRatioByExpanding, Qt.SmoothTransformation
                )
                self.label_photo.setPixmap(pixmap)






if __name__ == "__main__":

    app = QApplication(sys.argv)
    window = PersonnelPage()
    with open('../assets/styles.qss', 'r') as f:
        styles = f.read()
        app.setStyleSheet(styles)
    window.show()
    sys.exit(app.exec())
