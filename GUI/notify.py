import sys
from PyQt6.QtWidgets import *

class Notify:
    def __init__(self, condition, message, detailed_text=None):
        self.condition = condition
        self.message = message
        self.detailed_text = detailed_text

    def show(self):
        if self.condition:
            msg_box = QMessageBox(QMessageBox.Warning, "Warning", self.message)
            if self.detailed_text:
                msg_box.setDetailedText(self.detailed_text)
            response = msg_box.exec()
            if response == QMessageBox.Ok:
                print("Thank you, further details can be seen in the console.")
            else:
                print("The warning has been ignored, please take caution while proceeding.")

# To use this class in main, create a Notify object with the
# condition, message, and optional detailed text as seen below.
#
# notify = Notify(True, "Your warning message here", "Additional information about the warning can be displayed here.")
#
# Use the following to show the warning message if the condition is met
#
# notify.show()
