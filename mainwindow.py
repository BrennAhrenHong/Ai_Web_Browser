import os
import sys

from gui.mainwindow_ui import MainWindow_Ui
from ai_logic import Ai_Logic

from PyQt6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)

from PyQt6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)

from PyQt6.QtWidgets import (QAbstractScrollArea, QApplication, QFrame, QHBoxLayout,
    QMainWindow, QMenuBar, QPushButton, QSizePolicy,
    QSpacerItem, QStatusBar, QTextEdit, QVBoxLayout,
    QWidget)

class MainWindow(QMainWindow, MainWindow_Ui):
    def __init__(self):
        super().__init__()
        # MainWindow
        self.ui = MainWindow_Ui()
        self.ui.setupUi(self)
        self.show()

        self.ui.send_push_button.clicked.connect(lambda: self.send_button_pressed())
        self.ui.clear_push_button.clicked.connect(lambda: self.clear_button_pressed())

    def send_button_pressed(self):
        def save_file(output_text):
            i = 1
            folder = "output_logs"
            filename = f"output_log_{i}.txt"
            full_file_path = os.path.join(folder, filename)
            try:
                if not os.path.exists(folder):
                    try:
                        os.makedirs("output_logs", exist_ok=True)
                    except OSError as e:
                        print("Error creating folder:", e)
                    else:
                        print(f"Log folder created successfully.")

                while os.path.exists(full_file_path):
                    i += 1
                    filename = f"output_log_{i}.txt"
                    full_file_path = os.path.join(folder, filename)

                with open(file=full_file_path, mode="w") as notepad_file:
                    notepad_file.writelines(output_text)
                print(f"Output saved to file path: {full_file_path}")
            except OSError as e:
                if "File exists" in str(e):
                    print(f"{filename} already exists.")
                else:
                    print("An error has occurred during file creation.")
            else:
                print(f"File {filename} created successfully.")

        ai = Ai_Logic()
        self.ui.output_text_edit.setText(ai.start_process(topic=self.ui.input_text_edit.toPlainText()))
        output_text = self.ui.output_text_edit.toPlainText()
        save_file(output_text)

    def clear_button_pressed(self):
        self.ui.output_text_edit.clear()

if __name__ == "__main__":
    app = QApplication(sys.argv)

    app.setApplicationName("AI Web Browser")
    main_window = MainWindow()

    app.exec()