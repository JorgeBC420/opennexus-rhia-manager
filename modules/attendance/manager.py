from models import Session, Empleado
from typing import List, Optional

class EmployeeManager:
    """Gestor de operaciones CRUD para empleados."""

    @staticmethod
    def add_employee(nombre: str, cedula: str, iban: str, badge: str = "", salario_base: float = 0.0) -> Empleado:
        with Session() as session:
            empleado = Empleado(nombre=nombre, cedula=cedula, iban=iban, badge=badge, salario_base=salario_base)
            session.add(empleado)
            session.commit()
            return empleado

    @staticmethod
    def get_employees() -> List[Empleado]:
        with Session() as session:
            return session.query(Empleado).order_by(Empleado.nombre).all()

    @staticmethod
    def update_employee(empleado_id: int, **kwargs) -> Optional[Empleado]:
        with Session() as session:
            empleado = session.get(Empleado, empleado_id)
            if not empleado:
                return None
            for key, value in kwargs.items():
                setattr(empleado, key, value)
            session.commit()
            return empleado

    @staticmethod
    def delete_employee(empleado_id: int) -> bool:
        with Session() as session:
            empleado = session.get(Empleado, empleado_id)
            if not empleado:
                return False
            session.delete(empleado)
            session.commit()
            return True