import sys
from PySide2.QtGui import QPixmap
from PySide2.QtWebEngineWidgets import QWebEngineView
from PySide2.QtWidgets import (
    QApplication, QGridLayout, QRadioButton, QTextEdit,
    QWidget,
    QLabel,
    QVBoxLayout,
    QHBoxLayout,
    QLineEdit
)

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

        interval_layout = QHBoxLayout()
        interval_layout.addWidget(QLabel('Интервал: ['))
        self.a_line_edit = QLineEdit()
        interval_layout.addWidget(self.a_line_edit)
        interval_layout.addWidget(QLabel(';'))
        self.b_line_edit = QLineEdit()
        interval_layout.addWidget(self.b_line_edit)
        interval_layout.addWidget(QLabel(']'))
        digits_layout.addLayout(interval_layout)

        eps_layout = QHBoxLayout()
        eps_layout.addWidget(QLabel('Точность: '))
        self.esp_line_edit = QLineEdit()
        eps_layout.addWidget(self.esp_line_edit)
        digits_layout.addLayout(eps_layout)

        result_text_edit = QTextEdit()
        result_text_edit.setReadOnly(True)
        digits_layout.addWidget(result_text_edit)

        self.eq1_radio = QRadioButton()
        eq1_label = QLabel()
        eq1_label.setPixmap(QPixmap('assets/eq1.png'))
        layout.addWidget(self.eq1_radio, 0, 0)
        layout.addWidget(eq1_label, 0, 1)

        self.eq2_radio = QRadioButton()
        eq2_label = QLabel()
        eq2_label.setPixmap(QPixmap('assets/eq2.png'))
        layout.addWidget(self.eq2_radio, 1, 0)
        layout.addWidget(eq2_label, 1, 1)

        self.eq3_radio = QRadioButton()
        eq3_view = QWebEngineView()
        layout.addWidget(self.eq3_radio, 2, 0)
        layout.addWidget(eq3_view, 2, 1)

        self.eq4_radio = QRadioButton()
        eq4_view = QWebEngineView()
        layout.addWidget(self.eq4_radio, 3, 0)
        layout.addWidget(eq4_view, 3, 1)


if __name__ == "__main__":
    app = QApplication([])
    app.setStyle('Fusion')
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
