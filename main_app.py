import sys
from PyQt6.QtWidgets import (
    QApplication,
    QMainWindow,
    QTabWidget,
    QWidget,
    QVBoxLayout,
    QLabel,
    QPushButton,
    QMessageBox,
    QLineEdit,
    QFormLayout,
    QHBoxLayout,
    QTableView,
    QHeaderView
)
from PyQt6.QtCore import Qt
from models import Session, Empleado

# Ejemplo de ventana emergente pesada con tkinter y ttkthemes
def show_heavy_popup():
    import tkinter as tk
    from tkinter import ttk
    try:
        from ttkthemes import ThemedTk
        root = ThemedTk(theme="arc")
    except Exception:
        root = tk.Tk()
    root.title("Ventana Emergente Pesada")
    label = ttk.Label(root, text="Procesando operación pesada...", font=("Arial", 16))
    label.pack(padx=20, pady=20)
    btn = ttk.Button(root, text="Cerrar", command=root.destroy)
    btn.pack(pady=10)
    root.mainloop()

class MainWindow(QMainWindow):
    # --- CRUD Planilla ---
    def add_planilla(self, empleado_id, periodo_inicio, periodo_fin, salario_bruto, deducciones, salario_neto):
        from models import Session, Planilla
        with Session() as session:
            nueva_planilla = Planilla(
                empleado_id=empleado_id,
                periodo_inicio=periodo_inicio,
                periodo_fin=periodo_fin,
                salario_bruto=salario_bruto,
                deducciones=deducciones,
                salario_neto=salario_neto
            )
            session.add(nueva_planilla)
            session.commit()
        QMessageBox.information(self, "Éxito", "Planilla agregada correctamente.")

    def get_planillas(self, empleado_id=None):
        from models import Session, Planilla
        with Session() as session:
            query = session.query(Planilla)
            if empleado_id:
                query = query.filter(Planilla.empleado_id == empleado_id)
            return query.order_by(Planilla.periodo_inicio.desc()).all()

    def update_planilla(self, planilla_id, **kwargs):
        from models import Session, Planilla
        with Session() as session:
            planilla = session.get(Planilla, planilla_id)
            for key, value in kwargs.items():
                setattr(planilla, key, value)
            session.commit()
        QMessageBox.information(self, "Éxito", "Planilla actualizada correctamente.")

    def delete_planilla(self, planilla_id):
        from models import Session, Planilla
        with Session() as session:
            planilla = session.get(Planilla, planilla_id)
            session.delete(planilla)
            session.commit()
        QMessageBox.information(self, "Éxito", "Planilla eliminada correctamente.")

    # --- CRUD Asistencia ---
    def add_asistencia(self, empleado_id, fecha_hora_entrada, fecha_hora_salida=None):
        from models import Session, Asistencia
        with Session() as session:
            nueva_asistencia = Asistencia(
                empleado_id=empleado_id,
                fecha_hora_entrada=fecha_hora_entrada,
                fecha_hora_salida=fecha_hora_salida
            )
            session.add(nueva_asistencia)
            session.commit()
        QMessageBox.information(self, "Éxito", "Asistencia agregada correctamente.")

    def get_asistencias(self, empleado_id=None):
        from models import Session, Asistencia
        with Session() as session:
            query = session.query(Asistencia)
            if empleado_id:
                query = query.filter(Asistencia.empleado_id == empleado_id)
            return query.order_by(Asistencia.fecha_hora_entrada.desc()).all()

    def update_asistencia(self, asistencia_id, **kwargs):
        from models import Session, Asistencia
        with Session() as session:
            asistencia = session.get(Asistencia, asistencia_id)
            for key, value in kwargs.items():
                setattr(asistencia, key, value)
            session.commit()
        QMessageBox.information(self, "Éxito", "Asistencia actualizada correctamente.")

    def delete_asistencia(self, asistencia_id):
        from models import Session, Asistencia
        with Session() as session:
            asistencia = session.get(Asistencia, asistencia_id)
            session.delete(asistencia)
            session.commit()
        QMessageBox.information(self, "Éxito", "Asistencia eliminada correctamente.")
    def __init__(self):
        super().__init__()
        self.setWindowTitle("OpenNexus RHIA Manager - Plataforma de RRHH")
        self.setGeometry(100, 100, 1200, 700)

        self.tabs = QTabWidget()
        self.setCentralWidget(self.tabs)

        self.create_empleados_tab()
        self.create_horarios_tab()
        self.create_planillas_tab()
        self.create_reclutamiento_tab()

    def create_empleados_tab(self):
        tab = QWidget()
        layout = QVBoxLayout(tab)
        form_layout = QFormLayout()
        self.emp_nombre = QLineEdit()
        self.emp_cedula = QLineEdit()
        self.emp_iban = QLineEdit()
        self.emp_salario = QLineEdit()
        form_layout.addRow("Nombre Completo:", self.emp_nombre)
        form_layout.addRow("Cédula:", self.emp_cedula)
        form_layout.addRow("Cuenta IBAN:", self.emp_iban)
        form_layout.addRow("Salario Base:", self.emp_salario)
        layout.addLayout(form_layout)
        btn_layout = QHBoxLayout()
        btn_add = QPushButton("Agregar Empleado")
        btn_add.clicked.connect(self.add_empleado)
        btn_layout.addWidget(btn_add)
        btn_popup = QPushButton("Mostrar ventana pesada (tkinter)")
        btn_popup.clicked.connect(show_heavy_popup)
        btn_layout.addWidget(btn_popup)
        layout.addLayout(btn_layout)
        self.empleados_table = QTableView()
        self.empleados_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        layout.addWidget(self.empleados_table)
        tab.setLayout(layout)
        self.tabs.addTab(tab, "Empleados")
        self.load_empleados_data()

    def add_empleado(self):
        nombre = self.emp_nombre.text().strip()
        cedula = self.emp_cedula.text().strip()
        iban = self.emp_iban.text().strip()
        salario_str = self.emp_salario.text().strip()
        if not all([nombre, cedula, iban, salario_str]):
            QMessageBox.warning(self, "Datos incompletos", "Todos los campos son requeridos.")
            return
        try:
            salario_base = float(salario_str)
        except ValueError:
            QMessageBox.warning(self, "Dato Inválido", "El salario base debe ser un número.")
            return
        with Session() as session:
            session.add(Empleado(nombre=nombre, cedula=cedula, iban=iban, salario_base=salario_base))
            session.commit()
        self.load_empleados_data()
        for widget in [self.emp_nombre, self.emp_cedula, self.emp_iban, self.emp_salario]:
            widget.clear()

    def load_empleados_data(self):
        with Session() as session:
            empleados = session.query(Empleado).order_by(Empleado.nombre).all()
            data = [[e.id, e.nombre, e.cedula, e.iban, f"₡{e.salario_base:,.2f}"] for e in empleados]
            headers = ["ID", "Nombre", "Cédula", "IBAN", "Salario Base"]
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
            self.empleados_table.setModel(model)

    def create_horarios_tab(self):
        tab = QWidget()
        layout = QVBoxLayout(tab)
        layout.addWidget(QLabel("Control de Horarios", alignment=Qt.AlignmentFlag.AlignCenter))
        tab.setLayout(layout)
        self.tabs.addTab(tab, "Horarios")

    def create_planillas_tab(self):
        # --- UI para Planilla ---
        tab = QWidget()
        layout = QVBoxLayout(tab)
        layout.addWidget(QLabel("Gestión de Planilla", alignment=Qt.AlignmentFlag.AlignCenter))
        form_layout = QFormLayout()
        self.planilla_emp_id = QLineEdit()
        self.planilla_inicio = QLineEdit()
        self.planilla_fin = QLineEdit()
        self.planilla_bruto = QLineEdit()
        self.planilla_deducciones = QLineEdit()
        self.planilla_neto = QLineEdit()
        form_layout.addRow("ID Empleado:", self.planilla_emp_id)
        form_layout.addRow("Inicio Periodo (YYYY-MM-DD):", self.planilla_inicio)
        form_layout.addRow("Fin Periodo (YYYY-MM-DD):", self.planilla_fin)
        form_layout.addRow("Salario Bruto:", self.planilla_bruto)
        form_layout.addRow("Deducciones:", self.planilla_deducciones)
        form_layout.addRow("Salario Neto:", self.planilla_neto)
        layout.addLayout(form_layout)
        btn_add = QPushButton("Agregar Planilla")
        btn_add.clicked.connect(self.ui_add_planilla)
        layout.addWidget(btn_add)
        self.planilla_table = QTableView()
        self.planilla_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        layout.addWidget(self.planilla_table)
        tab.setLayout(layout)
        self.tabs.addTab(tab, "Planilla")
        self.load_planilla_data()

    def ui_add_planilla(self):
        # Validación básica y uso del método CRUD
        try:
            emp_id = int(self.planilla_emp_id.text())
            inicio = self.planilla_inicio.text()
            fin = self.planilla_fin.text()
            bruto = float(self.planilla_bruto.text())
            deducciones = float(self.planilla_deducciones.text())
            neto = float(self.planilla_neto.text())
        except ValueError:
            QMessageBox.warning(self, "Datos inválidos", "Verifica los campos numéricos.")
            return
        from datetime import datetime
        try:
            inicio_dt = datetime.strptime(inicio, "%Y-%m-%d")
            fin_dt = datetime.strptime(fin, "%Y-%m-%d")
        except Exception:
            QMessageBox.warning(self, "Fecha inválida", "Usa el formato YYYY-MM-DD.")
            return
        self.add_planilla(emp_id, inicio_dt, fin_dt, bruto, deducciones, neto)
        self.load_planilla_data()
        for widget in [self.planilla_emp_id, self.planilla_inicio, self.planilla_fin, self.planilla_bruto, self.planilla_deducciones, self.planilla_neto]:
            widget.clear()

    def load_planilla_data(self):
        # Visualización de planillas en tabla
        planillas = self.get_planillas()
        data = [[p.id, p.empleado_id, p.periodo_inicio.strftime('%Y-%m-%d'), p.periodo_fin.strftime('%Y-%m-%d'), f"₡{p.salario_bruto:,.2f}", f"₡{p.deducciones:,.2f}", f"₡{p.salario_neto:,.2f}"] for p in planillas]
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
        self.planilla_table.setModel(model)


    def create_reclutamiento_tab(self):
        tab = QWidget()
        layout = QVBoxLayout(tab)
        layout.addWidget(QLabel("Reclutamiento Inteligente", alignment=Qt.AlignmentFlag.AlignCenter))
        tab.setLayout(layout)
        self.tabs.addTab(tab, "Reclutamiento")

    # --- CRUD Puesto ---
    def add_puesto(self, titulo, descripcion, requerimientos):
        from models import Session, Puesto
        with Session() as session:
            nuevo_puesto = Puesto(titulo=titulo, descripcion=descripcion, requerimientos=requerimientos)
            session.add(nuevo_puesto)
            session.commit()
        QMessageBox.information(self, "Éxito", "Puesto agregado correctamente.")

    def get_puestos(self):
        from models import Session, Puesto
        with Session() as session:
            return session.query(Puesto).order_by(Puesto.titulo).all()

    def update_puesto(self, puesto_id, **kwargs):
        from models import Session, Puesto
        with Session() as session:
            puesto = session.get(Puesto, puesto_id)
            for key, value in kwargs.items():
                setattr(puesto, key, value)
            session.commit()
        QMessageBox.information(self, "Éxito", "Puesto actualizado correctamente.")

    def delete_puesto(self, puesto_id):
        from models import Session, Puesto
        with Session() as session:
            puesto = session.get(Puesto, puesto_id)
            session.delete(puesto)
            session.commit()
        QMessageBox.information(self, "Éxito", "Puesto eliminado correctamente.")

    # --- CRUD Candidato ---
    def add_candidato(self, nombre, puesto_id, cv_texto, puntuacion_general=0):
        from models import Session, Candidato
        with Session() as session:
            nuevo_candidato = Candidato(
                nombre=nombre,
                puesto_id=puesto_id,
                cv_texto=cv_texto,
                puntuacion_general=puntuacion_general
            )
            session.add(nuevo_candidato)
            session.commit()
        QMessageBox.information(self, "Éxito", "Candidato agregado correctamente.")

    def get_candidatos(self, puesto_id=None):
        from models import Session, Candidato
        with Session() as session:
            query = session.query(Candidato)
            if puesto_id:
                query = query.filter(Candidato.puesto_id == puesto_id)
            return query.order_by(Candidato.nombre).all()

    def update_candidato(self, candidato_id, **kwargs):
        from models import Session, Candidato
        with Session() as session:
            candidato = session.get(Candidato, candidato_id)
            for key, value in kwargs.items():
                setattr(candidato, key, value)
            session.commit()
        QMessageBox.information(self, "Éxito", "Candidato actualizado correctamente.")

    def delete_candidato(self, candidato_id):
        from models import Session, Candidato
        with Session() as session:
            candidato = session.get(Candidato, candidato_id)
            session.delete(candidato)
            session.commit()
        QMessageBox.information(self, "Éxito", "Candidato eliminado correctamente.")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    dark_palette = app.palette()
    dark_palette.setColor(app.palette().Window, Qt.GlobalColor.black)
    dark_palette.setColor(app.palette().WindowText, Qt.GlobalColor.white)
    dark_palette.setColor(app.palette().Base, Qt.GlobalColor.black)
    dark_palette.setColor(app.palette().AlternateBase, Qt.GlobalColor.gray)
    dark_palette.setColor(app.palette().ToolTipBase, Qt.GlobalColor.white)
    dark_palette.setColor(app.palette().ToolTipText, Qt.GlobalColor.white)
    dark_palette.setColor(app.palette().Text, Qt.GlobalColor.white)
    dark_palette.setColor(app.palette().Button, Qt.GlobalColor.black)
    dark_palette.setColor(app.palette().ButtonText, Qt.GlobalColor.white)
    dark_palette.setColor(app.palette().BrightText, Qt.GlobalColor.red)
    app.setPalette(dark_palette)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
import sys
from PyQt6.QtWidgets import (
    QApplication,
    QMainWindow,
    QTabWidget,
    QWidget,
    QVBoxLayout,
    QLabel,
    QPushButton,
    QMessageBox
)
from PyQt6.QtCore import Qt

# Ejemplo de ventana emergente pesada con tkinter y ttkthemes
def show_heavy_popup():
    import tkinter as tk
    from tkinter import ttk
    try:
        from ttkthemes import ThemedTk
        root = ThemedTk(theme="arc")
    except Exception:
        root = tk.Tk()
    root.title("Ventana Emergente Pesada")
    label = ttk.Label(root, text="Procesando operación pesada...", font=("Arial", 16))
    label.pack(padx=20, pady=20)
    btn = ttk.Button(root, text="Cerrar", command=root.destroy)
    btn.pack(pady=10)
    root.mainloop()

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("OpenNexus RHIA Manager - Plataforma de RRHH")
        self.setGeometry(100, 100, 1200, 700)

        self.tabs = QTabWidget()
        self.setCentralWidget(self.tabs)

        self.create_empleados_tab()
        self.create_horarios_tab()
        self.create_planillas_tab()
        self.create_reclutamiento_tab()

    def create_empleados_tab(self):
        tab = QWidget()
        layout = QVBoxLayout(tab)
        layout.addWidget(QLabel("Gestión de Empleados", alignment=Qt.AlignmentFlag.AlignCenter))
        btn_popup = QPushButton("Mostrar ventana pesada (tkinter)")
        btn_popup.clicked.connect(show_heavy_popup)
        layout.addWidget(btn_popup)
        tab.setLayout(layout)
        self.tabs.addTab(tab, "Empleados")

    def create_horarios_tab(self):
        # --- UI para Asistencia ---
        tab = QWidget()
        layout = QVBoxLayout(tab)
        layout.addWidget(QLabel("Control de Asistencia", alignment=Qt.AlignmentFlag.AlignCenter))
        form_layout = QFormLayout()
        self.asist_emp_id = QLineEdit()
        self.asist_entrada = QLineEdit()
        self.asist_salida = QLineEdit()
        form_layout.addRow("ID Empleado:", self.asist_emp_id)
        form_layout.addRow("Entrada (YYYY-MM-DD HH:MM):", self.asist_entrada)
        form_layout.addRow("Salida (YYYY-MM-DD HH:MM, opcional):", self.asist_salida)
        layout.addLayout(form_layout)
        btn_add = QPushButton("Agregar Asistencia")
        btn_add.clicked.connect(self.ui_add_asistencia)
        layout.addWidget(btn_add)
        self.asist_table = QTableView()
        self.asist_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        layout.addWidget(self.asist_table)
        tab.setLayout(layout)
        self.tabs.addTab(tab, "Asistencia")
        self.load_asist_data()

    def ui_add_asistencia(self):
        # Validación básica y uso del método CRUD
        try:
            emp_id = int(self.asist_emp_id.text())
            entrada = self.asist_entrada.text()
            salida = self.asist_salida.text()
        except ValueError:
            QMessageBox.warning(self, "Datos inválidos", "Verifica los campos numéricos.")
            return
        from datetime import datetime
        try:
            entrada_dt = datetime.strptime(entrada, "%Y-%m-%d %H:%M")
        except Exception:
            QMessageBox.warning(self, "Fecha de entrada inválida", "Usa el formato YYYY-MM-DD HH:MM.")
            return
        salida_dt = None
        if salida:
            try:
                salida_dt = datetime.strptime(salida, "%Y-%m-%d %H:%M")
            except Exception:
                QMessageBox.warning(self, "Fecha de salida inválida", "Usa el formato YYYY-MM-DD HH:MM.")
                return
        self.add_asistencia(emp_id, entrada_dt, salida_dt)
        self.load_asist_data()
        for widget in [self.asist_emp_id, self.asist_entrada, self.asist_salida]:
            widget.clear()

    def load_asist_data(self):
        # Visualización de asistencias en tabla
        asistencias = self.get_asistencias()
        data = []
        for a in asistencias:
            entrada = a.fecha_hora_entrada.strftime('%Y-%m-%d %H:%M')
            salida = a.fecha_hora_salida.strftime('%Y-%m-%d %H:%M') if a.fecha_hora_salida else "PENDIENTE"
            data.append([a.id, a.empleado_id, entrada, salida])
        headers = ["ID", "Empleado", "Entrada", "Salida"]
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
        self.asist_table.setModel(model)


    def create_planillas_tab(self):
        tab = QWidget()
        layout = QVBoxLayout(tab)
        layout.addWidget(QLabel("Gestión de Planilla", alignment=Qt.AlignmentFlag.AlignCenter))
        tab.setLayout(layout)
        self.tabs.addTab(tab, "Planilla")

    def create_reclutamiento_tab(self):
        tab = QWidget()
        layout = QVBoxLayout(tab)
        layout.addWidget(QLabel("Reclutamiento Inteligente", alignment=Qt.AlignmentFlag.AlignCenter))
        tab.setLayout(layout)
        self.tabs.addTab(tab, "Reclutamiento")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    dark_palette = app.palette()
    dark_palette.setColor(app.palette().Window, Qt.GlobalColor.black)
    dark_palette.setColor(app.palette().WindowText, Qt.GlobalColor.white)
    dark_palette.setColor(app.palette().Base, Qt.GlobalColor.black)
    dark_palette.setColor(app.palette().AlternateBase, Qt.GlobalColor.gray)
    dark_palette.setColor(app.palette().ToolTipBase, Qt.GlobalColor.white)
    dark_palette.setColor(app.palette().ToolTipText, Qt.GlobalColor.white)
    dark_palette.setColor(app.palette().Text, Qt.GlobalColor.white)
    dark_palette.setColor(app.palette().Button, Qt.GlobalColor.black)
    dark_palette.setColor(app.palette().ButtonText, Qt.GlobalColor.white)
    dark_palette.setColor(app.palette().BrightText, Qt.GlobalColor.red)
    app.setPalette(dark_palette)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
import sys
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QTabWidget, QVBoxLayout, QPushButton,
    QTableView, QHeaderView, QFormLayout, QLineEdit, QLabel, QDialog, QMessageBox, QFileDialog


import sys
from PyQt6.QtWidgets import (
    QApplication,
    QMainWindow,
    QTabWidget,
    QWidget,
    QVBoxLayout,
    QLabel,
    QPushButton,
    QMessageBox
)
from PyQt6.QtCore import Qt
from models import Session, Empleado, Asistencia, Planilla, Puesto, Candidato
from utils.file_utils import extract_text_from_file
from utils.ollama_utils import analyze_cv_with_ollama

# Ejemplo de ventana emergente pesada con tkinter y ttkthemes
def show_heavy_popup():
    import tkinter as tk
    from tkinter import ttk
    try:
        from ttkthemes import ThemedTk
        root = ThemedTk(theme="arc")
    except Exception:
        root = tk.Tk()
    root.title("Ventana Emergente Pesada")
    label = ttk.Label(root, text="Procesando operación pesada...", font=("Arial", 16))
    label.pack(padx=20, pady=20)
    btn = ttk.Button(root, text="Cerrar", command=root.destroy)
    btn.pack(pady=10)
    root.mainloop()

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("OpenNexus RHIA Manager - Plataforma de RRHH")
        self.setGeometry(100, 100, 1200, 700)

        self.tabs = QTabWidget()
        self.setCentralWidget(self.tabs)

        self.create_empleados_tab()
        self.create_horarios_tab()
        self.create_planillas_tab()
        self.create_reclutamiento_tab()

    def create_empleados_tab(self):
        tab = QWidget()
        layout = QVBoxLayout(tab)
        layout.addWidget(QLabel("Gestión de Empleados", alignment=Qt.AlignmentFlag.AlignCenter))
        btn_popup = QPushButton("Mostrar ventana pesada (tkinter)")
        btn_popup.clicked.connect(show_heavy_popup)
        layout.addWidget(btn_popup)
        tab.setLayout(layout)
        self.tabs.addTab(tab, "Empleados")

    def create_horarios_tab(self):
        tab = QWidget()
        layout = QVBoxLayout(tab)
        layout.addWidget(QLabel("Control de Horarios", alignment=Qt.AlignmentFlag.AlignCenter))
        tab.setLayout(layout)
        self.tabs.addTab(tab, "Horarios")

    def create_planillas_tab(self):
        tab = QWidget()
        layout = QVBoxLayout(tab)
        layout.addWidget(QLabel("Gestión de Planilla", alignment=Qt.AlignmentFlag.AlignCenter))
        tab.setLayout(layout)
        self.tabs.addTab(tab, "Planilla")

    def create_reclutamiento_tab(self):
        tab = QWidget()
        layout = QVBoxLayout(tab)
        layout.addWidget(QLabel("Reclutamiento Inteligente", alignment=Qt.AlignmentFlag.AlignCenter))
        tab.setLayout(layout)
        self.tabs.addTab(tab, "Reclutamiento")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    dark_palette = app.palette()
    dark_palette.setColor(app.palette().Window, Qt.GlobalColor.black)
    dark_palette.setColor(app.palette().WindowText, Qt.GlobalColor.white)
    dark_palette.setColor(app.palette().Base, Qt.GlobalColor.black)
    dark_palette.setColor(app.palette().AlternateBase, Qt.GlobalColor.gray)
    dark_palette.setColor(app.palette().ToolTipBase, Qt.GlobalColor.white)
    dark_palette.setColor(app.palette().ToolTipText, Qt.GlobalColor.white)
    dark_palette.setColor(app.palette().Text, Qt.GlobalColor.white)
    dark_palette.setColor(app.palette().Button, Qt.GlobalColor.black)
    dark_palette.setColor(app.palette().ButtonText, Qt.GlobalColor.white)
    dark_palette.setColor(app.palette().BrightText, Qt.GlobalColor.red)
    app.setPalette(dark_palette)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
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
    # Aplicar tema Fusion y modo oscuro
    app.setStyle("Fusion")
    dark_palette = app.palette()
    dark_palette.setColor(app.palette().Window, Qt.GlobalColor.black)
    dark_palette.setColor(app.palette().WindowText, Qt.GlobalColor.white)
    dark_palette.setColor(app.palette().Base, Qt.GlobalColor.black)
    dark_palette.setColor(app.palette().AlternateBase, Qt.GlobalColor.gray)
    dark_palette.setColor(app.palette().ToolTipBase, Qt.GlobalColor.white)
    dark_palette.setColor(app.palette().ToolTipText, Qt.GlobalColor.white)
    dark_palette.setColor(app.palette().Text, Qt.GlobalColor.white)
    dark_palette.setColor(app.palette().Button, Qt.GlobalColor.black)
    dark_palette.setColor(app.palette().ButtonText, Qt.GlobalColor.white)
    dark_palette.setColor(app.palette().BrightText, Qt.GlobalColor.red)
    app.setPalette(dark_palette)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
