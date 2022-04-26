import sys
import proxy
from PySide6.QtWidgets import (
    QLineEdit, QPushButton, QApplication, QVBoxLayout, QDialog)


class Form(QDialog):
    def __init__(self, parent=None):
        super(Form, self).__init__(parent)
        self.setWindowTitle('Proxy Settings')

        # create widgets
        self.edit = QLineEdit(proxy.server_check())
        self.button_clear = QPushButton('Clear')
        self.button_save = QPushButton('Save')

        # create layout
        layout = QVBoxLayout()
        layout.addWidget(self.edit)
        layout.addWidget(self.button_clear)
        layout.addWidget(self.button_save)
        # set layout
        self.setLayout(layout)

        # add button signal to proxy_changer slot
        self.button_clear.clicked.connect(self.edit.clear)
        self.button_save.clicked.connect(self.proxy_changer)

    def proxy_changer(self):
        print(self.edit.text())


if __name__ == '__main__':
    # check current settings first
    proxy.status_check()
    proxy.server_check()
    # create QtApplication
    app = QApplication(sys.argv)
    # create and show the window
    settings = Form()
    settings.show()
    # run the main Qt loop
    sys.exit(app.exec())
