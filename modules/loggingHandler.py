import os
import logging
import tempfile
import customtkinter


class TkinterHandler(logging.Handler):
    """
    A logging handler that outputs logs to a Tkinter Text widget.

    Args:
        text_widget (customtkinter.CTkTextbox): The Text widget to output logs to.
    """

    def __init__(self, text_widget):
        logging.Handler.__init__(self)
        self.text_widget = text_widget
        self.text_widget.configure(state='disabled')
        self.log_format = logging.Formatter('%(levelname)s: %(message)s\n')

        # Ensure log directory exists
        log_file = os.path.join(os.path.join(os.path.join(os.path.dirname(
            tempfile.gettempdir()), 'Proxy Settings'), "logs"), "log.txt")
        log_dir = os.path.dirname(log_file)
        if not os.path.exists(log_dir):
            os.makedirs(log_dir)

        # Configure logging to file
        self.file_handler = logging.FileHandler(log_file)
        self.file_handler.setFormatter(
            logging.Formatter('%(asctime)s - %(levelname)s: %(message)s'))
        self.file_handler.setLevel(logging.INFO)
        logging.getLogger().addHandler(self.file_handler)

    def emit(self, record):
        self.text_widget.configure(state='normal')
        self.text_widget.insert(
            customtkinter.END, self.log_format.format(record))
        self.text_widget.see(customtkinter.END)
        self.text_widget.configure(state='disabled')
        self.text_widget.update()
