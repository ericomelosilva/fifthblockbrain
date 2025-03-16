import sys
from PyQt5.QtWidgets import (
        QComboBox, QDoubleSpinBox, QWidget, QMainWindow, QPushButton, 
        QVBoxLayout, QDialog, QFormLayout,
        QLineEdit, QLabel, QDialogButtonBox
)

import database

class EnsembleConfigDialog(QDialog):
    """
    A dialog for configuring ensemble parameters
    """
    def __init__(self, current_config, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Configure Ensemble")

        layout = QFormLayout(self)

        self.absence_spin = QDoubleSpinBox()
        self.absence_spin.setRange(0, 10)
        self.absence_spin.setValue(current_config[0] if current_config else 1.0)
        layout.addRow("Absence Weight:", self.absence_spin)

        self.late_early_spin = QDoubleSpinBox()
        self.late_early_spin.setRange(0, 10)
        self.late_early_spin.setValue(current_config[1] if current_config else 0.5)
        layout.addRow("Arrive Late/Leave Early Weight:", self.late_early_spin)


        self.threshold_spin = QDoubleSpinBox()
        self.threshold_spin.setRange(0, 100)
        self.threshold_spin.setValue(current_config[2] if current_config else 2.0)
        layout.addRow("Makeup Threshold:", self.threshold_spin)

        self.button_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        self.button_box.accepted.connect(self.accept)
        self.button_box.rejected.connect(self.reject)
        layout.addWidget(self.button_box)

    def getConfig(self):
        return (
            self.absence_spin.value(),
            self.late_early_spin.value(),
            self.threshold_spin.value()
        )
        

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
        self.resize(800, 600)

        database.create_tables_from_file()

        layout = QVBoxLayout()

        self.ensemble_selector = QComboBox()
        self.refreshEnsembleSelector()
        layout.addWidget(self.ensemble_selector)

        self.configure_button = QPushButton("Configure Selected Ensemble")
        self.configure_button.clicked.connect(self.configureEnsemble)
        layout.addWidget(self.configure_button)


        self.ensembles_label = QLabel("ensembles will appear here.")
        layout.addWidget(self.ensembles_label)

        self.add_button = QPushButton("Add Ensemble")
        self.add_button.clicked.connect(self.openAddEnsembleDialog)
        layout.addWidget(self.add_button)

        self.setLayout(layout)
        
        self.refreshEnsemblesLabel()
        self.refreshEnsembleSelector()

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
                self.refreshEnsembleSelector()

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

    def openConfigureEnsembleDialog(self, ensemble_id):
        current_config = database.get_ensemble_config(ensemble_id)
        dialog = EnsembleConfigDialog(current_config, self)
        
        if dialog.exec() == QDialog.accepted:
            new_config = dialog.getConfig()
            database.update_ensemble_config(ensemble_id, *new_config)
            print("Config updated.")


    def refreshEnsembleSelector(self):
        """
        Fill combo box with all the ensembles from the database
        """

        self.ensemble_selector.clear()
        ensembles = database.get_ensembles()
        for e_id, e_name in ensembles:
            self.ensemble_selector.addItem(e_name, e_id)

    def configureEnsemble(self):
        """
        Retrieve selected ensembles id and open config dialog
        """
        ensemble_id = self.ensemble_selector.currentData()
        if ensemble_id is not None:
            self.openConfigureEnsembleDialog(ensemble_id)
        else:
            print("No ensemble selected.")
