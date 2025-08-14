import requests
from utils.file_utils import extract_text_from_file
from utils.ollama_utils import analyze_cv_with_ollama
from typing import Dict, Any, Optional

def process_candidate_application(puesto_id: int, cv_file: str, job_requirements: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    """
    Procesa la aplicación de un candidato: extrae texto del CV y lo analiza con IA.
    Args:
        puesto_id (int): ID del puesto.
        cv_file (str): Ruta al archivo del CV.
        job_requirements (dict): Requerimientos del puesto.
    Returns:
        dict | None: Análisis IA estructurado o None si falla.
    """
    cv_text = extract_text_from_file(cv_file)
    analysis = analyze_cv_with_ollama(job_requirements, cv_text)
    return analysis
