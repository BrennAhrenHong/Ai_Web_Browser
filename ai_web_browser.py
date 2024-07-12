import os
import traceback
import logging

from mainwindow import MainWindow
from PyQt6.QtWidgets import QApplication, QMessageBox

try:
    mainwindow = MainWindow()

except Exception:
    error_message = str(traceback.format_exc())
    error_window = QMessageBox(QMessageBox.critical, "ERROR!", error_message)
