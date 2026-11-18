import sys
from collections import Counter

from PySide6.QtCharts import (
    QBarCategoryAxis,
    QBarSeries,
    QBarSet,
    QChart,
    QChartView,
    QLineSeries,
    QPieSeries,
    QValueAxis,
)
from PySide6.QtGui import QPainter, QColor

from Services.service import Service

from PySide6 import QtWidgets, QtCore
from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QLabel,
    QScrollArea,
    QWidget,
    QPushButton,
    QApplication,
    QHBoxLayout,
    QVBoxLayout,
    QLineEdit,
    QListWidget,
)


class Dashboard(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("DASH")
        self.setupUi()
        self.connexion()


    def setupUi(self):
        self.scroll_area = QScrollArea(self)
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.scroll_area.setFrameShape(QScrollArea.NoFrame)
        content = QWidget()
        self.scroll_area.setWidget(content)

        root_layout = QVBoxLayout(self)
        root_layout.setContentsMargins(8, 8, 8, 8)
        root_layout.addWidget(self.scroll_area)

        content_layout = QVBoxLayout(content)
        content_layout.setContentsMargins(10, 10, 10, 10)
        content_layout.setSpacing(14)

        self.btn = QPushButton("Rafraîchir")
        cards_layout = QHBoxLayout()
        cards_layout.setSpacing(12)

        self.eleve_card, self.eleve_valeur, self.eleve_chart = self.carte_des_infos(
            "Élèves", "0", "Total des élèves"
        )
        self.prof_card, self.prof_valeur, self.prof_chart = self.carte_des_infos(
            "Professeurs", "0", "Total des professeurs"
        )
        self.personnel_card, self.personnel_valeur, self.personnel_chart = self.carte_des_infos(
            "Personnel", "0", "Total du personnel"
        )

        cards_layout.addWidget(self.eleve_card)
        cards_layout.addWidget(self.prof_card)
        cards_layout.addWidget(self.personnel_card)
        content_layout.addLayout(cards_layout)

        self.layout3 = QHBoxLayout()
        self.layout3.setSpacing(12)
        self.effectifs_chart_view = QChartView()
        self.effectifs_chart_view.setRenderHint(QPainter.Antialiasing)
        self.effectifs_chart_view.setFixedHeight(280)
        self.effectifs_chart_view.setStyleSheet("border: none;")
        self.ages_chart_view = QChartView()
        self.ages_chart_view.setRenderHint(QPainter.Antialiasing)
        self.ages_chart_view.setFixedHeight(280)
        self.ages_chart_view.setStyleSheet("border: none;")
        self.layout3.addWidget(self.effectifs_chart_view, 1)
        self.layout3.addWidget(self.ages_chart_view, 1)
        content_layout.addLayout(self.layout3)

        data_layout = QHBoxLayout()
        data_layout.setSpacing(12)
        overview_layout = QVBoxLayout()
        overview_layout.addWidget(self.apercu_infos("Aperçu"))
        overview_layout.addWidget(self.btn)
        data_layout.addLayout(overview_layout)
        data_layout.addWidget(self.recherche_champ())
        content_layout.addLayout(data_layout)

    def chart_view(self, eleves, professeurs, personnels):
        categories = ["Élèves", "Professeurs", "Personnel"]
        effectifs = [len(eleves), len(professeurs), len(personnels)]

        bar_set = QBarSet("Effectif")
        bar_set.append(effectifs)
        bar_set.setColor(QColor("#2b7de9"))
        bar_set.setBorderColor(QColor("#ffffff"))

        series = QBarSeries()
        series.append(bar_set)
        series.setLabelsVisible(True)

        chart = QChart()
        chart.addSeries(series)
        chart.setTitle("Effectifs enregistrés")
        chart.setAnimationOptions(QChart.SeriesAnimations)
        chart.setTheme(QChart.ChartThemeDark)
        chart.legend().hide()

        axis_x = QBarCategoryAxis()
        axis_x.append(categories)
        chart.addAxis(axis_x, Qt.AlignBottom)
        series.attachAxis(axis_x)

        axis_y = QValueAxis()
        axis_y.setRange(0, max(1, max(effectifs, default=0)))
        axis_y.setLabelFormat("%d")
        axis_y.setTitleText("Nombre")
        chart.addAxis(axis_y, Qt.AlignLeft)
        series.attachAxis(axis_y)

        return chart

    @staticmethod
    def _ages(records):
        return [
            record[3]
            for record in records
            if len(record) > 3 and isinstance(record[3], (int, float))
        ]

    def line_chart(self, records):
        age_counts = Counter(self._ages(records))
        chart = QChart()
        chart.setAnimationOptions(QChart.SeriesAnimations)
        chart.setTheme(QChart.ChartThemeDark)
        chart.legend().hide()
        chart.setBackgroundVisible(False)
        chart.setMargins(QtCore.QMargins(0, 0, 0, 0))

        if age_counts:
            line_series = QLineSeries()
            line_series.setColor(QColor("#38bdf8"))
            line_series.setPointsVisible(True)
            for age, count in sorted(age_counts.items()):
                line_series.append(age, count)
            chart.addSeries(line_series)

            axis_x = QValueAxis()
            axis_x.setTitleText("Âge")
            minimum_age = min(age_counts)
            maximum_age = max(age_counts)
            if minimum_age == maximum_age:
                minimum_age -= 1
                maximum_age += 1
            axis_x.setRange(minimum_age, maximum_age)
            axis_x.setLabelFormat("%d")
            chart.addAxis(axis_x, Qt.AlignBottom)
            line_series.attachAxis(axis_x)
            axis_x.hide()

            axis_y = QValueAxis()
            axis_y.setRange(0, max(age_counts.values()) + 1)
            chart.addAxis(axis_y, Qt.AlignLeft)
            line_series.attachAxis(axis_y)
            axis_y.hide()
        else:
            chart.setTitle("Aucune donnée")

        return chart

    def chart_line(self, records):
        chart = self.line_chart(records)
        chart_view = QChartView(chart)
        chart_view.setRenderHint(QPainter.Antialiasing)
        chart_view.setMinimumHeight(105)
        chart_view.setMaximumHeight(120)
        chart_view.setStyleSheet("border: none; background: transparent;")
        return chart_view

    def carte_des_infos(self, titre, valeur, description):
        card = QWidget()
        card.setStyleSheet(
            "background-color: #151E32; border: 1px solid #334155; border-radius: 20px;"
        )
        layout = QVBoxLayout(card)
        layout.setContentsMargins(12, 12, 12, 8)
        layout.setSpacing(4)

        title_label = QLabel(titre)
        title_label.setStyleSheet("font-size: 14px; color: #94A3B8;")
        value_label = QLabel(str(valeur))
        value_label.setStyleSheet("font-size: 34px; font-weight: 1000; color: #FFFFFF;")
        description_label = QLabel(description)
        description_label.setStyleSheet("font-size: 12px; color: #64748B;")
        description_label.setWordWrap(True)

        layout.addWidget(title_label)
        layout.addWidget(value_label)
        layout.addWidget(description_label)

        chart_view = self.chart_line([])
        layout.addWidget(chart_view)
        return card, value_label, chart_view


    def apercu_infos(self, titre):
        card = QWidget()
        card.setStyleSheet(
            "background-color: #151E32; border: 1px solid #334155; border-radius: 20px;"
        )
        layout = QVBoxLayout(card)
        layout.setContentsMargins(10, 10, 10, 10)
        layout.setSpacing(10)

        title_label = QLabel(titre)
        title_label.setStyleSheet("font-size: 14px; color: #94A3B8; border-radius:5px 5px;")
        self.listes_apercus = QListWidget()

        self.listes_apercus.setSelectionBehavior(QListWidget.SelectRows)
        self.listes_apercus.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)

        self.listes_apercus.setStyleSheet("font-size: 20px; font-weight: 700; color: B2F6A1;")


        layout.addWidget(title_label, alignment=QtCore.Qt.AlignCenter)
        layout.addWidget(self.listes_apercus)

        return card


    def recherche_champ(self):
        card = QWidget()
        card.setStyleSheet(
            "background-color: #151E32; border: 1px solid #334155; border-radius: 20px;"
        )
        layout = QVBoxLayout(card)
        layout.setContentsMargins(10, 10, 10, 10)
        layout.setSpacing(10)

        self.champ_recherche = QLineEdit()
        self.champ_recherche.setPlaceholderText(f"Recherche..., Nom ou ID")
        self.champ_recherche.setStyleSheet("padding:6px; border-radius:8px; background-color:#0F1724; color:#F1F5F9;")

        self.listes = QListWidget()


        self.listes.setSelectionBehavior(QListWidget.SelectRows)
        self.listes.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)

        self.listes.setStyleSheet("font-size: 20px; font-weight: 700; color: B2F6A1;")
        layout.addWidget(self.champ_recherche)

        layout.addWidget(self.listes)
        layout.addStretch(1)
        return card

    # la fonction de lieson entre les actions
    def connexion(self):
        self.btn.clicked.connect(self.on_actualise)
        self.champ_recherche.textChanged.connect(self.filtrer_apercu)
        self.on_actualise()

    def on_actualise(self):
        service = Service()
        eleves = service.get_eleves()
        professeurs = service.get_profs()
        personnels = service.get_personnels()
        for categorie, records in (
            ("élèves", eleves),
            ("professeurs", professeurs),
            ("membres du personnel", personnels),
        ):
            if not isinstance(records, list):
                raise RuntimeError(
                    f"Impossible de charger les données pour {categorie} : {records}"
                )

        self.eleve_valeur.setText(str(len(eleves)))
        self.prof_valeur.setText(str(len(professeurs)))
        self.personnel_valeur.setText(str(len(personnels)))
        self.eleve_chart.setChart(self.line_chart(eleves))
        self.prof_chart.setChart(self.line_chart(professeurs))
        self.personnel_chart.setChart(self.line_chart(personnels))

        self.listes_apercus.clear()
        for record in eleves:
            text = f"ID: {record[0]}: {record[1]}  {record[2]}"
            item = QtWidgets.QListWidgetItem(text)
            item.setData(QtCore.Qt.UserRole, record[0])
            self.listes_apercus.addItem(item)
        self.filtrer_apercu(self.champ_recherche.text())

        self.effectifs_chart_view.setChart(self.chart_view(eleves, professeurs, personnels))
        self.ages_chart_view.setChart(self.chart_champ2(eleves))




    # Le filtrage du texte tapé
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


    def chart_champ2(self, eleves):
        frequency = Counter(self._ages(eleves))
        chart = QChart()
        chart.setAnimationOptions(QChart.SeriesAnimations)
        chart.setTheme(QChart.ChartThemeDark)
        chart.setTitle('Âges')
        chart.setTitleBrush(QtCore.Qt.white)
        chart.legend().hide()

        if frequency:
            pie_series = QPieSeries()
            for age, count in sorted(frequency.items()):
                pie_series.append(f'{age} ans', count)
            chart.addSeries(pie_series)
            pie_series.setLabelsVisible(True)
            chart.legend().setVisible(True)
            chart.legend().setAlignment(QtCore.Qt.AlignBottom)
        else:
            chart.setTitle("Aucune donnée d'âge")

        return chart



if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Dashboard()
    with open("../assets/styles.qss", "r") as f:
        app.setStyleSheet(f.read())
    window.show()
    app.exec()