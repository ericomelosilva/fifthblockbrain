import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel
import database 
class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self): 
        layout = QVBoxLayout()
        self.label = QLabel("Loading data...")
        layout.addWidget(self.label)

        self.setLayout(layout)
        self.setWindowTitle("Attendance App Test")

        database.create_tables_from_file()

        database.add_ensemble("Test Ensemble")

        ensembles = database.get_ensembles()  # e.g., returns a list of tuples [(id, name), ...]

        message = "Ensembles in DB:\n"
        for e_id, e_name in ensembles:
            message += f"ID: {e_id}, Name: {e_name}\n"

        self.label.setText(message)

def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()

