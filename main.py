import sys
from PySide2.QtGui import QDoubleValidator, QPixmap, QRegularExpressionValidator
from PySide2.QtCore import Slot
from PySide2.QtWidgets import (
    QApplication, QButtonGroup, QComboBox, QFileDialog, QGridLayout, QPushButton, QRadioButton, QTextEdit,
    QWidget,
    QLabel,
    QVBoxLayout,
    QHBoxLayout,
    QLineEdit
)
from matplotlib.backends.backend_qt5agg import FigureCanvas
from matplotlib.figure import Figure
from eq_lib import eq_lib
import yaml
from ui_main import UIMainWindow

class MainWindow(UIMainWindow):
    def init_connections(self):
        self.method_combobox.currentIndexChanged[int].connect(self.method_changed)
        self.save_to_file_button.clicked.connect(self.save_to_file)
        self.load_from_file_button.clicked.connect(self.load_from_file)
        self.calc_button.clicked.connect(self.calc)

    def calc(self):
        method_id = self.method_combobox.currentIndex()
        eq = self.radio_group.checkedId()
        a = self.a_line_edit.text().replace(',', '.')
        b = self.b_line_edit.text().replace(',', '.')
        eps = self.eps_line_edit.text().replace(',', '.')
        point = self.point_lide_edit.text().replace(',', '.')

        if eq == -1:
            return

        eq = eq_lib[eq - 1]

        if eps:
            eps = float(eps)
        else:
            return

        self.plot.figure.clf()
        plot_ax = self.plot.figure.subplots()

        d = {}
        try:
            if method_id != 2:
                if a and b:
                    a = float(a)
                    b = float(b)
                else:
                    return
                
                if method_id == 0:
                    m = eq.solve_by_bisection
                elif method_id == 1:
                    m = eq.solve_by_newtons
                ans, k = m(a, b, eps)

                eq.plot_to_figure(plot_ax, a, b, eps)
            else:
                if point:
                    point = float(point)
                else:
                    return

                if method_id == 1:
                    m = eq.solve_by_newtons
                elif method_id == 2:
                    m = eq.solve_by_simple_iter

                ans, k = m(point, eps)
                eq.plot_to_figure(plot_ax, point - 1, point + 1, eps)
            d['ans'] = float(ans)
            d['f'] = float(eq.f(ans))
            d['k'] = k
            self.result_text_edit.setText(yaml.safe_dump(d))

            self.plot.draw()
        except Exception as e:
            d['error'] = str(e)
            self.result_text_edit.setText(yaml.safe_dump(d, allow_unicode=True))
    
    @Slot(int)
    def method_changed(self, id):
        if id != 2:
            self.point_lide_edit.setEnabled(False)
            self.a_line_edit.setEnabled(True)
            self.b_line_edit.setEnabled(True)
        else:
            self.point_lide_edit.setEnabled(True)
            self.a_line_edit.setEnabled(False)
            self.b_line_edit.setEnabled(False)

    def save_to_file(self):
        text = self.result_text_edit.toPlainText()
        if text:
            filename = QFileDialog().getSaveFileName(filter='Yaml files (*.yaml)')[0]
            
            with open(filename, 'w', encoding='utf-8') as file:
                file.write(text)

    def load_from_file(self):
        filename = QFileDialog().getOpenFileName(filter='Yaml files (*.yaml)')[0]
        
        with open(filename, 'r', encoding='utf-8') as file:
            conf = yaml.safe_load(file)
        
        if 'a' in conf:
            self.a_line_edit.setText(str(conf['a']).replace('.', ','))

        if 'b' in conf:
            self.b_line_edit.setText(str(conf['b']).replace('.', ','))

        if 'point' in conf:
            self.point_lide_edit.setText(str(conf['point']).replace('.', ','))

        if 'eps' in conf:
            self.eps_line_edit.setText(str(conf['eps']).replace('.', ','))

if __name__ == "__main__":
    app = QApplication([])
    app.setStyle('Fusion')
    window = MainWindow()
    window.init_connections();
    window.show()
    sys.exit(app.exec_())
