import sys

from PySide6.QtCore import Qt, Signal, QSize
from page_supprimer_eleves import PageSupprimeEleves
from page_supprimer_prof import PageSupprimeProfs
from page_supprimer_personnel import PageSupprimePersonnel

from PySide6.QtWidgets import (QWidget, QApplication, QPushButton,
                               QStackedWidget, QMessageBox, QLineEdit, QLabel, QVBoxLayout, QHBoxLayout,
                               QTableView, QMenu, QMenuBar, QFrame)

class MainWindow(QWidget):
    retour_demande = Signal()

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Suppression")
        self.setupUi()
        self.connextion()

    def setupUi(self):

        sidebar = QHBoxLayout()
        sidebar.setSpacing(16)
        sidebar.setContentsMargins(0, 0, 0, 0)


        self.btn_eleve = QPushButton("Élèves")
        self.btn_prof = QPushButton("Prof")
        self.btn_personnel = QPushButton("Personnel")
        self.btn_eleve.setMaximumSize(QSize(180, 50))
        self.btn_prof.setMaximumSize(QSize(180, 50))
        self.btn_personnel.setMaximumSize(QSize(180, 50))


        for b in (self.btn_eleve, self.btn_prof, self.btn_personnel):
            b.setObjectName("Btn_affiche-primary")


        sidebar.addWidget(self.btn_eleve)
        sidebar.addWidget(self.btn_prof)
        sidebar.addWidget(self.btn_personnel)

        self.stack = QStackedWidget()
        self.piles_page = self.stack

        self.eleve_page = PageSupprimeEleves()
        self.prof_page = PageSupprimeProfs()
        self.personnel_page = PageSupprimePersonnel()

        self.piles_page.addWidget(self.eleve_page)
        self.piles_page.addWidget(self.prof_page)
        self.piles_page.addWidget(self.personnel_page)

        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(10, 10, 10, 10)
        main_layout.setSpacing(5)

        main_layout.addLayout(sidebar)
        main_layout.addWidget(self.stack)

        main_layout.setStretch(0, 0)
        main_layout.setStretch(1, 1)

    def connextion(self):
        self.btn_eleve.clicked.connect(self.page_supprimer_eleves)
        self.btn_prof.clicked.connect(self.page_supprimer_profs)
        self.btn_personnel.clicked.connect(self.page_supprimer_personnels)

        self.eleve_page.BtnRetour.clicked.connect(self.retour_demande.emit)
        self.prof_page.BtnRetour.clicked.connect(self.retour_demande.emit)
        self.personnel_page.BtnRetour.clicked.connect(self.retour_demande.emit)


    def page_supprimer_eleves(self):
        self.stack.setCurrentIndex(0)

    def page_supprimer_profs(self):
        self.stack.setCurrentIndex(1)

    def page_supprimer_personnels(self):
        self.stack.setCurrentIndex(2)




if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    with open('../assets/styles.qss','r') as file:
        app.setStyleSheet(file.read())
    window.show()
    app.exec()
