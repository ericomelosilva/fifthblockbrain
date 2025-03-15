import sys
from PyQt5.QtWidgets import (
        QWidget, QMainWindow, QPushButton, 
        QVBoxLayout, QDialog, QFormLayout,
        QLineEdit, QLabel, QDialogButtonBox
)

import database

class AddEnsembleDialog(QDialog):
    """
    A simple dialog with a QLineEdit for typing an ensemble name,
    and OK/Cancel buttons.
    """
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Add Ensemble")

        layout = QFormLayout(self)

        self.ensemble_name_edit = QLineEdit()
        layout.addRow("Ensemble Name:", self.ensemble_name_edit)

        self.button_box = QDialogButtonBox(
                QDialogButtonBox.Ok | QDialogButtonBox.Cancel,
                parent=self
        )
        self.button_box.accepted.connect(self.accept)
        self.button_box.rejected.connect(self.reject)
        layout.addWidget(self.button_box)

    def getEnsembleName(self):
        """
        Returns text from QLineEdit (ensemble name)
        """
        return self.ensemble_name_edit.text().strip()

class MainWindow(QWidget):
    """
    Main application window. Shows a button for "add ensemble" and a 
    label listing all ensembles from db.
    """
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Fifth Block Brain")

        layout = QVBoxLayout()

        self.ensembles_label = QLabel("ensembles will appear here.")
        layout.addWidget(self.ensembles_label)

        self.add_button = QPushButton("Add Ensemble")
        self.add_button.clicked.connect(self.openAddEnsembleDialog)
        layout.addWidget(self.add_button)

        self.setLayout(layout)

        database.create_tables_from_file()
        self.refreshEnsemblesLabel()

    def openAddEnsembleDialog(self):
        """
        Opens the add ensemble dialog. if the user clicks ok it adds
        the ensemble to the database and refreshes the label
        """

        dialog = AddEnsembleDialog(self)
        if dialog.exec() == QDialog.Accepted:
            name = dialog.getEnsembleName()
            if name:
                database.add_ensemble(name)
                self.refreshEnsemblesLabel()

    def refreshEnsemblesLabel(self):
        """
        Fetches all ensembles from the database and updates the label
        """

        ensembles = database.get_ensembles()
        if not ensembles:
            self.ensembles_label.setText("No ensembles yet.")
        else:
            text = "Current Ensembles:\n"
            
            for e_id, e_name in ensembles:
                text += f"ID: {e_id}, Name: {e_name}\n"

            self.ensembles_label.setText(text)

