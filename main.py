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

class MainWindow(QWidget):
    def __init__(self):
        QWidget.__init__(self)
        self.setWindowTitle('Вычмат | Лабораторная 2')

        layout = QGridLayout()
        layout.setVerticalSpacing(20)
        layout.setHorizontalSpacing(20)
        self.setLayout(layout)

        digits_layout = QVBoxLayout()
        digits_layout.setSpacing(4)
        layout.addLayout(digits_layout, 0, 2, 4, 1)

        self.method_combobox = QComboBox()
        self.method_combobox.addItems([
            'Метод половинного деления',
            'Метод Ньютона',
            'Метод простых итераций'])
        self.method_combobox.currentIndexChanged[int].connect(self.method_changed)
        digits_layout.addWidget(self.method_combobox)

        interval_layout = QHBoxLayout()
        interval_layout.addWidget(QLabel('Интервал: ['))
        self.a_line_edit = QLineEdit()
        self.a_line_edit.setValidator(QDoubleValidator())
        interval_layout.addWidget(self.a_line_edit)
        interval_layout.addWidget(QLabel(';'))
        self.b_line_edit = QLineEdit()
        self.b_line_edit.setValidator(QDoubleValidator())
        interval_layout.addWidget(self.b_line_edit)
        interval_layout.addWidget(QLabel(']'))
        digits_layout.addLayout(interval_layout)

        point_layout = QHBoxLayout()
        point_layout.addWidget(QLabel('Начальное приближение: '))
        self.point_lide_edit = QLineEdit()
        self.point_lide_edit.setValidator(QDoubleValidator())
        point_layout.addWidget(self.point_lide_edit)
        self.point_lide_edit.setEnabled(False)
        digits_layout.addLayout(point_layout)

        eps_layout = QHBoxLayout()
        eps_layout.addWidget(QLabel('Точность: '))
        self.eps_line_edit = QLineEdit()
        self.eps_line_edit.setValidator(QDoubleValidator(1e-5, 1, 6))
        eps_layout.addWidget(self.eps_line_edit)
        digits_layout.addLayout(eps_layout)

        self.load_from_file_button = QPushButton()
        self.load_from_file_button.setText('Загрузить из файла')
        self.load_from_file_button.clicked.connect(self.load_from_file)
        digits_layout.addWidget(self.load_from_file_button)

        self.result_text_edit = QTextEdit()
        self.result_text_edit.setReadOnly(True)
        digits_layout.addWidget(self.result_text_edit)

        self.save_to_file_button = QPushButton()
        self.save_to_file_button.setText('Сохранить в файл')
        self.save_to_file_button.clicked.connect(self.save_to_file)
        digits_layout.addWidget(self.save_to_file_button)

        self.radio_group = QButtonGroup()

        self.eq1_radio = QRadioButton()
        self.radio_group.addButton(self.eq1_radio, 1)
        eq1_label = QLabel()
        eq1_label.setPixmap(QPixmap('assets/eq1.png'))
        layout.addWidget(self.eq1_radio, 0, 0)
        layout.addWidget(eq1_label, 0, 1)

        self.eq2_radio = QRadioButton()
        self.radio_group.addButton(self.eq2_radio, 2)
        eq2_label = QLabel()
        eq2_label.setPixmap(QPixmap('assets/eq2.png'))
        layout.addWidget(self.eq2_radio, 1, 0)
        layout.addWidget(eq2_label, 1, 1)

        self.eq3_radio = QRadioButton()
        self.radio_group.addButton(self.eq3_radio, 3)
        eq3_label = QLabel()
        eq3_label.setPixmap(QPixmap('assets/eq3.png'))
        layout.addWidget(self.eq3_radio, 2, 0)
        layout.addWidget(eq3_label, 2, 1)

        self.eq4_radio = QRadioButton()
        self.radio_group.addButton(self.eq4_radio, 4)
        eq4_label = QLabel()
        eq4_label.setPixmap(QPixmap('assets/eq4.png'))
        layout.addWidget(self.eq4_radio, 3, 0)
        layout.addWidget(eq4_label, 3, 1)

        self.calc_button = QPushButton()
        self.calc_button.setText('Посчитать')
        self.calc_button.clicked.connect(self.calc)
        layout.addWidget(self.calc_button, 4, 0, 1, 3)

        self.plot = FigureCanvas(Figure(figsize=(5, 5)))
        layout.addWidget(self.plot, 5, 0, 1, 3)

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
            if method_id == 0:
                if a and b:
                    a = float(a)
                    b = float(b)
                else:
                    return
                
                ans, k = eq.solve_by_bisection(a, b, eps)

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
        if id == 0:
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
    window.show()
    sys.exit(app.exec_())
