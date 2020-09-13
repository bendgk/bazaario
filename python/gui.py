"""
This demo demonstrates how to embed a matplotlib (mpl) plot 
into a PyQt4 GUI application, including:
* Using the navigation toolbar
* Adding data to the plot
* Dynamically modifying the plot's properties
* Processing mpl events
* Saving the plot to a file from a menu
The main goal is to serve as a basis for developing rich PyQt GUI
applications featuring mpl plots (using the mpl OO API).
Eli Bendersky (eliben@gmail.com)
License: this code is in the public domain
Last modified: 19.01.2009
"""
import sys, os, random, time

import matplotlib
matplotlib.use('Qt5Agg')

from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from matplotlib.figure import Figure

from pymongo import MongoClient
from pymongo import ASCENDING, DESCENDING

client = MongoClient('mongodb://localhost:27017/')
ticker_db = client["tickers"]

class ItemSelector(QWidget):
    def __init__(self, products, mplCanvas):
        super().__init__()
        self.mplCanvas = mplCanvas
        self.products = products
        self.products_view = products.copy()
        self.current_product = None

        self.list_view = QListView()
        self.model = QStringListModel(self.products_view)

        self.list_view.setModel(self.model)
        self.sel_model = self.list_view.selectionModel()
        self.sel_model.selectionChanged.connect(self.selection_changed)
        self.list_view.setFixedWidth(300)

        layout = QVBoxLayout()

        completer = QCompleter(products)
        completer.setCaseSensitivity(Qt.CaseInsensitive)
        search_bar = QLineEdit()
        search_bar.setPlaceholderText("Search")
        search_bar.setCompleter(completer)

        completer.highlighted.connect(self.completed)
        search_bar.textEdited.connect(self.search_edit)

        layout.addWidget(search_bar)
        layout.addWidget(self.list_view)
        self.setLayout(layout)

    def search_edit(self, text):
        if text == "":
            self.products_view = self.products

        else:
            b = []
            for product in self.products:
                text = text.replace(" ", "_")
                if text.lower() in product.lower():
                    b.append(product)

            self.products_view = b
        
        self.model.setStringList(self.products_view)

    def completed(self, text):
        self.current_product = text
        print(self.current_product)
        self.search_edit(text)
        self.selected(self.current_product)

    def selection_changed(self, item):
        self.current_product = self.sel_model.selection().indexes()[0].data()
        self.selected(self.current_product)

    def selected(self, product):
        ticks = list(ticker_db[product].find().sort("time", DESCENDING).limit(1000))
        ask_prices = [tick["ask_price"] for tick in ticks]
        times = [tick["time"] for tick in ticks]
        
        print(times, ask_prices)

        self.mplCanvas.set_graph(times, ask_prices)





class MplCanvas(FigureCanvasQTAgg):

    def __init__(self, parent=None, width=5, height=4, dpi=10):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111)
        super(MplCanvas, self).__init__(fig)

    def set_graph(self, times, prices):
        self.axes.cla()

        #5s ticks

        self.axes.plot(times, prices)
        self.draw()

class Window(QMainWindow):

    def __init__(self):
        super().__init__()
        products = ticker_db.list_collection_names()

        #Build UI

        #Menu Bar
        exitAct = QAction(QIcon('exit.png'), '&Exit', self)
        exitAct.setShortcut('Ctrl+Q')
        exitAct.setStatusTip('Exit application')
        exitAct.triggered.connect(qApp.quit)

        self.statusBar()

        menubar = self.menuBar()
        fileMenu = menubar.addMenu('&File')
        fileMenu.addAction(exitAct)

        self.setGeometry(300, 300, 600, 400)
        self.setWindowTitle('Bazaario')

        w = QWidget(self)
        layout = QHBoxLayout()
        
        #MPL Graph
        sc = MplCanvas(self, width=100, height=100, dpi=100)

        #Item Selector
        layout.addWidget(ItemSelector(products, sc))
        layout.addWidget(sc)
        
        w.setLayout(layout)
        self.setCentralWidget(w)
        self.show()


def main():
    app = QApplication(sys.argv)
    window = Window()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()