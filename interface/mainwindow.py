import sys

from PySide6.QtCore import Qt
from PySide6.QtGui import QPixmap, QPainter, QPainterPath

from eleve_page import ElevePage
from prof_page import ProfPage
from personnel_page import PersonnelPage
from dashboard import Dashboard as Dash
from recherche_page import RecherchePage
from page_supprimer import MainWindow as PageSupprimerWindow

from PySide6.QtWidgets import (QWidget, QApplication, QPushButton,
                               QStackedWidget, QMessageBox, QLineEdit, QLabel, QVBoxLayout, QHBoxLayout,
                               QTableView, QMenu, QMenuBar, QFrame)

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("DASH")
        self.setupUi()
        self.connextion()

    def setupUi(self):

        sidebar = QVBoxLayout()
        sidebar.setSpacing(16)
        sidebar.setContentsMargins(0, 0, 0, 0)


        self.btn_tableau = QPushButton("Tableau")
        self.btn_eleve = QPushButton("Élèves")
        self.btn_prof = QPushButton("Prof")
        self.btn_personnel = QPushButton("Personnel")
        self.btn_recherche_et_info = QPushButton("Récherche")
        self.btn_supprimer = QPushButton("Supprimer")
        self.btn_supprimer.setObjectName('btn-sup')


        for b in (self.btn_tableau, self.btn_eleve, self.btn_prof, self.btn_personnel, self.btn_recherche_et_info):
            b.setObjectName("Btn_affiche-primary")

        label_profile = QLabel()
        label_profile.setPixmap(self.creer_avatar_circulaire())
        sidebar.addWidget(label_profile)

        user_nom = QLabel("<h1 style='color:rgba(255, 0, 20, 0.50)' >DOURA</h1>")

        user_nom.setAlignment(Qt.AlignCenter)
        sidebar.addWidget(user_nom)


        sidebar.addWidget(self.btn_tableau)

        sidebar.addWidget(self.btn_eleve)
        sidebar.addWidget(self.btn_prof)
        sidebar.addWidget(self.btn_personnel)

        sidebar.addSpacing(10)
        sidebar.addWidget(self.btn_recherche_et_info)
        sidebar.addStretch()
        sidebar.addWidget(self.btn_supprimer)


        self.stack = QStackedWidget()
        self.piles_page = self.stack

        self.dash = Dash()
        self.eleve_page = ElevePage()
        self.prof_page = ProfPage()
        self.personnel_page = PersonnelPage()
        self.recherche_page = RecherchePage()
        self.supprimer_page = PageSupprimerWindow()

        self.piles_page.addWidget(self.dash)
        self.piles_page.addWidget(self.eleve_page)
        self.piles_page.addWidget(self.prof_page)
        self.piles_page.addWidget(self.personnel_page)
        self.piles_page.addWidget(self.recherche_page)
        self.piles_page.addWidget(self.supprimer_page)

        main_layout = QHBoxLayout(self)
        main_layout.setContentsMargins(10, 10, 10, 10)
        main_layout.setSpacing(5)
        main_layout.addLayout(sidebar)
        main_layout.addWidget(self.stack)

        main_layout.setStretch(0, 0)
        main_layout.setStretch(1, 1)

    def connextion(self):
        self.btn_tableau.clicked.connect(self.dash.on_actualise)
        self.btn_tableau.clicked.connect(self.page_dashboard)
        self.btn_eleve.clicked.connect(self.page_add_sudent)
        self.btn_prof.clicked.connect(self.page_add_prof)
        self.btn_personnel.clicked.connect(self.page_add_personal)
        self.btn_recherche_et_info.clicked.connect(self.page_add_info_et_recherche)
        self.btn_supprimer.clicked.connect(self.page_supprimer)

        self.eleve_page.retour_demande.connect(self.page_dashboard)
        self.prof_page.retour_demande.connect(self.page_dashboard)
        self.personnel_page.retour_demande.connect(self.page_dashboard)
        self.recherche_page.retour_demande.connect(self.page_dashboard)
        self.supprimer_page.retour_demande.connect(self.page_dashboard)





    @staticmethod
    def creer_avatar_circulaire(chemin_image='../images/dark_img.jpeg', taille=100):
        source = QPixmap(chemin_image).scaled(
            taille, taille, Qt.KeepAspectRatioByExpanding, Qt.SmoothTransformation
        )

        resultat = QPixmap(taille, taille)
        resultat.fill(Qt.transparent)

        painter = QPainter(resultat)
        painter.setRenderHint(QPainter.Antialiasing)

        chemin = QPainterPath()
        chemin.addEllipse(0, 0, taille, taille)
        painter.setClipPath(chemin)

        painter.drawPixmap(0, 0, source)
        painter.end()

        return resultat




    def page_dashboard(self):
        self.stack.setCurrentIndex(0)

    def page_add_sudent(self):
        self.stack.setCurrentIndex(1)

    def page_add_prof(self):
        self.stack.setCurrentIndex(2)

    def page_add_personal(self):
        self.stack.setCurrentIndex(3)

    def page_add_info_et_recherche(self):
        self.stack.setCurrentIndex(4)

    def page_supprimer(self):
        self.stack.setCurrentWidget(self.supprimer_page)




if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    with open('../assets/styles.qss','r') as file:
        app.setStyleSheet(file.read())
    window.show()
    app.exec()
