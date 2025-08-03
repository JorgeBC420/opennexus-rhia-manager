import pandas as pd
from fpdf import FPDF
from sqlalchemy.orm import Session

def export_employees_to_excel(session: Session, output_path=None):
    from models import Empleado
    empleados = session.query(Empleado).all()
    data = [{
        'ID': e.id,
        'Nombre': e.nombre,
        'Badge': e.badge,
        'Cédula': e.cedula,
        'IBAN': e.iban
    } for e in empleados]
    df = pd.DataFrame(data)
    if output_path:
        df.to_excel(output_path, index=False)
    return df

def export_candidates_to_pdf(session: Session, puesto_id=None, output_path=None):
    from models import Candidato, Puesto
    query = session.query(Candidato)
    if puesto_id:
        query = query.filter(Candidato.puesto_id == puesto_id)
    candidatos = query.all()
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, txt="Reporte de Candidatos", ln=True, align='C')
    for c in candidatos:
        pdf.cell(0, 10, txt=f"ID: {c.id} | Nombre: {c.nombre}", ln=True)
        pdf.multi_cell(0, 10, txt=f"Análisis IA: {c.analisis_ia or 'N/A'}")
    if output_path:
        pdf.output(output_path)
    return pdf
