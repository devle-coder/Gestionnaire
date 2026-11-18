# import sys
# import seaborn as sns
# from PySide6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget
# from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
# from matplotlib.figure import Figure
#
# class IrisVisualizer(QMainWindow):
#    def __init__(self):
#        super().__init__()
#        self.setWindowTitle("Iris Dataset Visualizations")
#        self.setGeometry(100, 100, 1200, 900)  # x, y, width, height
#        self.initUI()
#
#    def initUI(self):
#        central_widget = QWidget(self)
#        self.setCentralWidget(central_widget)
#        layout = QVBoxLayout(central_widget)
#
#        # Adding multiple plots
#        self.addScatterPlot(layout)
#        self.addHistogram(layout)
#        self.addBoxPlot(layout)
#
#    def addPlotCanvas(self, layout, plot_func):
#        canvas = FigureCanvas(Figure(figsize=(6, 4)))
#        plot_func(canvas.figure)
#        layout.addWidget(canvas)
#
#    def addScatterPlot(self, layout):
#        def scatter_plot(figure):
#            iris = sns.load_dataset("iris")
#            ax = figure.add_subplot(111)
#            sns.scatterplot(data=iris, x="sepal_length", y="sepal_width", hue="species", ax=ax)
#            ax.set_title("Sepal Length vs Sepal Width")
#
#        self.addPlotCanvas(layout, scatter_plot)
#
#    def addHistogram(self, layout):
#        def histogram(figure):
#            iris = sns.load_dataset("iris")
#            ax = figure.add_subplot(111)
#            sns.histplot(iris, x="petal_length", hue="species", kde=True, ax=ax)
#            ax.set_title("Histogram of Petal Length")
#
#        self.addPlotCanvas(layout, histogram)
#
#    def addBoxPlot(self, layout):
#        def box_plot(figure):
#            iris = sns.load_dataset("iris")
#            ax = figure.add_subplot(111)
#            sns.boxplot(x="species", y="petal_width", data=iris, ax=ax)
#            ax.set_title("Box Plot of Petal Width")
#
#        self.addPlotCanvas(layout, box_plot)
#
# # Run the application
# app = QApplication(sys.argv)
# window = IrisVisualizer()
# window.show()
# sys.exit(app.exec_())
import sys
from PySide6.QtCore import Qt
from PySide6.QtGui import QPainter
from PySide6.QtWidgets import QApplication, QMainWindow
from PySide6.QtCharts import QChart, QChartView, QBarSet, QBarSeries, QBarCategoryAxis, QValueAxis

class HistogramWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Histogramme avec PySide6 QChart")
        self.resize(800, 600)

        # 1. Créer les données (QBarSet)
        # Chaque valeur correspond à la fréquence d'un intervalle
        set_donnees = QBarSet("Fréquence")
        set_donnees.append([12, 28, 45, 33, 18, 7])

        # 2. Créer la série de barres (QBarSeries)
        series = QBarSeries()
        series.append(set_donnees)
        # Optionnel : réduire l'espace entre les barres pour un effet histogramme
        series.setBarWidth(0.95)

        # 3. Créer le graphique (QChart)
        chart = QChart()
        chart.addSeries(series)
        chart.setTitle("Distribution des scores (Histogramme)")
        chart.setAnimationOptions(QChart.SeriesAnimations)

        # 4. Configurer l'axe X (Intervalles / Classes)
        intervalles = ["0-10", "10-20", "20-30", "30-40", "40-50", "50-60"]
        axe_x = QBarCategoryAxis()
        axe_x.append(intervalles)
        axe_x.setTitleText("Intervalles de scores")
        chart.addAxis(axe_x, Qt.AlignBottom)
        series.attachAxis(axe_x)

        # 5. Configurer l'axe Y (Valeurs / Effectifs)
        axe_y = QValueAxis()
        axe_y.setRange(0, 50)
        axe_y.setTitleText("Nombre d'observations")
        chart.addAxis(axe_y, Qt.AlignLeft)
        series.attachAxis(axe_y)

        # Masquer la légende si une seule série est affichée
        chart.legend().setVisible(False)

        # 6. Créer la vue (QChartView) et activer l'anticrénelage
        chart_view = QChartView(chart)
        chart_view.setRenderHint(QPainter.Antialiasing)

        self.setCentralWidget(chart_view)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = HistogramWindow()
    window.show()
    sys.exit(app.exec())
