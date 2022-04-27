import sys
import proxy
import logging
from PySide6.QtWidgets import (
    QLineEdit, QPushButton, QApplication, QVBoxLayout, QDialog, QPlainTextEdit)

# Uncomment below for terminal log messages
# logging.basicConfig(level=logging.DEBUG, format=' %(asctime)s - %(name)s - %(levelname)s - %(message)s')


class QTextEditLogger(logging.Handler):
    def __init__(self, parent):
        super().__init__()
        self.widget = QPlainTextEdit(parent)
        self.widget.setReadOnly(True)

    def emit(self, record):
        msg = self.format(record)
        self.widget.appendPlainText(msg)


class Form(QDialog):
    def __init__(self, parent=None):
        super(Form, self).__init__(parent)
        self.setWindowTitle('Proxy Settings')

        # create widgets
        self.edit = QLineEdit(proxy.server_check())
        self.button_clear = QPushButton('Clear')
        self.button_save = QPushButton('Save')

        self.logTextBox = QTextEditLogger(self)
        # You can format what is printed to text box
        self.logTextBox.setFormatter(logging.Formatter(
            '%(levelname)s - %(message)s'))
        logging.getLogger().addHandler(self.logTextBox)
        # You can control the logging level
        logging.getLogger().setLevel(logging.DEBUG)

        # create layout
        layout = QVBoxLayout()
        layout.addWidget(self.edit)
        layout.addWidget(self.button_clear)
        layout.addWidget(self.button_save)
        layout.addWidget(self.logTextBox.widget)
        # set layout
        self.setLayout(layout)

        # add button signal to proxy_changer slot
        self.button_clear.clicked.connect(self.edit.clear)
        self.button_save.clicked.connect(self.proxy_changer)

    def proxy_changer(self):
        print(self.edit.text())
        logging.info('Clicked a button')


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
