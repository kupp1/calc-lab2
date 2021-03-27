from PySide2.QtGui import QDoubleValidator, QPixmap
from PySide2.QtWidgets import (
    QButtonGroup,
    QComboBox,
    QGridLayout,
    QPushButton,
    QRadioButton,
    QTextEdit,
    QWidget,
    QLabel,
    QVBoxLayout,
    QHBoxLayout,
    QLineEdit
)
from matplotlib.backends.backend_qt5agg import FigureCanvas
from matplotlib.figure import Figure

class UIMainWindow(QWidget):
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
        digits_layout.addWidget(self.load_from_file_button)

        self.result_text_edit = QTextEdit()
        self.result_text_edit.setReadOnly(True)
        digits_layout.addWidget(self.result_text_edit)

        self.save_to_file_button = QPushButton()
        self.save_to_file_button.setText('Сохранить в файл')
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
        layout.addWidget(self.calc_button, 4, 0, 1, 3)

        self.plot = FigureCanvas(Figure(figsize=(5, 5)))
        layout.addWidget(self.plot, 5, 0, 1, 3)

        graph_interval_layout = QHBoxLayout()
        graph_interval_layout.addWidget(QLabel('['))
        self.graph_a_line_edit = QLineEdit()
        self.graph_a_line_edit.setValidator(QDoubleValidator())
        graph_interval_layout.addWidget(self.graph_a_line_edit)
        graph_interval_layout.addWidget(QLabel(';'))
        self.graph_b_line_edit = QLineEdit()
        self.graph_b_line_edit.setValidator(QDoubleValidator())
        graph_interval_layout.addWidget(self.graph_b_line_edit)
        graph_interval_layout.addWidget(QLabel(']'))
        layout.addLayout(graph_interval_layout, 6, 0, 1, 3)

        self.update_graph_button = QPushButton()
        self.update_graph_button.setText('Поcтроить')
        graph_interval_layout.addWidget(self.update_graph_button)