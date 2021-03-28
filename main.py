import sys
from PySide2.QtGui import QDoubleValidator, QPixmap, QRegularExpressionValidator
from PySide2.QtCore import Slot
from PySide2.QtWidgets import (
    QApplication, QButtonGroup, QComboBox, QFileDialog, QGridLayout, QMessageBox, QPushButton, QRadioButton, QTextEdit,
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
        self.update_graph_button.clicked.connect(self.plot2graph)

    @staticmethod
    def show_warning(s):
        box = QMessageBox()
        box.setWindowTitle('Ошибка')
        box.setIcon(QMessageBox.Warning)
        box.setText(s)
        box.exec_()

    def get_eq(self):
        eq = self.radio_group.checkedId()
        if 1 <= eq <= 4:
            return eq_lib[eq - 1]
        else:
            self.show_warning('Необходмо выбрать одно из уравнений')

    def _get_interval(self, a, b):
        a = a.text().replace(',', '.')
        b = b.text().replace(',', '.')
        if a and b:
            a = float(a)
            b = float(b)
            if b <= a:
                self.show_warning('b должно быть >= a')
                return None, None
            else:
                return a, b
        else:
            self.show_warning('Введите [a, b]')
            return None, None

    def get_interval(self):
        return self._get_interval(self.a_line_edit, self.b_line_edit)

    def get_graph_interval(self):
        return self._get_interval(self.graph_a_line_edit,
         self.graph_b_line_edit)

    def get_eps(self):
        eps = self.eps_line_edit.text().replace(',', '.')
        if eps:
            eps = float(eps)
            return eps
        else:
            self.show_warning('Введите точность')


    def calc(self):
        method_id = self.method_combobox.currentIndex()
        eq = self.get_eq()
        if not eq:
            return
        a, b = self.get_interval()
        if not a and not b:
            return
        eps = self.get_eps()
        if not eps:
            return
        point = self.point_lide_edit.text().replace(',', '.')

        self.plot.figure.clf()
        plot_ax = self.plot.figure.subplots()

        try:
            if method_id != 2:
                if method_id == 0:
                    m = eq.solve_by_bisection
                elif method_id == 1:
                    m = eq.solve_by_newtons
                d = m(a, b, eps)

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
            self.result_text_edit.setText(yaml.safe_dump(d, allow_unicode=True))

            self.plot.draw()
        except Exception as e:
            self.result_text_edit.setText('')
            self.show_warning(str(e))
    
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

    def plot2graph(self):
        eq = self.get_eq()
        if not eq:
            return
        eps = self.get_eps()
        if not eps:
            return
        a, b = self.get_graph_interval()
        if not a and not b:
            return

        self.plot.figure.clf()
        plot_ax = self.plot.figure.subplots()
        eq.plot_to_figure(plot_ax, a, b, eps)
        self.plot.draw()

if __name__ == "__main__":
    app = QApplication([])
    app.setStyle('Fusion')
    window = MainWindow()
    window.init_connections();
    window.show()
    sys.exit(app.exec_())
