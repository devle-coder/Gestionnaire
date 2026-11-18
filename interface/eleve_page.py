import sys


from PySide6 import QtCore
from Eleves.eleve import Eleve
from Services.service import Service
from PySide6.QtGui import QPixmap, Qt

from PySide6.QtWidgets import (QWidget, QPushButton,
                               QListWidget, QVBoxLayout, QHBoxLayout,
                               QMainWindow, QLineEdit, QTimeEdit,
                               QTextEdit, QLabel, QApplication,
                               QSpinBox, QComboBox, QFormLayout, QMessageBox, QFileDialog
                               )

class ElevePage(QWidget):
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
        title = QLabel("<h1>Inscription d'élève</h1>".title())

        main_layout.addLayout(layout)

        self.BtnRetour = QPushButton("Retour")
        self.BtnRetour.setFixedWidth(100)
        layout.addWidget(self.BtnRetour)
        self.BtnAjouter = QPushButton("Ajouter")

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
        self.ageEdit.setRange(5,20)
        self.ageEdit.setValue(0)
        self.metierEdit = QLineEdit()
        self.metierEdit.setPlaceholderText("Métier")
        self.classeEdit = QComboBox()
        self.classeEdit.addItems(["L1", "terminale", "L3", "L4"])
        self.classeEdit.setCurrentIndex(2)
        self.classeEdit.setFixedWidth(100)
        self.classeEdit.setMinimumHeight(50)


        form.addRow("Nom", self.nomEdit)
        form.addRow("Prénom", self.prenomEdit)
        form.addRow("Âge", self.ageEdit)
        form.addRow("Métier", self.metierEdit)
        form.addRow("Classe", self.classeEdit)

        main_layout.addLayout(form)

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
        self.BtnAjouter.clicked.connect(self.ajouter)
        self.btn_choisir.clicked.connect(self.choisir_image)



    def ajouter(self):
        service = Service()
        nom = self.nomEdit.text()
        prenom = self.prenomEdit.text()
        age = self.ageEdit.value()
        metier = self.metierEdit.text()
        classe = self.classeEdit.currentText()
        eleve = Eleve(nom, prenom, age, metier, classe)
        try:
            service.save_student(eleve)
            QMessageBox.information(self, 'Ajouter', 'Ajouter')
        except Exception as e:
            QMessageBox.warning(self, "Erreur", str(e))

        self.nomEdit.clear()
        self.prenomEdit.clear()
        self.ageEdit.clear()
        self.metierEdit.clear()
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







# astuce
# label = QLabel("&Nom :") # Le '&' souligne le 'N' et crée le raccourci Alt+N
# champ = QLineEdit()
# label.setBuddy(champ) # Lie le label au champ

if __name__ == "__main__":

    app = QApplication(sys.argv)
    window = ElevePage()
    with open('../assets/styles.qss', 'r') as f:
        styles = f.read()
        app.setStyleSheet(styles)
    window.show()
    sys.exit(app.exec())
