import sys

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QApplication, QMainWindow

from spinner import WaitingSpinner

app = QApplication(sys.argv)

window = QMainWindow()
window.show()

spinner = WaitingSpinner(
    window,
    disable_parent_when_spinning=True,
    modality=Qt.WindowModality.ApplicationModal,
)
spinner.start()  # starts spinning
app.exec()
