import sys
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QTabWidget, QVBoxLayout, QPushButton,
    QTableView, QHeaderView, QFormLayout, QLineEdit, QLabel, QDialog, QMessageBox, QFileDialog
)
from PyQt6.QtCore import Qt, QAbstractTableModel
from models import Session, Empleado, Candidato, Puesto
from export_utils import export_employees_to_excel, export_candidates_to_pdf
from recruitment import process_candidate_application

class EmployeeTableModel(QAbstractTableModel):
    headers = ["ID", "Nombre", "Badge", "Cédula", "IBAN"]
    def __init__(self, data=None):
        super().__init__()
        self._data = data or []
    def rowCount(self, parent=None):
        return len(self._data)
    def columnCount(self, parent=None):
        return len(self.headers)
    def data(self, index, role=Qt.ItemDataRole.DisplayRole):
        if role == Qt.ItemDataRole.DisplayRole:
            return self._data[index.row()][index.column()]
    def headerData(self, section, orientation, role):
        if role == Qt.ItemDataRole.DisplayRole and orientation == Qt.Orientation.Horizontal:
            return self.headers[section]

class RecruitmentTab(QWidget):
    def __init__(self, session):
        super().__init__()
        self.session = session
        layout = QVBoxLayout()
        self.upload_btn = QPushButton("Subir CV")
        self.upload_btn.clicked.connect(self.upload_cv)
        layout.addWidget(self.upload_btn)
        self.setLayout(layout)
    def upload_cv(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Selecciona el CV", "", "Archivos (*.pdf *.docx *.html *.txt)")
        if file_path:
            # Simulación de requerimientos
            job_requirements = {
                "puesto": "Ingeniero de Software Senior (Backend)",
                "requerimientos": "5+ años de experiencia profesional en desarrollo de software. Experiencia sólida con Python y el framework Django o FastAPI. Experiencia con bases de datos PostgreSQL. Nivel de inglés: B2 o superior. Título universitario en Ingeniería de Sistemas o carrera afín. Deseable: Experiencia con Docker y AWS."
            }
            analysis = process_candidate_application(1, file_path, job_requirements)
            QMessageBox.information(self, "Análisis IA", str(analysis))

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.session = Session()
        self.setWindowTitle("RRHH App Modular")
        self.resize(900, 600)
        tabs = QTabWidget()
        tabs.addTab(self.create_employees_tab(), "Empleados")
        tabs.addTab(RecruitmentTab(self.session), "Reclutamiento")
        self.setCentralWidget(tabs)
    def create_employees_tab(self):
        widget = QWidget()
        layout = QVBoxLayout()
        self.table = QTableView()
        self.load_employees()
        layout.addWidget(self.table)
        export_btn = QPushButton("Exportar a Excel")
        export_btn.clicked.connect(self.export_excel)
        layout.addWidget(export_btn)
        widget.setLayout(layout)
        return widget
    def load_employees(self):
        empleados = self.session.query(Empleado).all()
        data = [[e.id, e.nombre, e.badge, e.cedula, e.iban] for e in empleados]
        self.table.setModel(EmployeeTableModel(data))
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
    def export_excel(self):
        file_path, _ = QFileDialog.getSaveFileName(self, "Guardar Excel", "", "Excel Files (*.xlsx)")
        if file_path:
            export_employees_to_excel(self.session, file_path)
            QMessageBox.information(self, "Exportación", "Empleados exportados correctamente.")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
