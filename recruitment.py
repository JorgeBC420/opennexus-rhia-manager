import requests
from .file_utils import extract_text_from_file
import json

def analyze_cv_with_ollama(job_requirements, cv_text, model="llama3"):
    prompt = f"""
Actúa como un reclutador técnico senior altamente experimentado para una startup de tecnología en Costa Rica. Tu tarea es analizar el siguiente currículum y evaluarlo objetivamente contra los requerimientos del puesto.

Puesto:
{job_requirements['puesto']}

Requerimientos Clave:
{job_requirements['requerimientos']}

Texto del Currículum:
---
{cv_text}
---

Tu Tarea:
Analiza el CV y proporciona tu evaluación EXCLUSIVAMENTE en formato JSON. No añadas ningún texto antes o después del JSON. La estructura debe ser la siguiente:

{
  "puntuacion_general": <un número entero de 1 a 100, donde 100 es una coincidencia perfecta>,
  "resumen_alineacion": "<Un resumen conciso de 2-3 frases explicando por qué el candidato es o no es un buen fit>",
  "habilidades_encontradas": ["<lista de habilidades clave mencionadas en el CV que coinciden con los requerimientos>"],
  "experiencia_relevante_anos": <un número estimado de años de experiencia relevante basado en el CV>,
  "nivel_ingles_estimado": "<A1, A2, B1, B2, C1, C2, o N/A si no se menciona>",
  "puntos_fuertes": "<Describe en una frase los puntos más fuertes del candidato para este puesto>",
  "posibles_debilidades": "<Describe en una frase las posibles áreas donde el candidato no cumple o donde se necesita más información>"
}
"""
    response = requests.post(
        "http://localhost:11434/api/generate",
        json={"model": model, "prompt": prompt}
    )
    result = response.json()
    # Extraer solo el JSON de la respuesta
    try:
        analysis = json.loads(result['response'])
    except Exception:
        analysis = None
    return analysis

def process_candidate_application(puesto_id, cv_file, job_requirements):
    file_path = extract_text_from_file(cv_file)
    cv_text = extract_text_from_file(file_path)
    analysis = analyze_cv_with_ollama(job_requirements, cv_text)
    return analysis
