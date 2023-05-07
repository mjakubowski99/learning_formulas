from PyQt5.QtWidgets import QWidget, QVBoxLayout
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import (
    FigureCanvasQTAgg,
)
from matplotlib.figure import Figure

class PandasHistogram:

    def hist(self, df, column):
        fig, ax = plt.subplots()

        canvas = FigureCanvasQTAgg(Figure(figsize=(15, 10)))
        ax = canvas.figure.subplots()

        widget = QWidget()
        layout = QVBoxLayout(widget)

        categories = df[column].value_counts().index
        counts = df[column].value_counts().values

        ax.bar(categories, counts)
        layout.addWidget(canvas)

        return widget

