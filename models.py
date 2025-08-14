from sqlalchemy import create_engine, Column, Integer, String, Float, ForeignKey, DateTime, Boolean, LargeBinary
from sqlalchemy.orm import declarative_base, relationship, sessionmaker
from datetime import datetime
from config import DATABASE_URI
from typing import Optional

Base = declarative_base()
engine = create_engine(DATABASE_URI)
Session = sessionmaker(bind=engine)

class Empleado(Base):
    __tablename__ = 'empleados'
    id = Column(Integer, primary_key=True)
    nombre = Column(String(100), nullable=False)
    badge = Column(String(20))
    cedula = Column(String(15), nullable=False, unique=True)
    iban = Column(String(34), nullable=False)
    documentos = relationship('DocumentoEmpleado', back_populates='empleado')
    asistencias = relationship('Asistencia', back_populates='empleado')

class DocumentoEmpleado(Base):
    __tablename__ = 'documentos_empleado'
    id = Column(Integer, primary_key=True)
    empleado_id = Column(Integer, ForeignKey('empleados.id'))
    nombre = Column(String(100))
    archivo = Column(LargeBinary)
    empleado = relationship('Empleado', back_populates='documentos')

class Asistencia(Base):
    __tablename__ = 'asistencias'
    id = Column(Integer, primary_key=True)
    empleado_id = Column(Integer, ForeignKey('empleados.id'))
    fecha = Column(DateTime, default=datetime.now)
    tipo = Column(String(10)) # entrada/salida
    empleado = relationship('Empleado', back_populates='asistencias')

class Puesto(Base):
    __tablename__ = 'puestos'
    id = Column(Integer, primary_key=True)
    nombre = Column(String(100), nullable=False)
    activo = Column(Boolean, default=True)
    candidatos = relationship('Candidato', back_populates='puesto')

class Candidato(Base):
    __tablename__ = 'candidatos'
    id = Column(Integer, primary_key=True)
    nombre = Column(String(100), nullable=False)
    puesto_id = Column(Integer, ForeignKey('puestos.id'))
    cv = Column(LargeBinary)
    analisis_ia = Column(String)
    puesto = relationship('Puesto', back_populates='candidatos')

Base.metadata.create_all(engine)
