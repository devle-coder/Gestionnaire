import sys
from Prof.professeurs import Professeurs
from Services.service import Service

from PySide6 import QtWidgets, QtCore
from PySide6.QtGui import Qt, QPixmap
from PySide6.QtWidgets import (
                        QWidget, QLabel, QTextEdit,
                        QPushButton, QMessageBox, QFormLayout,
                        QSpinBox, QDateEdit, QApplication, QHBoxLayout,
                        QVBoxLayout, QLineEdit, QComboBox, QFileDialog
)

class ProfPage(QWidget):
    retour_demande = QtCore.Signal()

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Prof Page")
        self.setFixedSize(800, 800)
        self.setupUi()
        self.connexion()

    def setupUi(self):
        main_layout = QVBoxLayout(self)


        layout = QHBoxLayout()
        title = QLabel("<h1>Inscription de prof</h1>".title())

        main_layout.addLayout(layout)

        self.BtnRetour = QPushButton("Retour")
        self.BtnRetour.setFixedWidth(100)
        layout.addWidget(self.BtnRetour)

        layout.addWidget(title, alignment=QtCore.Qt.AlignCenter)


        form = QFormLayout()

        form.setContentsMargins(5, 5, 5, 5)
        form.setSpacing(5)

        self.nomEdit = QLineEdit()


        self.nomEdit.setPlaceholderText("Nom")
        self.prenomEdit = QLineEdit()
        self.prenomEdit.setPlaceholderText("Prenom")
        self.ageEdit = QSpinBox()
        self.ageEdit.setRange(0, 60)
        self.ageEdit.setValue(0)
        self.metierEdit = QLineEdit()
        self.metierEdit.setPlaceholderText("Métier")
        self.classeEdit = QComboBox()
        self.matierEdit = QComboBox()
        self.matierEdit.addItems(['Anglais', 'Math', 'Science', 'Physique'])
        self.classeEdit.addItems(["L1", "terminale", "L3", "L4"])
        self.matierEdit.setCurrentIndex(0)
        self.classeEdit.setCurrentIndex(0)
        self.matierEdit.setFixedWidth(100)
        self.classeEdit.setFixedWidth(100)

        self.BtnAjouter = QPushButton("Ajouter")

        form.addRow("Nom", self.nomEdit)
        form.addRow("Prénom", self.prenomEdit)
        form.addRow("Âge", self.ageEdit)
        form.addRow("Métier", self.metierEdit)
        form.addRow("Classe", self.classeEdit)
        form.setSpacing(10)
        form.addRow("Matière", self.matierEdit)

        main_layout.addLayout(form)

        # le layout pour les params optionnel
        Layout = QHBoxLayout()

        user_description = QTextEdit()
        user_description.setPlaceholderText('Déscription')

        optionnel = QLabel("<p style='text-align:center' >Optionnel<p>")
        main_layout.addWidget(optionnel)
        self.label_photo = QLabel("Aucune photo")
        self.label_photo.setFixedSize(120, 120)
        self.label_photo.setAlignment(Qt.AlignCenter)
        self.label_photo.setStyleSheet("border: 1px solid gray; border-radius: 60px;")
        main_layout.addWidget(self.label_photo)

        self.btn_choisir = QPushButton("Changer la photo")
        self.btn_choisir.setMaximumSize(QtCore.QSize(150, 150))
        main_layout.addWidget(self.btn_choisir)
        Layout.addWidget(user_description)
        main_layout.addLayout(Layout)
        main_layout.addWidget(self.BtnAjouter)

    def connexion(self):
        self.BtnRetour.clicked.connect(self.retour_demande.emit)
        self.BtnAjouter.clicked.connect(self.enregistre)
        self.btn_choisir.clicked.connect(self.choisir_image)

    def enregistre(self):
        service = Service()
        nom = self.nomEdit.text()
        prenom = self.prenomEdit.text()
        age = self.ageEdit.value()
        metier = self.matierEdit.currentText()
        classe = self.classeEdit.currentText()
        matier = self.matierEdit.currentText()
        prof = Professeurs(nom, prenom, age, metier, matier, classe)
        try:
            service.save_tech(prof)
            QMessageBox.information(self, 'Ajouter', 'Ajouter')
        except Exception as e:
            QMessageBox.warning(self, "Erreur", str(e))

        self.nomEdit.clear()
        self.prenomEdit.clear()
        self.ageEdit.setValue(0)
        self.metierEdit.clear()
        self.classeEdit.setCurrentIndex(0)
        self.matierEdit.setCurrentIndex(0)
        return

    def choisir_image(self):
        chemin_fichier, _ = QFileDialog.getOpenFileName(
            None,  # Widget parent (ou self dans une classe)
            "Choisir une photo de profil",  # Titre de la fenêtre
            "",  # Dossier de départ ("" = dernier dossier ouvert)
            "Images (*.png *.jpg *.jpeg *.bmp)"  # Filtre de fichiers
        )

        if chemin_fichier:
            if chemin_fichier:
                pixmap = QPixmap(chemin_fichier).scaled(
                    120, 120, Qt.KeepAspectRatioByExpanding, Qt.SmoothTransformation
                )
                self.label_photo.setPixmap(pixmap)



if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = ProfPage()
    with open('../assets/styles.qss', 'r') as f:
        app.setStyleSheet(f.read())
    window.show()
    app.exec()