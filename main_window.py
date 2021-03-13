import sys
from PySide2.QtWidgets import (
    QApplication,
    QWidget,
    QLabel,
    QVBoxLayout,
    QHBoxLayout,
    QLineEdit
)


class MainWindow(QWidget):
    def __init__(self):
        QWidget.__init__(self)
        self.setWindowTitle('Вычмат Лабораторная 2')

        layout = QVBoxLayout()
        self.setLayout(layout)

        intervalLayout = QHBoxLayout()
        layout.addLayout(intervalLayout)
        intervalLayout.addWidget(QLabel('Интервал: ['))
        self.a_line_edit = QLineEdit()
        intervalLayout.addWidget(self.a_line_edit)
        intervalLayout.addWidget(QLabel(';'))
        self.b_line_edit = QLineEdit()
        intervalLayout.addWidget(self.b_line_edit)
        intervalLayout.addWidget(QLabel(']'))

        epsLayout = QHBoxLayout()
        layout.addLayout(epsLayout)
        epsLayout.addWidget(QLabel('Точность: '))
        self.esp_line_edit = QLineEdit()
        epsLayout.addWidget(self.esp_line_edit)


if __name__ == "__main__":
    app = QApplication([])
    app.setStyle('Fusion')
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
