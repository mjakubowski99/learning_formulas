from PyQt5.QtWidgets import QWidget, QVBoxLayout
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import (
    FigureCanvasQTAgg,
)
from matplotlib.figure import Figure

class PandasHistogram:

    def hist(self, df, column):
        fig, ax = plt.subplots()

        canvas = FigureCanvasQTAgg(Figure(figsize=(5, 3)))
        ax = canvas.figure.subplots()

        widget = QWidget()
        layout = QVBoxLayout(widget)

        if df[column].dtype.kind in 'biufc':
            ax.hist(df[column], 50, facecolor="green", alpha=0.75)
            layout.addWidget(canvas)

        return widget

