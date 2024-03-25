import logging
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

    def emit(self, record):
        self.text_widget.configure(state='normal')
        self.text_widget.insert(
            customtkinter.END, self.log_format.format(record))
        self.text_widget.see(customtkinter.END)
        self.text_widget.configure(state='disabled')
        self.text_widget.update()
