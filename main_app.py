import sys
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QTabWidget, QWidget, QVBoxLayout, QLabel, QPushButton, QMessageBox,
    QLineEdit, QFormLayout, QHBoxLayout, QTableView, QHeaderView, QFileDialog
)
from PyQt6.QtCore import Qt
from modules.candidates.manager import CandidateManager
from modules.job_openings.manager import JobOpeningManager
from modules.cv_parser.parser import CVParser
from modules.ai_analyzer.analyzer import AIAnalyzer
from modules.employees.manager import EmployeeManager
from modules.attendance.manager import AttendanceManager
from modules.payroll.manager import PayrollManager

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("OpenNexus RHIA Manager - Plataforma de RRHH")
        self.setGeometry(100, 100, 1200, 700)
        self.tabs = QTabWidget()
        self.setCentralWidget(self.tabs)
        self.create_candidates_tab()
        self.create_job_openings_tab()
        self.create_employees_tab()
        self.create_attendance_tab()
        self.create_payroll_tab()
        self.create_cv_analysis_tab()

    # --- CANDIDATOS ---
    def create_candidates_tab(self):
        tab = QWidget()
        layout = QVBoxLayout(tab)
        self.candidate_name = QLineEdit()
        self.candidate_job_id = QLineEdit()
        self.candidate_cv_path = QLineEdit()
        form = QFormLayout()
        form.addRow("Nombre:", self.candidate_name)
        form.addRow("ID Puesto:", self.candidate_job_id)
        form.addRow("Ruta CV:", self.candidate_cv_path)
        btn_add = QPushButton("Agregar Candidato")
        btn_add.clicked.connect(self.add_candidate)
        layout.addLayout(form)
        layout.addWidget(btn_add)
        self.candidates_table = QTableView()
        self.candidates_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        layout.addWidget(self.candidates_table)
        tab.setLayout(layout)
        self.tabs.addTab(tab, "Candidatos")
        self.load_candidates()

    def add_candidate(self):
        nombre = self.candidate_name.text().strip()
        puesto_id = int(self.candidate_job_id.text())
        cv_path = self.candidate_cv_path.text().strip()
        with open(cv_path, 'rb') as f:
            cv_bytes = f.read()
        cv_text = CVParser.extract_text(cv_path, cv_bytes)
        job_requirements = {"titulo": "Puesto", "requerimientos": "Requerimientos del puesto"}  # Mejorar: obtener de JobOpeningManager
        analysis = AIAnalyzer.analyze_cv(job_requirements, cv_text)
        CandidateManager.add_candidate(nombre, puesto_id, cv_bytes, str(analysis))
        self.load_candidates()

    def load_candidates(self):
        candidates = CandidateManager.get_candidates()
        data = [[c.id, c.nombre, c.puesto_id] for c in candidates]
        headers = ["ID", "Nombre", "Puesto"]
        from PyQt6.QtCore import QAbstractTableModel
        class TableModel(QAbstractTableModel):
            def __init__(self, data, headers):
                super().__init__()
                self._data = data
                self.headers = headers
            def rowCount(self, parent=None):
                return len(self._data)
            def columnCount(self, parent=None):
                return len(self.headers)
            def data(self, index, role):
                if role == Qt.ItemDataRole.DisplayRole:
                    return self._data[index.row()][index.column()]
                return None
            def headerData(self, section, orientation, role):
                if role == Qt.ItemDataRole.DisplayRole and orientation == Qt.Orientation.Horizontal:
                    return self.headers[section]
                return None
        model = TableModel(data, headers)
        self.candidates_table.setModel(model)

    # --- VACANTES ---
    def create_job_openings_tab(self):
        tab = QWidget()
        layout = QVBoxLayout(tab)
        self.job_name = QLineEdit()
        form = QFormLayout()
        form.addRow("Nombre del Puesto:", self.job_name)
        btn_add = QPushButton("Agregar Puesto")
        btn_add.clicked.connect(self.add_job_opening)
        layout.addLayout(form)
        layout.addWidget(btn_add)
        self.jobs_table = QTableView()
        self.jobs_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        layout.addWidget(self.jobs_table)
        tab.setLayout(layout)
        self.tabs.addTab(tab, "Vacantes")
        self.load_job_openings()

    def add_job_opening(self):
        nombre = self.job_name.text().strip()
        JobOpeningManager.add_job_opening(nombre)
        self.load_job_openings()

    def load_job_openings(self):
        jobs = JobOpeningManager.get_job_openings()
        data = [[j.id, j.nombre] for j in jobs]
        headers = ["ID", "Nombre"]
        from PyQt6.QtCore import QAbstractTableModel
        class TableModel(QAbstractTableModel):
            def __init__(self, data, headers):
                super().__init__()
                self._data = data
                self.headers = headers
            def rowCount(self, parent=None):
                return len(self._data)
            def columnCount(self, parent=None):
                return len(self.headers)
            def data(self, index, role):
                if role == Qt.ItemDataRole.DisplayRole:
                    return self._data[index.row()][index.column()]
                return None
            def headerData(self, section, orientation, role):
                if role == Qt.ItemDataRole.DisplayRole and orientation == Qt.Orientation.Horizontal:
                    return self.headers[section]
                return None
        model = TableModel(data, headers)
        self.jobs_table.setModel(model)

    # --- EMPLEADOS ---
    def create_employees_tab(self):
        tab = QWidget()
        layout = QVBoxLayout(tab)
        self.emp_name = QLineEdit()
        self.emp_cedula = QLineEdit()
        self.emp_iban = QLineEdit()
        self.emp_badge = QLineEdit()
        self.emp_salary = QLineEdit()
        form = QFormLayout()
        form.addRow("Nombre:", self.emp_name)
        form.addRow("Cédula:", self.emp_cedula)
        form.addRow("IBAN:", self.emp_iban)
        form.addRow("Badge:", self.emp_badge)
        form.addRow("Salario Base:", self.emp_salary)
        btn_add = QPushButton("Agregar Empleado")
        btn_add.clicked.connect(self.add_employee)
        layout.addLayout(form)
        layout.addWidget(btn_add)
        self.employees_table = QTableView()
        self.employees_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        layout.addWidget(self.employees_table)
        tab.setLayout(layout)
        self.tabs.addTab(tab, "Empleados")
        self.load_employees()

    def add_employee(self):
        nombre = self.emp_name.text().strip()
        cedula = self.emp_cedula.text().strip()
        iban = self.emp_iban.text().strip()
        badge = self.emp_badge.text().strip()
        try:
            salario_base = float(self.emp_salary.text().strip())
        except ValueError:
            salario_base = 0.0
        EmployeeManager.add_employee(nombre, cedula, iban, badge, salario_base)
        self.load_employees()

    def load_employees(self):
        employees = EmployeeManager.get_employees()
        data = [[e.id, e.nombre, e.cedula, e.iban, e.badge, e.salario_base] for e in employees]
        headers = ["ID", "Nombre", "Cédula", "IBAN", "Badge", "Salario Base"]
        from PyQt6.QtCore import QAbstractTableModel
        class TableModel(QAbstractTableModel):
            def __init__(self, data, headers):
                super().__init__()
                self._data = data
                self.headers = headers
            def rowCount(self, parent=None):
                return len(self._data)
            def columnCount(self, parent=None):
                return len(self.headers)
            def data(self, index, role):
                if role == Qt.ItemDataRole.DisplayRole:
                    return self._data[index.row()][index.column()]
                return None
            def headerData(self, section, orientation, role):
                if role == Qt.ItemDataRole.DisplayRole and orientation == Qt.Orientation.Horizontal:
                    return self.headers[section]
                return None
        model = TableModel(data, headers)
        self.employees_table.setModel(model)

    # --- ASISTENCIA ---
    def create_attendance_tab(self):
        tab = QWidget()
        layout = QVBoxLayout(tab)
        self.att_emp_id = QLineEdit()
        self.att_fecha = QLineEdit()
        self.att_tipo = QLineEdit()
        form = QFormLayout()
        form.addRow("ID Empleado:", self.att_emp_id)
        form.addRow("Fecha (YYYY-MM-DD HH:MM):", self.att_fecha)
        form.addRow("Tipo (entrada/salida):", self.att_tipo)
        btn_add = QPushButton("Agregar Asistencia")
        btn_add.clicked.connect(self.add_attendance)
        layout.addLayout(form)
        layout.addWidget(btn_add)
        self.attendance_table = QTableView()
        self.attendance_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        layout.addWidget(self.attendance_table)
        tab.setLayout(layout)
        self.tabs.addTab(tab, "Asistencia")
        self.load_attendance()

    def add_attendance(self):
        from datetime import datetime
        try:
            empleado_id = int(self.att_emp_id.text())
            fecha = datetime.strptime(self.att_fecha.text().strip(), "%Y-%m-%d %H:%M")
            tipo = self.att_tipo.text().strip()
        except Exception:
            QMessageBox.warning(self, "Datos inválidos", "Verifica los campos de asistencia.")
            return
        AttendanceManager.add_attendance(empleado_id, fecha, tipo)
        self.load_attendance()

    def load_attendance(self):
        attendances = AttendanceManager.get_attendances()
        data = [[a.id, a.empleado_id, a.fecha.strftime('%Y-%m-%d %H:%M'), a.tipo] for a in attendances]
        headers = ["ID", "Empleado", "Fecha", "Tipo"]
        from PyQt6.QtCore import QAbstractTableModel
        class TableModel(QAbstractTableModel):
            def __init__(self, data, headers):
                super().__init__()
                self._data = data
                self.headers = headers
            def rowCount(self, parent=None):
                return len(self._data)
            def columnCount(self, parent=None):
                return len(self.headers)
            def data(self, index, role):
                if role == Qt.ItemDataRole.DisplayRole:
                    return self._data[index.row()][index.column()]
                return None
            def headerData(self, section, orientation, role):
                if role == Qt.ItemDataRole.DisplayRole and orientation == Qt.Orientation.Horizontal:
                    return self.headers[section]
                return None
        model = TableModel(data, headers)
        self.attendance_table.setModel(model)

    # --- PLANILLA ---
    def create_payroll_tab(self):
        tab = QWidget()
        layout = QVBoxLayout(tab)
        self.pay_emp_id = QLineEdit()
        self.pay_inicio = QLineEdit()
        self.pay_fin = QLineEdit()
        self.pay_bruto = QLineEdit()
        self.pay_deducciones = QLineEdit()
        self.pay_neto = QLineEdit()
        form = QFormLayout()
        form.addRow("ID Empleado:", self.pay_emp_id)
        form.addRow("Inicio Periodo (YYYY-MM-DD):", self.pay_inicio)
        form.addRow("Fin Periodo (YYYY-MM-DD):", self.pay_fin)
        form.addRow("Salario Bruto:", self.pay_bruto)
        form.addRow("Deducciones:", self.pay_deducciones)
        form.addRow("Salario Neto:", self.pay_neto)
        btn_add = QPushButton("Agregar Planilla")
        btn_add.clicked.connect(self.add_payroll)
        layout.addLayout(form)
        layout.addWidget(btn_add)
        self.payroll_table = QTableView()
        self.payroll_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        layout.addWidget(self.payroll_table)
        tab.setLayout(layout)
        self.tabs.addTab(tab, "Planilla")
        self.load_payroll()

    def add_payroll(self):
        from datetime import datetime
        try:
            empleado_id = int(self.pay_emp_id.text())
            inicio = datetime.strptime(self.pay_inicio.text().strip(), "%Y-%m-%d")
            fin = datetime.strptime(self.pay_fin.text().strip(), "%Y-%m-%d")
            bruto = float(self.pay_bruto.text().strip())
            deducciones = float(self.pay_deducciones.text().strip())
            neto = float(self.pay_neto.text().strip())
        except Exception:
            QMessageBox.warning(self, "Datos inválidos", "Verifica los campos de planilla.")
            return
        PayrollManager.add_payroll(empleado_id, inicio, fin, bruto, deducciones, neto)
        self.load_payroll()

    def load_payroll(self):
        payrolls = PayrollManager.get_payrolls()
        data = [[p.id, p.empleado_id, p.periodo_inicio.strftime('%Y-%m-%d'), p.periodo_fin.strftime('%Y-%m-%d'), p.salario_bruto, p.deducciones, p.salario_neto] for p in payrolls]
        headers = ["ID", "Empleado", "Inicio", "Fin", "Bruto", "Deducciones", "Neto"]
        from PyQt6.QtCore import QAbstractTableModel
        class TableModel(QAbstractTableModel):
            def __init__(self, data, headers):
                super().__init__()
                self._data = data
                self.headers = headers
            def rowCount(self, parent=None):
                return len(self._data)
            def columnCount(self, parent=None):
                return len(self.headers)
            def data(self, index, role):
                if role == Qt.ItemDataRole.DisplayRole:
                    return self._data[index.row()][index.column()]
                return None
            def headerData(self, section, orientation, role):
                if role == Qt.ItemDataRole.DisplayRole and orientation == Qt.Orientation.Horizontal:
                    return self.headers[section]
                return None
        model = TableModel(data, headers)
        self.payroll_table.setModel(model)

    # --- ANÁLISIS DE CV CON IA ---
    def create_cv_analysis_tab(self):
        tab = QWidget()
        layout = QVBoxLayout(tab)
        label = QLabel("Análisis de CV con IA")
        layout.addWidget(label)
        btn_upload = QPushButton("Subir y analizar CV")
        btn_upload.clicked.connect(self.upload_and_analyze_cv)
        layout.addWidget(btn_upload)
        self.analysis_result = QLabel("")
        layout.addWidget(self.analysis_result)
        tab.setLayout(layout)
        self.tabs.addTab(tab, "Análisis IA")

    def upload_and_analyze_cv(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Selecciona el CV", "", "Archivos (*.pdf *.docx *.xlsx *.txt)")
        if file_path:
            with open(file_path, 'rb') as f:
                file_bytes = f.read()
            cv_text = CVParser.extract_text(file_path, file_bytes)
            job_requirements = {"titulo": "Puesto", "requerimientos": "Requerimientos del puesto"}  # Mejorar: obtener de JobOpeningManager
            analysis = AIAnalyzer.analyze_cv(job_requirements, cv_text)
            self.analysis_result.setText(str(analysis))

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
